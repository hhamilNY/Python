@echo off
echo.
echo 🚀 USGS Earthquake Monitor - Build System
echo =========================================
echo.

echo 📊 Checking current status...
python version_status.py

echo.
echo 🔨 Starting automated build process...
echo.

python build_manager.py

echo.
echo ✅ Build system completed!
pause