"""
Quick version check and build status for USGS Earthquake Monitor
"""

import json
import os
from pathlib import Path
from datetime import datetime


def show_current_status():
    """Show current version and build status"""
    project_root = Path.cwd()
    version_file = project_root / "version.json"
    builds_dir = project_root / "builds"
    
    print("🌍 USGS Earthquake Monitor - Status Report")
    print("=" * 50)
    
    # Show current version
    if version_file.exists():
        with open(version_file, 'r') as f:
            version_info = json.load(f)
        
        print(f"📊 Current Version: {version_info['version']}")
        print(f"🏗️ Build Number: {version_info['build_number']}")
        print(f"📅 Last Release: {version_info['release_date']}")
        print(f"📝 Last Notes: {version_info.get('release_notes', 'No notes')[:60]}...")
    else:
        print("❌ No version file found - project not initialized")
        return
    
    # Show available builds
    if builds_dir.exists():
        builds = list(builds_dir.iterdir())
        builds = [b for b in builds if b.is_dir()]
        
        if builds:
            print(f"\n📦 Available Builds ({len(builds)}):")
            print("-" * 30)
            
            for build_dir in sorted(builds, key=lambda x: x.name, reverse=True):
                release_info_file = build_dir / "RELEASE_INFO.json"
                if release_info_file.exists():
                    with open(release_info_file, 'r') as f:
                        build_info = json.load(f)
                    
                    exe_files = [f for f in build_info['files'] if f['type'] == 'executable']
                    exe_count = len(exe_files)
                    total_size = sum(f['size'] for f in build_info['files']) / (1024 * 1024)
                    
                    print(f"  📁 {build_dir.name}")
                    print(f"     Version: {build_info['version']} | Files: {len(build_info['files'])} | Size: {total_size:.1f}MB")
                    print(f"     Executables: {exe_count} | Date: {build_info['release_date']}")
                else:
                    print(f"  📁 {build_dir.name} (no build info)")
        else:
            print("\n📦 No builds found")
    else:
        print("\n📦 No builds directory found")
    
    print("\n💡 Commands:")
    print("  python build_manager.py  - Create new build")
    print("  python version_status.py - Show this status")


if __name__ == "__main__":
    show_current_status()