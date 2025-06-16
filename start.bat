@echo off
echo ============================================================
echo    Security Scanner - Website Vulnerability Assessment
echo ============================================================
echo.
echo 🛡️  Starting Security Scanner...
echo ⚠️  WARNING: Use responsibly - only scan websites you own!
echo.

REM Try to run with different Python commands
python launcher.py
if %ERRORLEVEL% NEQ 0 (
    python3 launcher.py
    if %ERRORLEVEL% NEQ 0 (
        py launcher.py
        if %ERRORLEVEL% NEQ 0 (
            echo.
            echo ❌ Could not start with launcher. Trying direct method...
            echo.
            python app/main.py
            if %ERRORLEVEL% NEQ 0 (
                python3 app/main.py
                if %ERRORLEVEL% NEQ 0 (
                    py app/main.py
                    if %ERRORLEVEL% NEQ 0 (
                        echo.
                        echo ❌ Failed to start Security Scanner!
                        echo    Please make sure Python is installed and added to PATH
                        echo    Or try installing from Microsoft Store
                        echo.
                    )
                )
            )
        )
    )
)

echo.
echo Press any key to exit...
pause >nul
