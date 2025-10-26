@echo off
echo.
echo 🌍 USGS Earthquake Monitor Launcher
echo ====================================
echo.
echo Checking Python installation...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python from python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found!
echo.
echo Installing required packages...
python -m pip install matplotlib numpy requests >nul 2>&1

echo ✅ Dependencies installed!
echo.
echo 🚀 Starting USGS Earthquake Monitor...
echo.

python mp10Ex.py

echo.
echo 👋 Thanks for using USGS Earthquake Monitor!
pause