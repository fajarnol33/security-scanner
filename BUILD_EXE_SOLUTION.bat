@echo off
echo ============================================================
echo    Security Scanner - EXE Builder Solution
echo ============================================================
echo.
echo Since Python is not installed on this system, here are your options:
echo.
echo 🔧 OPTION 1: Install Python (Recommended)
echo    1. Go to: https://python.org/downloads/
echo    2. Download Python 3.11 or newer
echo    3. IMPORTANT: Check "Add Python to PATH" during installation
echo    4. Restart this terminal after installation
echo    5. Run: python build_exe.py
echo.
echo 📦 OPTION 2: Use Online Build Service
echo    1. Upload this project to GitHub
echo    2. Use GitHub Actions to build EXE automatically
echo    3. Download the built EXE file
echo.
echo 💻 OPTION 3: Use Another Computer
echo    1. Copy this folder to a computer with Python installed
echo    2. Run: python build_exe.py
echo    3. Copy the resulting EXE back to this computer
echo.
echo 🌐 OPTION 4: Use the Python Version (No EXE needed)
echo    1. Install Python on target computers
echo    2. Copy the SecurityScanner_Portable_Python folder
echo    3. Run: RUN_SECURITY_SCANNER.bat
echo.
echo Creating portable Python version as backup...
echo.

python create_portable.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Cannot create portable version - Python not found
    echo.
    echo 📋 MANUAL STEPS TO BUILD EXE:
    echo.
    echo 1. Install Python from: https://python.org/downloads/
    echo 2. Open new terminal and run: python build_exe.py
    echo 3. Your EXE will be in: SecurityScanner_Portable/SecurityScanner.exe
    echo.
    echo 📁 All build files are ready in this folder!
    echo.
)

echo.
echo Press any key to exit...
pause >nul
