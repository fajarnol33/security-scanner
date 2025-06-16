#!/usr/bin/env python3
"""
Test script untuk Security Scanner
"""

import os
import sys
import subprocess

def check_python():
    """Check Python installation"""
    print("🐍 Checking Python installation...")
    try:
        python_version = sys.version
        print(f"✅ Python version: {python_version}")
        return True
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True, check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_import():
    """Test importing Flask and other dependencies"""
    print("\n🔍 Testing imports...")
    try:
        import flask
        print(f"✅ Flask version: {flask.__version__}")
        
        import requests
        print(f"✅ Requests version: {requests.__version__}")
        
        import bs4
        print(f"✅ BeautifulSoup4 version: {bs4.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_flask_app():
    """Test Flask app initialization"""
    print("\n🌐 Testing Flask app...")
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from app.main import app
        
        # Test app creation
        if app:
            print("✅ Flask app created successfully")
            
            # Test route
            with app.test_client() as client:
                response = client.get('/')
                if response.status_code == 200:
                    print("✅ Main route accessible")
                    return True
                else:
                    print(f"❌ Main route returned status: {response.status_code}")
                    return False
        else:
            print("❌ Flask app creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("🛡️  Security Scanner - System Test")
    print("=" * 60)
    
    tests = [
        ("Python Check", check_python),
        ("Install Requirements", install_requirements),
        ("Test Imports", test_import),
        ("Test Flask App", test_flask_app)
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
        print("\n🎉 All tests passed! You can now run the Security Scanner:")
        print("   python app/main.py")
        print("   Then open: http://localhost:5000")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print("\n⚠️  Remember: Use this tool responsibly and only on websites you own!")

if __name__ == '__main__':
    main()
