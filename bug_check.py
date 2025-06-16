"""
Security Scanner - Comprehensive Bug Check and Fix Script
Checks all components for errors, imports, and compatibility issues
"""

import os
import sys
import traceback
import importlib
from pathlib import Path

def check_imports():
    """Test all required imports"""
    print("🔍 Checking imports...")
    required_modules = [
        'flask', 'requests', 'beautifulsoup4', 'urllib3', 
        'ssl', 'socket', 're', 'time', 'random', 'json'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            if module == 'beautifulsoup4':
                importlib.import_module('bs4')
            else:
                importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            missing_modules.append(module)
    
    return missing_modules

def check_flask_app():
    """Test Flask app initialization and routes"""
    print("\n🌐 Checking Flask app...")
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
        
        # Import app components
        from app.main import app
        
        # Test app creation
        if not app:
            print("❌ Flask app creation failed")
            return False
        
        print("✅ Flask app created successfully")
        
        # Test routes
        with app.test_client() as client:
            # Test main route
            response = client.get('/')
            if response.status_code != 200:
                print(f"❌ Main route error: {response.status_code}")
                return False
            print("✅ Main route accessible")
            
            # Test API route
            response = client.post('/api/scan', 
                                 json={'url': 'https://httpbin.org/get'},
                                 content_type='application/json')
            if response.status_code not in [200, 400]:  # 400 is acceptable for invalid input
                print(f"❌ API route error: {response.status_code}")
                return False
            print("✅ API route accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        traceback.print_exc()
        return False

def check_template():
    """Check template rendering"""
    print("\n🎨 Checking template...")
    try:
        template_path = Path('app/templates/index.html')
        if not template_path.exists():
            print("❌ Template file not found")
            return False
        
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for unclosed tags
        if content.count('<') != content.count('>'):
            print("❌ Unclosed HTML tags detected")
            return False
        
        # Check for Jinja2 syntax errors
        jinja_patterns = ['{%', '%}', '{{', '}}']
        for pattern in jinja_patterns:
            if content.count(pattern.replace('%', '% ')) > content.count(pattern.replace(' ', '')):
                print(f"❌ Jinja2 syntax issue with {pattern}")
                return False
        
        print("✅ Template syntax valid")
        return True
        
    except Exception as e:
        print(f"❌ Template check failed: {e}")
        return False

def check_file_structure():
    """Verify all required files exist"""
    print("\n📁 Checking file structure...")
    required_files = [
        'app/main.py',
        'app/templates/index.html',
        'requirements.txt',
        'config.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
        else:
            print(f"✅ Found: {file_path}")
    
    return missing_files

def test_vulnerability_functions():
    """Test all vulnerability detection functions"""
    print("\n🛡️ Testing vulnerability detection functions...")
    try:
        from app.main import (
            check_sql_injection, check_xss_vulnerabilities, 
            check_sensitive_files, check_command_injection,
            check_directory_traversal, check_headers
        )
        
        test_url = "https://httpbin.org/get"
        
        functions = [
            ('SQL Injection', check_sql_injection),
            ('XSS Detection', check_xss_vulnerabilities),
            ('Sensitive Files', check_sensitive_files),
            ('Command Injection', check_command_injection),
            ('Directory Traversal', check_directory_traversal),
            ('Headers Check', check_headers)
        ]
        
        for name, func in functions:
            try:
                result = func(test_url)
                if isinstance(result, list):
                    print(f"✅ {name}: Returns list with {len(result)} items")
                else:
                    print(f"❌ {name}: Invalid return type")
                    return False
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Vulnerability functions test failed: {e}")
        return False

def main():
    """Run comprehensive checks"""
    print("=" * 60)
    print("🔍 Security Scanner - Comprehensive Bug Check")
    print("=" * 60)
    
    checks = [
        ("Import Check", check_imports),
        ("File Structure", check_file_structure),
        ("Template Check", check_template),
        ("Flask App Test", check_flask_app),
        ("Vulnerability Functions", test_vulnerability_functions)
    ]
    
    all_passed = True
    results = []
    
    for check_name, check_func in checks:
        print(f"\n--- {check_name} ---")
        try:
            result = check_func()
            if isinstance(result, bool):
                passed = result
            elif isinstance(result, list):
                passed = len(result) == 0
            else:
                passed = True
            
            results.append((check_name, passed))
            if not passed:
                all_passed = False
                
        except Exception as e:
            print(f"❌ {check_name} failed with exception: {e}")
            results.append((check_name, False))
            all_passed = False
    
    print("\n" + "=" * 60)
    print("📊 Final Results")
    print("=" * 60)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    if all_passed:
        print("\n🎉 All checks passed! Ready for .exe compilation")
        return True
    else:
        print("\n⚠️ Some checks failed. Please fix issues before compilation")
        return False

if __name__ == '__main__':
    main()
