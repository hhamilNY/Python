"""
Automated Build System for USGS Earthquake Monitor
Handles versioning, release notes, and organized builds
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from change_tracker import ChangeTracker


class BuildManager:
    def __init__(self):
        self.project_root = Path.cwd()
        self.version_file = self.project_root / "version.json"
        self.builds_dir = self.project_root / "builds"
        self.main_script = "mp10Ex.py"
        
    def load_version_info(self):
        """Load current version information"""
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                return json.load(f)
        else:
            # Default version info
            return {
                "version": "1.0.0",
                "build_number": 1,
                "release_date": datetime.now().strftime("%Y-%m-%d"),
                "release_notes": "Initial release"
            }
    
    def save_version_info(self, version_info):
        """Save updated version information"""
        with open(self.version_file, 'w') as f:
            json.dump(version_info, f, indent=4)
    
    def increment_version(self, version_type="patch"):
        """Increment version number based on type (major, minor, patch)"""
        version_info = self.load_version_info()
        version_parts = version_info["version"].split(".")
        major, minor, patch = map(int, version_parts)
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        else:  # patch
            patch += 1
        
        version_info["version"] = f"{major}.{minor}.{patch}"
        version_info["build_number"] += 1
        version_info["release_date"] = datetime.now().strftime("%Y-%m-%d")
        
        return version_info
    
    def get_release_notes(self):
        """Interactive release notes input with change detection"""
        # First, check for automated changes
        print("\n� Checking for code changes...")
        tracker = ChangeTracker()
        changes, summary = tracker.get_change_summary()
        
        if changes:
            print("📊 DETECTED CHANGES:")
            print("-" * 30)
            print(f"Files modified: {len(summary['files_modified'])}")
            print(f"Total changes: {summary['total_changes']}")
            
            print("\n�📝 SUGGESTED RELEASE NOTES:")
            print("-" * 30)
            print(summary['suggested_notes'])
            
            print("\n" + "=" * 50)
            choice = input("Use suggested notes? (y)es, (e)dit, or (c)ustom: ").strip().lower()
            
            if choice == 'y':
                return summary['suggested_notes']
            elif choice == 'e':
                print("\n✏️ Edit the suggested notes below:")
                print("(Modify as needed, press Enter twice to finish)")
                print("-" * 50)
                
                # Pre-populate with suggested notes
                lines = summary['suggested_notes'].split('\n')
                print("Current suggested notes:")
                for i, line in enumerate(lines, 1):
                    print(f"{i:2d}: {line}")
                
                print("\nEnter your modified notes (press Enter twice to finish):")
                notes = []
                while True:
                    line = input()
                    if line == "" and notes and notes[-1] == "":
                        break
                    notes.append(line)
                
                # Remove trailing empty lines
                while notes and notes[-1] == "":
                    notes.pop()
                
                return "\n".join(notes)
            else:
                # Fall through to custom input
                pass
        else:
            print("✅ No automated changes detected.")
        
        # Custom release notes input
        print("\n📝 Enter Custom Release Notes:")
        print("Enter your release notes (press Enter twice to finish):")
        print("-" * 50)
        
        notes = []
        while True:
            line = input()
            if line == "" and notes and notes[-1] == "":
                break
            notes.append(line)
        
        # Remove trailing empty lines
        while notes and notes[-1] == "":
            notes.pop()
        
        return "\n".join(notes)
    
    def create_build_directory(self, version_info):
        """Create versioned build directory"""
        version = version_info["version"]
        build_num = version_info["build_number"]
        build_name = f"v{version}_build{build_num}"
        
        build_dir = self.builds_dir / build_name
        build_dir.mkdir(parents=True, exist_ok=True)
        
        return build_dir, build_name
    
    def copy_source_files(self, build_dir):
        """Copy source files to build directory"""
        files_to_copy = [
            "mp10Ex.py",
            "requirements.txt",
            "README.md",
            "RUN_EARTHQUAKE_MONITOR.bat"
        ]
        
        for file_name in files_to_copy:
            src_file = self.project_root / file_name
            if src_file.exists():
                shutil.copy2(src_file, build_dir / file_name)
    
    def build_executable(self, build_dir, version_info):
        """Build executable in the versioned directory"""
        version = version_info["version"]
        build_num = version_info["build_number"]
        exe_name = f"USGS_Earthquake_Monitor_v{version}"
        
        print(f"🔨 Building executable: {exe_name}.exe")
        
        # Change to build directory
        original_dir = os.getcwd()
        os.chdir(build_dir)
        
        try:
            # Build with UV and PyInstaller
            cmd = [
                "uv", "run", "pyinstaller",
                "--onefile",
                "--name", exe_name,
                "--distpath", ".",
                "--workpath", "temp_build",
                "--specpath", "temp_build",
                "mp10Ex.py"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=original_dir)
            
            if result.returncode == 0:
                # Clean up temporary files
                if Path("temp_build").exists():
                    shutil.rmtree("temp_build")
                return True, exe_name
            else:
                print(f"❌ Build failed: {result.stderr}")
                return False, None
                
        finally:
            os.chdir(original_dir)
    
    def create_release_info(self, build_dir, version_info, build_name):
        """Create release information file"""
        release_info = {
            "build_name": build_name,
            "version": version_info["version"],
            "build_number": version_info["build_number"],
            "release_date": version_info["release_date"],
            "release_notes": version_info["release_notes"],
            "files": [],
            "build_timestamp": datetime.now().isoformat()
        }
        
        # List all files in build directory
        for file_path in build_dir.iterdir():
            if file_path.is_file():
                release_info["files"].append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "type": "executable" if file_path.suffix == ".exe" else "source"
                })
        
        # Save release info
        with open(build_dir / "RELEASE_INFO.json", 'w') as f:
            json.dump(release_info, f, indent=4)
        
        # Create human-readable release notes
        with open(build_dir / "RELEASE_NOTES.txt", 'w') as f:
            f.write(f"USGS Earthquake Monitor - Version {version_info['version']}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Build Number: {version_info['build_number']}\n")
            f.write(f"Release Date: {version_info['release_date']}\n")
            f.write(f"Build Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("Release Notes:\n")
            f.write("-" * 20 + "\n")
            f.write(version_info['release_notes'])
            f.write("\n\n")
            f.write("Files in this release:\n")
            f.write("-" * 25 + "\n")
            for file_info in release_info["files"]:
                size_mb = file_info["size"] / (1024 * 1024)
                f.write(f"- {file_info['name']} ({size_mb:.2f} MB) [{file_info['type']}]\n")
    
    def show_build_summary(self, build_dir, version_info, build_name):
        """Display build summary"""
        print("\n" + "=" * 60)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📦 Build Name: {build_name}")
        print(f"🔢 Version: {version_info['version']}")
        print(f"🏗️ Build Number: {version_info['build_number']}")
        print(f"📅 Release Date: {version_info['release_date']}")
        print(f"📁 Build Directory: {build_dir.relative_to(self.project_root)}")
        print("\n📋 Files Created:")
        
        for file_path in sorted(build_dir.iterdir()):
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                icon = "🎯" if file_path.suffix == ".exe" else "📄"
                print(f"  {icon} {file_path.name} ({size_mb:.2f} MB)")
        
        print(f"\n📝 Release Notes:")
        print("-" * 20)
        print(version_info['release_notes'])
        print("\n" + "=" * 60)
    
    def interactive_build(self):
        """Interactive build process with user approval"""
        print("🚀 USGS Earthquake Monitor - Automated Build System")
        print("=" * 60)
        
        # Load current version
        current_version = self.load_version_info()
        print(f"📊 Current Version: {current_version['version']} (Build {current_version['build_number']})")
        
        # Ask for version increment type
        print("\n🔄 Version Increment Options:")
        print("1. Patch (1.0.0 → 1.0.1) - Bug fixes, small changes")
        print("2. Minor (1.0.0 → 1.1.0) - New features, improvements")
        print("3. Major (1.0.0 → 2.0.0) - Breaking changes, major updates")
        
        while True:
            choice = input("\nSelect increment type (1-3): ").strip()
            if choice == "1":
                version_type = "patch"
                break
            elif choice == "2":
                version_type = "minor"
                break
            elif choice == "3":
                version_type = "major"
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
        
        # Calculate new version
        new_version_info = self.increment_version(version_type)
        print(f"\n📈 New Version: {new_version_info['version']} (Build {new_version_info['build_number']})")
        
        # Get release notes
        release_notes = self.get_release_notes()
        new_version_info["release_notes"] = release_notes
        
        # Show build preview
        print(f"\n📋 Build Preview:")
        print(f"Version: {new_version_info['version']}")
        print(f"Build: {new_version_info['build_number']}")
        print(f"Date: {new_version_info['release_date']}")
        print(f"Notes: {release_notes[:100]}{'...' if len(release_notes) > 100 else ''}")
        
        # Ask for approval
        approval = input(f"\n✅ Approve this build? (y/N): ").strip().lower()
        if approval != 'y':
            print("❌ Build cancelled by user.")
            return False
        
        # Create build
        print("\n🔨 Starting build process...")
        
        # Create build directory
        build_dir, build_name = self.create_build_directory(new_version_info)
        print(f"📁 Created build directory: {build_name}")
        
        # Copy source files
        self.copy_source_files(build_dir)
        print("📄 Copied source files")
        
        # Build executable
        success, exe_name = self.build_executable(build_dir, new_version_info)
        if not success:
            print("❌ Build failed!")
            return False
        
        print(f"✅ Executable created: {exe_name}.exe")
        
        # Create release documentation
        self.create_release_info(build_dir, new_version_info, build_name)
        print("📝 Generated release documentation")
        
        # Update version file
        self.save_version_info(new_version_info)
        print("💾 Updated version information")
        
        # Show summary
        self.show_build_summary(build_dir, new_version_info, build_name)
        
        return True


def main():
    """Main build script entry point"""
    try:
        builder = BuildManager()
        success = builder.interactive_build()
        
        if success:
            print("\n🎯 Build system completed successfully!")
            print("💡 Tip: Your versioned build is ready for distribution!")
        else:
            print("\n⚠️ Build process was not completed.")
            
    except KeyboardInterrupt:
        print("\n\n❌ Build cancelled by user (Ctrl+C)")
    except Exception as e:
        print(f"\n❌ Build system error: {e}")
        print("💡 Please check your setup and try again.")


if __name__ == "__main__":
    main()