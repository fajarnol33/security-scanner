from flask import Flask, render_template, request, jsonify
import requests
import ssl
import socket
from urllib.parse import urlparse, urljoin, parse_qs, urlunparse
from bs4 import BeautifulSoup
import re
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import warnings
import os
import sys
import webbrowser
import threading
from datetime import datetime

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
try:
    warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
except:
    pass

# PyInstaller compatibility
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
    template_dir = os.path.join(application_path, 'app', 'templates')
    static_dir = os.path.join(application_path, 'app', 'static')
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(os.path.dirname(application_path), 'app', 'templates')
    static_dir = os.path.join(os.path.dirname(application_path), 'app', 'static')

app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir if os.path.exists(static_dir) else None)
app.config['SECRET_KEY'] = 'security-scanner-secret-key-2025'

def open_browser():
    """Open browser after a delay"""
    import time
    time.sleep(2)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:5000')
    except:
        pass  # Silently fail if can't open browser

def safe_request(session, method, url, **kwargs):
    """Safe request wrapper with comprehensive error handling"""
    try:
        kwargs.setdefault('timeout', 10)
        kwargs.setdefault('verify', False)
        kwargs.setdefault('allow_redirects', True)
        
        if method.upper() == 'GET':
            response = session.get(url, **kwargs)
        elif method.upper() == 'POST':
            response = session.post(url, **kwargs)
        else:
            return None
            
        return response
        
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError, 
            requests.exceptions.RequestException, Exception):
        return None

# Konfigurasi session dengan retry strategy
def get_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

# User agents untuk menghindari deteksi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Payload untuk testing berbagai kerentanan
SQL_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR 'a'='a",
    "admin'--",
    "' UNION SELECT NULL--"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>"
]

COMMAND_PAYLOADS = [
    "; cat /etc/passwd",
    "| whoami", 
    "& dir"
]

# File sensitif yang sering terekspos
SENSITIVE_FILES = [
    '.env',
    '.git/config', 
    'config.php',
    'wp-config.php',
    'backup.sql',
    'admin/',
    'phpmyadmin/'
]

# Error messages yang mengindikasikan SQL Injection
SQL_ERROR_PATTERNS = [
    r"SQL syntax.*MySQL",
    r"Warning.*mysql_.*",
    r"valid MySQL result",
    r"PostgreSQL.*ERROR",
    r"ORA-\d{4,5}",
    r"Oracle.*Driver"
]

def check_ssl_certificate(url):
    """Cek sertifikat SSL"""
    vulnerabilities = []
    try:
        hostname = urlparse(url).hostname
        if not hostname:
            return vulnerabilities
            
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if (not_after - datetime.now()).days < 30:
                    vulnerabilities.append({
                        'category': 'SSL/TLS',
                        'name': 'Sertifikat SSL Akan Expire',
                        'severity': 'Medium',
                        'description': f'Sertifikat SSL akan expire pada {not_after.strftime("%d-%m-%Y")}.',
                        'how': 'Hacker dapat melakukan man-in-the-middle attack ketika sertifikat sudah expire.',
                        'mitigation': 'Perbarui sertifikat SSL sebelum tanggal expiry.'
                    })
    except:
        pass
    
    return vulnerabilities

def check_headers(url):
    """Cek security headers"""
    vulnerabilities = []
    try:
        session = get_session()
        resp = safe_request(session, 'GET', url)
        if not resp:
            return vulnerabilities
            
        headers = resp.headers
        
        security_headers = {
            'X-Frame-Options': {
                'name': 'Clickjacking Protection',
                'description': 'Header X-Frame-Options tidak ditemukan. Website rentan terhadap clickjacking.',
                'how': 'Hacker dapat membuat website palsu yang menampilkan website Anda dalam iframe tersembunyi.',
                'mitigation': 'Tambahkan header "X-Frame-Options: DENY" atau "X-Frame-Options: SAMEORIGIN"'
            },
            'Content-Security-Policy': {
                'name': 'Cross-Site Scripting (XSS) Protection', 
                'description': 'Header Content-Security-Policy tidak ditemukan. Website rentan terhadap serangan XSS.',
                'how': 'Hacker dapat menyisipkan script JavaScript berbahaya.',
                'mitigation': 'Implementasikan Content Security Policy yang ketat.'
            },
            'Strict-Transport-Security': {
                'name': 'HTTPS Downgrade Attack',
                'description': 'Header Strict-Transport-Security tidak ditemukan.',
                'how': 'Hacker dapat memaksa user mengakses website melalui HTTP yang tidak terenkripsi.',
                'mitigation': 'Tambahkan header "Strict-Transport-Security: max-age=31536000"'
            }
        }
        
        for header, info in security_headers.items():
            if header not in headers:
                vulnerabilities.append({
                    'category': 'Security Headers',
                    'name': info['name'],
                    'severity': 'High',
                    'description': info['description'],
                    'how': info['how'],
                    'mitigation': info['mitigation']
                })
                
    except Exception:
        pass
    
    return vulnerabilities

