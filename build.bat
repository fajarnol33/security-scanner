@echo off
echo ============================================================
echo    Security Scanner - EXE Builder
echo ============================================================
echo.
echo 🔨 Building portable executable...
echo This may take a few minutes...
echo.

REM Try different Python commands
python build_exe.py
if %ERRORLEVEL% EQU 0 goto success

python3 build_exe.py
if %ERRORLEVEL% EQU 0 goto success

py build_exe.py
if %ERRORLEVEL% EQU 0 goto success

echo.
echo ❌ Build failed! Make sure Python is installed.
echo.
goto end

:success
echo.
echo ✅ Build completed successfully!
echo 📁 Check SecurityScanner_Portable folder
echo 🚀 Run SecurityScanner_Portable\SecurityScanner.exe
echo.

:end
echo Press any key to exit...
pause >nul
