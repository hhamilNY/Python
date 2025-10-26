"""
Build script to create standalone executable for USGS Earthquake Monitor
"""
import subprocess
import sys
import os

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("🚀 Building USGS Earthquake Monitor Executable...")
    print("="*50)
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window (for GUI apps)
        "--name=USGS_Earthquake_Monitor",  # Custom name
        "--icon=earthquake.ico",  # Custom icon (if available)
        "--add-data=*.py;.",  # Include Python files
        "--hidden-import=matplotlib",
        "--hidden-import=numpy", 
        "--hidden-import=requests",
        "--hidden-import=datetime",
        "mp10Ex.py"
    ]
    
    try:
        print("Building executable...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ SUCCESS! Executable built successfully!")
            print(f"📁 Location: {os.path.abspath('dist/USGS_Earthquake_Monitor.exe')}")
            print("\n📋 Distribution Instructions:")
            print("1. Copy 'USGS_Earthquake_Monitor.exe' to any computer")
            print("2. Double-click to run (no Python installation needed)")
            print("3. Requires internet connection for earthquake data")
        else:
            print("❌ Build failed:")
            print(result.stderr)
            
    except FileNotFoundError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed. Run this script again.")

if __name__ == "__main__":
    build_executable()