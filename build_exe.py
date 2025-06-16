#!/usr/bin/env python3
"""
Security Scanner - Portable EXE Builder
Builds a standalone executable for Windows
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🛡️  Security Scanner - Portable EXE Builder")
    print("=" * 60)
    print()

def check_python():
    """Check if Python is available"""
    try:
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 7:
            print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} - OK")
            return True
        else:
            print(f"❌ Python {python_version.major}.{python_version.minor} - Need Python 3.7+")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def install_build_requirements():
    """Install PyInstaller and dependencies"""
    print("\n📦 Installing build requirements...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements-build.txt'
        ], check=True, capture_output=True, text=True)
        print("✅ Build requirements installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_icon():
    """Create a simple icon file"""
    print("\n🎨 Creating application icon...")
    
    # Create a simple ICO file (this is a minimal approach)
    # In production, you'd want a proper icon
    icon_content = """
    AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A
    """
    
    try:
        # For now, we'll skip icon creation and let PyInstaller use default
        print("✅ Using default application icon")
        return True
    except Exception as e:
        print(f"⚠️  Icon creation skipped: {e}")
        return True

def create_version_info():
    """Create version info for Windows executable"""
    print("\n📄 Creating version info...")
    
    version_info = '''
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Security Scanner'),
        StringStruct(u'FileDescription', u'Website Vulnerability Assessment Tool'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'SecurityScanner'),
        StringStruct(u'LegalCopyright', u'© 2025 Security Scanner'),
        StringStruct(u'OriginalFilename', u'SecurityScanner.exe'),
        StringStruct(u'ProductName', u'Security Scanner'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    try:
        with open('version_info.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)
        print("✅ Version info created")
        return True
    except Exception as e:
        print(f"❌ Failed to create version info: {e}")
        return False

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building portable executable...")
    
    try:
        # Build command
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            'SecurityScanner.spec',
            '--clean',
            '--noconfirm'
        ]
        
        print("Running PyInstaller...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            return True
        else:
            print(f"❌ Build failed!")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Build process failed: {e}")
        return False

def create_portable_package():
    """Create portable package with necessary files"""
    print("\n📦 Creating portable package...")
    
    try:
        # Create portable directory
        portable_dir = Path("SecurityScanner_Portable")
        if portable_dir.exists():
            shutil.rmtree(portable_dir)
        portable_dir.mkdir()
        
        # Copy executable
        exe_path = Path("dist/SecurityScanner.exe")
        if exe_path.exists():
            shutil.copy2(exe_path, portable_dir / "SecurityScanner.exe")
            print("✅ Executable copied")
        else:
            print("❌ Executable not found!")
            return False
        
        # Create README for portable version
        readme_content = """
# Security Scanner - Portable Version

## 🚀 How to Use
1. Double-click SecurityScanner.exe
2. Browser will open to http://localhost:5000
3. Enter website URL and click "Scan Website"

## ⚠️ Important
- Use only on websites you own or have permission to test
- For educational purposes only
- Antivirus may flag this as suspicious (false positive)

## 🛡️ Features
- SQL Injection Detection
- XSS Vulnerability Testing
- Command Injection Scanning
- Sensitive File Detection
- Security Headers Analysis

## 📞 Troubleshooting
- If Windows blocks the exe, click "More info" → "Run anyway"
- Make sure port 5000 is not being used by other applications
- Check Windows Firewall if browser doesn't open automatically

## 🎓 Educational Use Only
This tool is for learning cybersecurity and testing your own websites.
Unauthorized use is prohibited and may be illegal.

Version: 1.0.0
Built: 2025
"""
        
        with open(portable_dir / "README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("✅ Portable package created successfully!")
        print(f"📁 Location: {portable_dir.absolute()}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create portable package: {e}")
        return False

def cleanup():
    """Clean up build files"""
    print("\n🧹 Cleaning up build files...")
    
    cleanup_dirs = ['build', '__pycache__']
    cleanup_files = ['version_info.txt']
    
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Removed {dir_name}")
    
    for file_name in cleanup_files:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"✅ Removed {file_name}")

def main():
    """Main build process"""
    print_header()
    
    # Pre-build checks
    if not check_python():
        print("\n❌ Python version check failed!")
        return False
    
    if not os.path.exists('app/main.py'):
        print("\n❌ app/main.py not found! Are you in the correct directory?")
        return False
    
    # Build process
    steps = [
        ("Install Requirements", install_build_requirements),
        ("Create Icon", create_icon),
        ("Create Version Info", create_version_info),
        ("Build Executable", build_executable),
        ("Create Portable Package", create_portable_package),
        ("Cleanup", cleanup)
    ]
    
    for step_name, step_func in steps:
        print(f"\n🔄 {step_name}...")
        if not step_func():
            print(f"\n❌ {step_name} failed! Build aborted.")
            return False
    
    print("\n" + "=" * 60)
    print("🎉 BUILD SUCCESSFUL!")
    print("=" * 60)
    print("📁 Your portable Security Scanner is ready!")
    print("📂 Location: SecurityScanner_Portable/")
    print("🚀 Run: SecurityScanner_Portable/SecurityScanner.exe")
    print("\n⚠️  IMPORTANT:")
    print("- Use only for educational purposes")
    print("- Test only websites you own")
    print("- Some antivirus may flag as suspicious (false positive)")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            print("\n❌ Build failed! Check errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Build cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
