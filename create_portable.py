#!/usr/bin/env python3
"""
ALTERNATIVE: Create Standalone Python Script
Since PyInstaller requires Python installation, this creates a more portable version
"""

import os
import shutil
import zipfile
from pathlib import Path

def create_portable_version():
    """Create a portable version without PyInstaller"""
    print("🚀 Creating Portable Python Version...")
    
    # Create portable directory
    portable_dir = Path("SecurityScanner_Portable_Python")
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    portable_dir.mkdir()
    
    # Copy all necessary files
    files_to_copy = [
        "app/",
        "requirements.txt",
        "launcher.py",
        "README.md",
        "USAGE.md"
    ]
    
    for item in files_to_copy:
        src = Path(item)
        if src.is_dir():
            shutil.copytree(src, portable_dir / src.name)
        elif src.exists():
            shutil.copy2(src, portable_dir / src.name)
    
    # Create run script
    run_script = """@echo off
echo ============================================================
echo    Security Scanner - Portable Python Version
echo ============================================================
echo.
echo Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Starting Security Scanner...
echo Browser will open to: http://localhost:5000
echo.

python app/main.py

pause
"""
    
    with open(portable_dir / "RUN_SECURITY_SCANNER.bat", 'w') as f:
        f.write(run_script)
    
    # Create README
    readme = """
# Security Scanner - Portable Python Version

## How to Use:
1. Make sure Python is installed on the target computer
2. Double-click: RUN_SECURITY_SCANNER.bat
3. Browser will open to http://localhost:5000
4. Enter website URL and click "Scan Website"

## Requirements:
- Python 3.7+ installed
- Internet connection (for installing dependencies)

## Features:
- SQL Injection Detection
- XSS Vulnerability Testing  
- Command Injection Scanning
- Sensitive File Detection
- Security Headers Analysis

## Legal Notice:
Use only on websites you own or have permission to test.
For educational purposes only.
"""
    
    with open(portable_dir / "README_PORTABLE.txt", 'w') as f:
        f.write(readme)
    
    print(f"✅ Portable version created: {portable_dir}")
    return True

def create_exe_instructions():
    """Create detailed instructions for building EXE"""
    instructions = """
# 🔨 How to Build SecurityScanner.exe

## Option 1: Use Pre-built Python Executable

If you have Python installed:
1. Install PyInstaller: `pip install PyInstaller`
2. Run: `pyinstaller SecurityScanner.spec`
3. Find EXE in: `dist/SecurityScanner.exe`

## Option 2: Use Online Build Services

### GitHub Actions (Recommended)
1. Upload this project to GitHub
2. Create .github/workflows/build.yml:
```yaml
name: Build EXE
on: [push]
jobs:
  build:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - run: pip install -r requirements-build.txt
    - run: pyinstaller SecurityScanner.spec
    - uses: actions/upload-artifact@v3
      with:
        name: SecurityScanner-EXE
        path: dist/SecurityScanner.exe
```

### AppVeyor
1. Connect your GitHub repo to AppVeyor
2. Add appveyor.yml:
```yaml
image: Visual Studio 2022
install:
  - python -m pip install -r requirements-build.txt
build_script:
  - pyinstaller SecurityScanner.spec
artifacts:
  - path: dist\\SecurityScanner.exe
```

## Option 3: Cloud Build Platforms

### Replit
1. Import project to Replit
2. Install PyInstaller
3. Run build command
4. Download the EXE

### CodeSandbox
1. Create new Python environment
2. Upload project files
3. Install dependencies and PyInstaller
4. Build and download

## Option 4: Virtual Machine

1. Use Windows VM (VMware/VirtualBox)
2. Install Python + PyInstaller
3. Build the EXE
4. Transfer to main machine

## Manual Build Commands:

```bash
# Install build tools
pip install PyInstaller==6.2.0
pip install -r requirements-build.txt

# Build executable
pyinstaller --onefile --windowed --name SecurityScanner app/main.py

# Or use spec file
pyinstaller SecurityScanner.spec
```

## Troubleshooting:

### "Python not found"
- Install Python from python.org
- Check "Add to PATH" during installation
- Restart terminal after installation

### "PyInstaller not found"
```bash
python -m pip install --upgrade pip
python -m pip install PyInstaller
```

### "Missing modules"
```bash
pip install -r requirements-build.txt
```

## Expected Result:
- File: SecurityScanner.exe (~50-80MB)
- Standalone executable (no Python needed)
- Auto-opens browser to localhost:5000
- Full vulnerability scanning features

Happy Building! 🛡️
"""
    
    with open("HOW_TO_BUILD_EXE.md", 'w') as f:
        f.write(instructions)
    
    print("✅ Build instructions created: HOW_TO_BUILD_EXE.md")

if __name__ == '__main__':
    create_portable_version()
    create_exe_instructions()
    print("\n🎉 Alternative solutions created!")
    print("📁 Check: SecurityScanner_Portable_Python/")
    print("📖 Read: HOW_TO_BUILD_EXE.md")
