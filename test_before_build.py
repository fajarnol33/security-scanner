#!/usr/bin/env python3
"""
Pre-Build Testing Script
Tests all functionality before building EXE
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    required_modules = [
        'flask', 'requests', 'bs4', 'urllib3', 'ssl', 'socket',
        'urllib.parse', 'warnings', 'datetime', 'time', 'random',
        'threading', 'webbrowser', 're'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module} - {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n❌ Failed imports: {failed_imports}")
        return False
    
    print("✅ All imports successful")
    return True

def test_file_structure():
    """Test required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app/main.py',
        'app/templates/index.html',
        'requirements.txt',
        'requirements-build.txt',
        'SecurityScanner.spec',
        'build_exe.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - Missing")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_flask_app():
    """Test Flask app functionality"""
    print("\n🌐 Testing Flask app...")
    
    try:
        sys.path.append('app')
        from main import app
        
        with app.test_client() as client:
            # Test main route
            response = client.get('/')
            if response.status_code == 200:
                print("  ✅ Main route works")
            else:
                print(f"  ❌ Main route failed: {response.status_code}")
                return False
            
            # Test POST with URL
            response = client.post('/', data={'url': 'https://example.com'})
            if response.status_code == 200:
                print("  ✅ POST route works")
            else:
                print(f"  ❌ POST route failed: {response.status_code}")
                return False
        
        print("✅ Flask app functional")
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def test_vulnerability_functions():
    """Test vulnerability detection functions"""
    print("\n🛡️ Testing vulnerability functions...")
    
    try:
        sys.path.append('app')
        from main import (
            check_headers, check_ssl_certificate, 
            check_forms_and_inputs, check_directory_listing
        )
        
        # Test functions exist and are callable
        test_url = "https://httpbin.org"
        
        functions_to_test = [
            ('Headers Check', check_headers),
            ('SSL Check', check_ssl_certificate),
            ('Forms Check', check_forms_and_inputs),
            ('Directory Check', check_directory_listing)
        ]
        
        for func_name, func in functions_to_test:
            try:
                result = func(test_url)
                if isinstance(result, list):
                    print(f"  ✅ {func_name} - Returns list")
                else:
                    print(f"  ⚠️ {func_name} - Unexpected return type")
            except Exception as e:
                print(f"  ❌ {func_name} - Error: {e}")
                return False
        
        print("✅ Vulnerability functions working")
        return True
        
    except Exception as e:
        print(f"❌ Vulnerability functions test failed: {e}")
        return False

def test_template_rendering():
    """Test template rendering"""
    print("\n🎨 Testing template rendering...")
    
    try:
        sys.path.append('app')
        from main import app
        
        with app.test_client() as client:
            response = client.get('/')
            content = response.get_data(as_text=True)
            
            # Check for key elements
            required_elements = [
                'Security Scanner',
                'Scan Website',
                'form',
                'input',
                'button'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element.lower() not in content.lower():
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"  ❌ Missing template elements: {missing_elements}")
                return False
            
            print("  ✅ All template elements present")
        
        print("✅ Template rendering works")
        return True
        
    except Exception as e:
        print(f"❌ Template rendering test failed: {e}")
        return False

def test_pyinstaller_compatibility():
    """Test PyInstaller compatibility"""
    print("\n🔨 Testing PyInstaller compatibility...")
    
    try:
        # Check if PyInstaller is available
        result = subprocess.run([sys.executable, '-c', 'import PyInstaller'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ PyInstaller available")
        else:
            print("  ❌ PyInstaller not available")
            return False
        
        # Test spec file syntax
        if Path('SecurityScanner.spec').exists():
            with open('SecurityScanner.spec', 'r') as f:
                spec_content = f.read()
                if 'Analysis' in spec_content and 'EXE' in spec_content:
                    print("  ✅ Spec file looks valid")
                else:
                    print("  ❌ Spec file invalid")
                    return False
        
        print("✅ PyInstaller compatibility good")
        return True
        
    except Exception as e:
        print(f"❌ PyInstaller compatibility test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Security Scanner - Pre-Build Testing")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure", test_file_structure),
        ("Flask App", test_flask_app),
        ("Vulnerability Functions", test_vulnerability_functions),
        ("Template Rendering", test_template_rendering),
        ("PyInstaller Compatibility", test_pyinstaller_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Tests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Ready to build EXE!")
        print("   Run: python build_exe.py")
        print("   Or: double-click build.bat")
        return True
    else:
        print("\n⚠️ Some tests failed. Fix issues before building.")
        return False

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Testing cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