def check_sql_injection(url):
    """Test SQL Injection vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        original_response = safe_request(session, 'GET', url, headers=headers)
        if not original_response:
            return vulnerabilities
            
        soup = BeautifulSoup(original_response.content, 'html.parser')
        forms = soup.find_all('form')
        
        for form in forms:
            if form.get('method', '').lower() == 'post':
                action = form.get('action', '')
                if action and not action.startswith('http'):
                    action = urljoin(url, action)
                elif not action:
                    action = url
                
                inputs = form.find_all(['input', 'textarea'])
                form_data = {}
                
                for inp in inputs:
                    name = inp.get('name')
                    if name and inp.get('type') not in ['submit', 'button', 'reset']:
                        form_data[name] = 'test'
                
                for payload in SQL_PAYLOADS[:2]:  # Limit payloads
                    test_data = form_data.copy()
                    
                    for field in test_data:
                        test_data[field] = payload
                        
                        response = safe_request(session, 'POST', action, data=test_data, headers=headers)
                        if response:
                            for pattern in SQL_ERROR_PATTERNS:
                                if re.search(pattern, response.text, re.IGNORECASE):
                                    vulnerabilities.append({
                                        'category': 'SQL Injection',
                                        'name': f'SQL Injection Vulnerability - Field: {field}',
                                        'severity': 'Critical',
                                        'description': f'Field "{field}" rentan terhadap SQL Injection.',
                                        'how': 'Hacker dapat bypass authentication atau mengakses database.',
                                        'mitigation': 'Gunakan prepared statements dan validasi input.',
                                        'payload_used': payload,
                                        'field': field
                                    })
                                    break
                        
                        test_data[field] = 'test'
                        time.sleep(0.5)
                        
    except Exception:
        pass
    
    return vulnerabilities

def check_xss_vulnerabilities(url):
    """Test Cross-Site Scripting vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = safe_request(session, 'GET', url, headers=headers)
        if not response:
            return vulnerabilities
            
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all('form')
        
        for form in forms:
            action = form.get('action', '')
            if action and not action.startswith('http'):
                action = urljoin(url, action)
            elif not action:
                action = url
            
            method = form.get('method', 'get').lower()
            inputs = form.find_all(['input', 'textarea'])
            
            form_data = {}
            text_inputs = []
            
            for inp in inputs:
                name = inp.get('name')
                input_type = inp.get('type', 'text')
                
                if name and input_type not in ['submit', 'button', 'reset', 'hidden']:
                    if input_type in ['text', 'email', 'search'] or inp.name == 'textarea':
                        text_inputs.append(name)
                        form_data[name] = 'test'
                    else:
                        form_data[name] = 'test'
            
            for field in text_inputs:
                for payload in XSS_PAYLOADS[:2]:
                    test_data = form_data.copy()
                    test_data[field] = payload
                    
                    if method == 'post':
                        response = safe_request(session, 'POST', action, data=test_data, headers=headers)
                    else:
                        response = safe_request(session, 'GET', action, params=test_data, headers=headers)
                    
                    if response and payload in response.text:
                        vulnerabilities.append({
                            'category': 'Cross-Site Scripting (XSS)',
                            'name': f'Reflected XSS - Field: {field}',
                            'severity': 'High',
                            'description': f'Field "{field}" rentan terhadap Reflected XSS.',
                            'how': 'Hacker dapat mengirim link berbahaya dengan script JavaScript.',
                            'mitigation': 'Lakukan HTML encoding dan gunakan Content Security Policy.',
                            'payload_used': payload,
                            'field': field
                        })
                        break
                    
                    time.sleep(0.5)
                    
    except Exception:
        pass
    
    return vulnerabilities

def check_sensitive_files(url):
    """Check for exposed sensitive files"""
    vulnerabilities = []
    session = get_session()
    base_url = url.rstrip('/')
    
    for file_path in SENSITIVE_FILES:
        try:
            test_url = f"{base_url}/{file_path}"
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            
            response = safe_request(session, 'GET', test_url, headers=headers)
            
            if response and response.status_code == 200:
                content = response.text.lower()
                
                sensitive_keywords = ['password', 'secret', 'api_key', 'database', 'mysql']
                if any(keyword in content for keyword in sensitive_keywords):
                    vulnerabilities.append({
                        'category': 'Information Disclosure',
                        'name': f'Exposed Sensitive File: {file_path}',
                        'severity': 'Critical',
                        'description': f'File sensitif "{file_path}" dapat diakses secara publik.',
                        'how': 'Hacker dapat memperoleh kredensial atau informasi sistem.',
                        'mitigation': f'Pindahkan file "{file_path}" ke luar document root.',
                        'url': test_url
                    })
                    
        except Exception:
            continue
        
        time.sleep(0.3)
    
    return vulnerabilities

