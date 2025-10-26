"""
Automated Change Tracking System for USGS Earthquake Monitor
Monitors code changes and generates suggested release notes
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
import difflib


class ChangeTracker:
    def __init__(self):
        self.project_root = Path.cwd()
        self.changes_file = self.project_root / "change_tracking.json"
        self.tracked_files = [
            "mp10Ex.py",
            "build_manager.py", 
            "requirements.txt",
            "README.md"
        ]
        
    def get_file_hash(self, file_path):
        """Calculate MD5 hash of file content"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except FileNotFoundError:
            return None
    
    def load_tracking_data(self):
        """Load previous tracking data"""
        if self.changes_file.exists():
            with open(self.changes_file, 'r') as f:
                return json.load(f)
        return {"last_check": None, "file_hashes": {}, "change_history": []}
    
    def save_tracking_data(self, data):
        """Save tracking data"""
        with open(self.changes_file, 'w') as f:
            json.dump(data, f, indent=4)
    
    def detect_changes(self):
        """Detect changes in tracked files"""
        tracking_data = self.load_tracking_data()
        current_hashes = {}
        changes_detected = []
        
        for file_name in self.tracked_files:
            file_path = self.project_root / file_name
            current_hash = self.get_file_hash(file_path)
            current_hashes[file_name] = current_hash
            
            if file_name in tracking_data["file_hashes"]:
                old_hash = tracking_data["file_hashes"][file_name]
                if old_hash != current_hash:
                    # File changed
                    change_info = self.analyze_file_changes(file_path, file_name)
                    changes_detected.append(change_info)
            else:
                # New file
                changes_detected.append({
                    "file": file_name,
                    "type": "new_file",
                    "description": f"Added new file: {file_name}",
                    "timestamp": datetime.now().isoformat()
                })
        
        # Update tracking data
        tracking_data["file_hashes"] = current_hashes
        tracking_data["last_check"] = datetime.now().isoformat()
        if changes_detected:
            tracking_data["change_history"].extend(changes_detected)
        
        self.save_tracking_data(tracking_data)
        return changes_detected
    
    def analyze_file_changes(self, file_path, file_name):
        """Analyze what type of changes were made to a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
        except:
            return {
                "file": file_name,
                "type": "file_error",
                "description": f"Could not read {file_name}",
                "timestamp": datetime.now().isoformat()
            }
        
        # Analyze content for specific change types
        change_type = "modified"
        description = f"Modified {file_name}"
        
        # Detect specific changes in main script
        if file_name == "mp10Ex.py":
            if "def " in current_content and "new" in current_content.lower():
                change_type = "feature_added"
                description = "Added new features to earthquake monitor"
            elif "fix" in current_content.lower() or "bug" in current_content.lower():
                change_type = "bug_fix"
                description = "Bug fixes and improvements"
            elif "option" in current_content.lower():
                change_type = "enhancement"
                description = "Enhanced monitoring options"
        
        # Check for documentation changes
        elif file_name == "README.md":
            change_type = "documentation"
            description = "Updated documentation"
        
        # Check for dependency changes
        elif file_name == "requirements.txt":
            change_type = "dependencies"
            description = "Updated project dependencies"
        
        return {
            "file": file_name,
            "type": change_type,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_suggested_release_notes(self, changes):
        """Generate suggested release notes based on detected changes"""
        if not changes:
            return "No significant changes detected."
        
        notes = []
        
        # Group changes by type
        features = [c for c in changes if c["type"] == "feature_added"]
        enhancements = [c for c in changes if c["type"] == "enhancement"]
        bug_fixes = [c for c in changes if c["type"] == "bug_fix"]
        docs = [c for c in changes if c["type"] == "documentation"]
        deps = [c for c in changes if c["type"] == "dependencies"]
        other = [c for c in changes if c["type"] not in ["feature_added", "enhancement", "bug_fix", "documentation", "dependencies"]]
        
        # Build release notes
        if features:
            notes.append("🆕 NEW FEATURES:")
            for feature in features:
                notes.append(f"  - {feature['description']}")
            notes.append("")
        
        if enhancements:
            notes.append("✨ ENHANCEMENTS:")
            for enhancement in enhancements:
                notes.append(f"  - {enhancement['description']}")
            notes.append("")
        
        if bug_fixes:
            notes.append("🐛 BUG FIXES:")
            for fix in bug_fixes:
                notes.append(f"  - {fix['description']}")
            notes.append("")
        
        if docs:
            notes.append("📚 DOCUMENTATION:")
            for doc in docs:
                notes.append(f"  - {doc['description']}")
            notes.append("")
        
        if deps:
            notes.append("📦 DEPENDENCIES:")
            for dep in deps:
                notes.append(f"  - {dep['description']}")
            notes.append("")
        
        if other:
            notes.append("🔧 OTHER CHANGES:")
            for change in other:
                notes.append(f"  - {change['description']}")
            notes.append("")
        
        return "\n".join(notes).strip()
    
    def get_change_summary(self):
        """Get summary of all changes since last build"""
        changes = self.detect_changes()
        
        if not changes:
            return None, "No changes detected since last check."
        
        summary = {
            "total_changes": len(changes),
            "files_modified": list(set(c["file"] for c in changes)),
            "change_types": list(set(c["type"] for c in changes)),
            "suggested_notes": self.generate_suggested_release_notes(changes),
            "detailed_changes": changes
        }
        
        return changes, summary


def integrate_with_build_manager():
    """Show how to integrate with build_manager.py"""
    tracker = ChangeTracker()
    changes, summary = tracker.get_change_summary()
    
    print("🔍 CHANGE DETECTION REPORT")
    print("=" * 40)
    
    if changes:
        print(f"📊 Changes Detected: {summary['total_changes']}")
        print(f"📁 Files Modified: {', '.join(summary['files_modified'])}")
        print(f"🏷️ Change Types: {', '.join(summary['change_types'])}")
        print("\n📝 SUGGESTED RELEASE NOTES:")
        print("-" * 30)
        print(summary['suggested_notes'])
        print("\n💡 You can edit these notes during the build process.")
    else:
        print("✅ No changes detected since last check.")
        print("💡 Make some code changes and run again.")
    
    return summary


if __name__ == "__main__":
    integrate_with_build_manager()