def check_command_injection(url):
    """Check for command injection vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = safe_request(session, 'GET', url, headers=headers)
        if not response:
            return vulnerabilities
            
        soup = BeautifulSoup(response.content, 'html.parser')
        forms = soup.find_all('form')
        
        for form in forms:
            action = form.get('action', url)
            if action and not action.startswith('http'):
                action = urljoin(url, action)
            
            method = form.get('method', 'get').lower()
            inputs = form.find_all(['input', 'textarea'])
            
            form_data = {}
            for inp in inputs:
                name = inp.get('name')
                if name and inp.get('type') not in ['submit', 'button', 'reset', 'hidden']:
                    form_data[name] = 'test'
            
            for field in form_data:
                for payload in COMMAND_PAYLOADS[:2]:
                    test_data = form_data.copy()
                    test_data[field] = payload
                    
                    if method == 'post':
                        response = safe_request(session, 'POST', action, data=test_data, headers=headers)
                    else:
                        response = safe_request(session, 'GET', action, params=test_data, headers=headers)
                    
                    if response:
                        cmd_indicators = ['root:', 'uid=', 'Directory of', 'Volume Serial Number']
                        if any(indicator in response.text for indicator in cmd_indicators):
                            vulnerabilities.append({
                                'category': 'Command Injection',
                                'name': f'Command Injection - Field: {field}',
                                'severity': 'Critical',
                                'description': f'Field "{field}" rentan terhadap command injection.',
                                'how': 'Hacker dapat menjalankan command sistem operasi.',
                                'mitigation': 'Hindari eksekusi command dengan input user.',
                                'payload_used': payload,
                                'field': field
                            })
                            break
                    
                    time.sleep(0.5)
                    
    except Exception:
        pass
    
    return vulnerabilities

def check_directory_listing(url):
    """Check for directory listing"""
    vulnerabilities = []
    try:
        session = get_session()
        test_paths = ['/admin/', '/backup/', '/uploads/']
        
        for path in test_paths:
            test_url = url.rstrip('/') + path
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            
            response = safe_request(session, 'GET', test_url, headers=headers)
            
            if response and response.status_code == 200 and 'Index of' in response.text:
                vulnerabilities.append({
                    'category': 'Directory Listing',
                    'name': f'Directory Listing Enabled: {path}',
                    'severity': 'Medium',
                    'description': f'Directory listing diaktifkan pada {path}',
                    'how': 'Hacker dapat melihat struktur direktori dan file.',
                    'mitigation': 'Nonaktifkan directory listing di web server.'
                })
                
    except Exception:
        pass
    
    return vulnerabilities

def check_vulnerabilities(url):
    """Main function untuk cek semua kerentanan"""
    all_vulnerabilities = []
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        all_vulnerabilities.extend(check_headers(url))
        all_vulnerabilities.extend(check_ssl_certificate(url))
        all_vulnerabilities.extend(check_sql_injection(url))
        all_vulnerabilities.extend(check_xss_vulnerabilities(url))
        all_vulnerabilities.extend(check_sensitive_files(url))
        all_vulnerabilities.extend(check_command_injection(url))
        all_vulnerabilities.extend(check_directory_listing(url))
    except Exception:
        pass
    
    return all_vulnerabilities

@app.route('/', methods=['GET', 'POST'])
def index():
    vulnerabilities = []
    url = ''
    scan_summary = {}
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            try:
                vulnerabilities = check_vulnerabilities(url)
                
                scan_summary = {
                    'total': len(vulnerabilities),
                    'critical': len([v for v in vulnerabilities if v.get('severity') == 'Critical']),
                    'high': len([v for v in vulnerabilities if v.get('severity') == 'High']),
                    'medium': len([v for v in vulnerabilities if v.get('severity') == 'Medium']),
                    'low': len([v for v in vulnerabilities if v.get('severity') == 'Low'])
                }
            except Exception:
                pass
    
    return render_template('index.html', 
                         vulnerabilities=vulnerabilities, 
                         url=url, 
                         scan_summary=scan_summary)

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """API endpoint untuk scanning"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip() if data else ''
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        vulnerabilities = check_vulnerabilities(url)
        
        return jsonify({
            'url': url,
            'vulnerabilities': vulnerabilities,
            'summary': {
                'total': len(vulnerabilities),
                'critical': len([v for v in vulnerabilities if v.get('severity') == 'Critical']),
                'high': len([v for v in vulnerabilities if v.get('severity') == 'High']),
                'medium': len([v for v in vulnerabilities if v.get('severity') == 'Medium']),
                'low': len([v for v in vulnerabilities if v.get('severity') == 'Low'])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    try:
        print("=" * 60)
        print("🛡️  Security Scanner Starting...")
        print("📍 Server will be available at: http://localhost:5000")
        print("⚠️  Use responsibly - only scan websites you own!")
        print("🌐 Opening browser...")
        print("=" * 60)
        
        # Start browser in background thread
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start Flask server
        app.run(debug=False, host='127.0.0.1', port=5000, threaded=True, use_reloader=False)
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        if getattr(sys, 'frozen', False):
            # Only pause in executable mode
            input("Press Enter to exit...")
        sys.exit(1)
