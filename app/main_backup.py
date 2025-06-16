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
from datetime import datetime

# Suppress SSL warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')
warnings.filterwarnings('ignore', category=requests.packages.urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'security-scanner-secret-key-2025'

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
        
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None

# User agents untuk menghindari deteksi
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

def check_ssl_certificate(url):
    """Cek sertifikat SSL"""
    vulnerabilities = []
    try:
        hostname = urlparse(url).hostname
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()                # Cek masa berlaku sertifikat
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
    except ssl.SSLError:
        vulnerabilities.append({
            'category': 'SSL/TLS',
            'name': 'SSL Configuration Error',
            'severity': 'High',
            'description': 'Konfigurasi SSL tidak valid atau menggunakan protokol yang lemah.',
            'how': 'Hacker dapat melakukan downgrade attack atau mengeksploitasi kelemahan protokol.',
            'mitigation': 'Konfigurasi ulang SSL dengan protokol TLS 1.2 atau yang lebih baru.'
        })
    except:
        pass
    
    return vulnerabilities

def check_headers(url):
    """Cek security headers"""
    vulnerabilities = []
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        headers = resp.headers
        
        security_headers = {
            'X-Frame-Options': {
                'name': 'Clickjacking Protection',
                'description': 'Header X-Frame-Options tidak ditemukan. Website rentan terhadap clickjacking.',
                'how': 'Hacker dapat membuat website palsu yang menampilkan website Anda dalam iframe tersembunyi, lalu menipu user untuk melakukan klik pada elemen yang tidak terlihat.',
                'mitigation': 'Tambahkan header "X-Frame-Options: DENY" atau "X-Frame-Options: SAMEORIGIN"'
            },
            'Content-Security-Policy': {
                'name': 'Cross-Site Scripting (XSS) Protection',
                'description': 'Header Content-Security-Policy tidak ditemukan. Website rentan terhadap serangan XSS.',
                'how': 'Hacker dapat menyisipkan script JavaScript berbahaya yang akan dieksekusi di browser user, mencuri cookie, session, atau data sensitif lainnya.',
                'mitigation': 'Implementasikan Content Security Policy yang ketat untuk membatasi sumber script dan resource.'
            },
            'Strict-Transport-Security': {
                'name': 'HTTPS Downgrade Attack',
                'description': 'Header Strict-Transport-Security tidak ditemukan. Website rentan terhadap downgrade attack.',
                'how': 'Hacker dapat memaksa user mengakses website melalui HTTP yang tidak terenkripsi, sehingga dapat menyadap data yang dikirim.',
                'mitigation': 'Tambahkan header "Strict-Transport-Security: max-age=31536000; includeSubDomains"'
            },
            'X-Content-Type-Options': {
                'name': 'MIME Type Sniffing',
                'description': 'Header X-Content-Type-Options tidak ditemukan. Browser dapat melakukan MIME sniffing.',
                'how': 'Hacker dapat mengunggah file berbahaya yang akan diinterpretasikan browser sebagai script executable.',
                'mitigation': 'Tambahkan header "X-Content-Type-Options: nosniff"'
            },
            'Referrer-Policy': {
                'name': 'Information Leakage via Referrer',
                'description': 'Header Referrer-Policy tidak ditemukan. URL sensitif dapat bocor melalui referrer.',
                'how': 'Informasi sensitif dalam URL dapat bocor ke website lain melalui header referrer.',
                'mitigation': 'Tambahkan header "Referrer-Policy: strict-origin-when-cross-origin"'
            },
            'Permissions-Policy': {
                'name': 'Browser Feature Policy',
                'description': 'Header Permissions-Policy tidak ditemukan. Browser feature tidak dibatasi.',
                'how': 'Script berbahaya dapat mengakses fitur browser seperti kamera, mikrofon, geolocation tanpa kontrol.',
                'mitigation': 'Implementasikan Permissions-Policy untuk membatasi akses ke fitur browser.'
            }
        }
        
        for header, info in security_headers.items():
            if header not in headers:
                vulnerabilities.append({
                    'category': 'Security Headers',
                    'name': info['name'],
                    'severity': 'Medium' if header in ['Referrer-Policy', 'Permissions-Policy'] else 'High',
                    'description': info['description'],
                    'how': info['how'],
                    'mitigation': info['mitigation']
                })
        
        # Cek server information disclosure
        if 'Server' in headers:
            server_info = headers['Server']
            if any(keyword in server_info.lower() for keyword in ['apache', 'nginx', 'iis', 'tomcat']):
                vulnerabilities.append({
                    'category': 'Information Disclosure',
                    'name': 'Server Information Disclosure',
                    'severity': 'Low',
                    'description': f'Server mengungkapkan informasi: {server_info}',
                    'how': 'Informasi server dapat digunakan hacker untuk mencari exploit spesifik untuk versi software yang digunakan.',
                    'mitigation': 'Sembunyikan atau ubah header Server untuk tidak mengungkapkan informasi versi.'
                })
                
    except requests.RequestException as e:
        vulnerabilities.append({
            'category': 'Connection',
            'name': 'Connection Error', 
            'severity': 'Critical',
            'description': f'Gagal mengakses {url}: {str(e)}',
            'how': 'Website tidak dapat diakses, mungkin down atau memblokir request.',
            'mitigation': 'Periksa status server dan konfigurasi firewall.'
        })
    
    return vulnerabilities

def check_forms_and_inputs(url):
    """Cek potensi kerentanan pada form"""
    vulnerabilities = []
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Cek form tanpa CSRF protection
        forms = soup.find_all('form')
        for form in forms:
            csrf_found = False
            inputs = form.find_all('input')
            for inp in inputs:
                if inp.get('name') and 'csrf' in inp.get('name').lower():
                    csrf_found = True
                    break
            
            if not csrf_found and form.get('method', '').lower() == 'post':
                vulnerabilities.append({
                    'category': 'Form Security',
                    'name': 'Missing CSRF Protection',
                    'severity': 'High',
                    'description': 'Ditemukan form POST tanpa perlindungan CSRF token.',
                    'how': 'Hacker dapat membuat website yang mengirim request POST ke form Anda atas nama user yang sedang login, melakukan aksi yang tidak diinginkan.',
                    'mitigation': 'Implementasikan CSRF token pada semua form yang mengubah data.'
                })
        
        # Cek input field yang mungkin rentan XSS
        inputs = soup.find_all(['input', 'textarea'])
        for inp in inputs:
            input_type = inp.get('type', 'text')
            if input_type in ['text', 'search', 'url', 'email'] or inp.name == 'textarea':
                vulnerabilities.append({
                    'category': 'Input Validation',
                    'name': 'Potential XSS via Input Fields',
                    'severity': 'Medium',
                    'description': 'Ditemukan input field yang berpotensi rentan terhadap XSS jika tidak ada validasi.',
                    'how': 'Hacker dapat memasukkan script JavaScript melalui input field yang kemudian akan dieksekusi ketika data ditampilkan kembali.',
                    'mitigation': 'Implementasikan input validation dan output encoding yang proper.'
                })
                break
                
    except Exception as e:
        pass
    
    return vulnerabilities

def check_directory_listing(url):
    """Cek directory listing"""
    vulnerabilities = []
    try:
        test_paths = ['/admin/', '/backup/', '/test/', '/temp/', '/uploads/', '/files/']
        for path in test_paths:
            test_url = url.rstrip('/') + path
            resp = requests.get(test_url, timeout=5)
            if resp.status_code == 200 and 'Index of' in resp.text:
                vulnerabilities.append({
                    'category': 'Directory Listing',
                    'name': f'Directory Listing Enabled: {path}',
                    'severity': 'Medium',
                    'description': f'Directory listing diaktifkan pada {path}',
                    'how': 'Hacker dapat melihat struktur direktori dan file-file yang ada, berpotensi menemukan file sensitif atau backup.',
                    'mitigation': 'Nonaktifkan directory listing di web server atau tambahkan file index.html kosong.'
                })
    except:
        pass
    
    return vulnerabilities

# Payload untuk testing berbagai kerentanan
SQL_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR 'a'='a",
    "admin'--",
    "' UNION SELECT NULL--",
    "'; DROP TABLE users--",
    "1' OR '1'='1' /*",
    "' OR 1=1#",
    "' OR 1=1;--",
    "1' AND '1'='1",
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "javascript:alert('XSS')",
    "<body onload=alert('XSS')>",
    "'><script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "<script>console.log('XSS')</script>",
    "<iframe src='javascript:alert(\"XSS\")'></iframe>",
    "<input onfocus=alert('XSS') autofocus>"
]

# File sensitif yang sering terekspos
SENSITIVE_FILES = [
    '.env',
    '.git/config',
    '.git/HEAD',
    'config.php',
    'wp-config.php',
    'database.yml',
    'settings.py',
    'web.config',
    '.htaccess',
    'robots.txt',
    'sitemap.xml',
    'admin/',
    'administrator/',
    'phpmyadmin/',
    'backup/',
    'backup.sql',
    'dump.sql',
    'users.txt',
    'passwords.txt',
    '.DS_Store'
]

# Error messages yang mengindikasikan SQL Injection
SQL_ERROR_PATTERNS = [
    r"SQL syntax.*MySQL",
    r"Warning.*mysql_.*",
    r"valid MySQL result",
    r"MySqlClient\.",
    r"PostgreSQL.*ERROR",
    r"Warning.*\Wpg_.*",
    r"valid PostgreSQL result",
    r"Npgsql\.",
    r"Driver.* SQL.*",
    r"OLE DB.* SQL",
    r"(\W|\A)SQL Server.*Driver",
    r"Warning.*mssql_.*",
    r"ODBC.* SQL.*",
    r"Microsoft.* ODBC.* SQL",
    r"ORA-\d{4,5}",
    r"Oracle.* JDBC.*",
    r"Oracle.*Driver",
    r"Warning.*\Woci_.*",
    r"Warning.*\Wora_.*"
]

def check_sql_injection(url):
    """Test SQL Injection vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    try:
        # Get original response
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        original_response = session.get(url, headers=headers, timeout=10, verify=False)
        
        # Parse URL dan form
        soup = BeautifulSoup(original_response.content, 'html.parser')
        forms = soup.find_all('form')
        
        # Test forms with POST method
        for form in forms:
            if form.get('method', '').lower() == 'post':
                action = form.get('action', '')
                if action:
                    if not action.startswith('http'):
                        action = urljoin(url, action)
                else:
                    action = url
                
                # Get all input fields
                inputs = form.find_all(['input', 'textarea', 'select'])
                form_data = {}
                
                for inp in inputs:
                    name = inp.get('name')
                    if name and inp.get('type') not in ['submit', 'button', 'reset']:
                        form_data[name] = 'test'
                
                # Test each payload
                for payload in SQL_PAYLOADS[:3]:  # Limit payloads untuk menghindari spam
                    test_data = form_data.copy()
                    
                    # Inject payload into each field
                    for field in test_data:
                        test_data[field] = payload
                        
                        try:
                            response = session.post(action, data=test_data, headers=headers, timeout=10, verify=False)
                            
                            # Check for SQL error patterns
                            for pattern in SQL_ERROR_PATTERNS:
                                if re.search(pattern, response.text, re.IGNORECASE):
                                    vulnerabilities.append({
                                        'category': 'SQL Injection',
                                        'name': f'SQL Injection Vulnerability - Field: {field}',
                                        'severity': 'Critical',
                                        'description': f'Field "{field}" rentan terhadap SQL Injection. Ditemukan error database yang mengindikasikan kerentanan.',
                                        'how': f'Hacker dapat memasukkan payload seperti "{payload}" untuk mengakses atau memanipulasi database. Ini dapat menyebabkan pencurian data, bypass autentikasi, atau penghapusan data.',
                                        'mitigation': 'Gunakan prepared statements/parameterized queries, validasi input yang ketat, dan principle of least privilege untuk database user.',
                                        'payload_used': payload,
                                        'field': field
                                    })
                                    break
                        except:
                            continue
                        
                        # Reset field value
                        test_data[field] = 'test'
                        time.sleep(0.5)  # Rate limiting
        
        # Test GET parameters
        parsed_url = urlparse(url)
        if parsed_url.query:
            params = parse_qs(parsed_url.query)
            
            for param_name in params:
                for payload in SQL_PAYLOADS[:2]:  # Test fewer payloads for GET
                    test_params = params.copy()
                    test_params[param_name] = [payload]
                    
                    # Rebuild URL with malicious parameter
                    new_query = '&'.join([f"{k}={v[0]}" for k, v in test_params.items()])
                    test_url = urlunparse((
                        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                        parsed_url.params, new_query, parsed_url.fragment
                    ))
                    
                    try:
                        response = session.get(test_url, headers=headers, timeout=10, verify=False)
                        
                        # Check for SQL error patterns
                        for pattern in SQL_ERROR_PATTERNS:
                            if re.search(pattern, response.text, re.IGNORECASE):
                                vulnerabilities.append({
                                    'category': 'SQL Injection',
                                    'name': f'SQL Injection via GET Parameter: {param_name}',
                                    'severity': 'Critical',
                                    'description': f'Parameter GET "{param_name}" rentan terhadap SQL Injection.',
                                    'how': f'Hacker dapat memodifikasi URL dengan payload SQL untuk mengakses database secara tidak sah.',
                                    'mitigation': 'Validasi dan sanitasi semua input GET parameter, gunakan whitelist validation.',
                                    'payload_used': payload,
                                    'parameter': param_name
                                })
                                break
                    except:
                        continue
                    
                    time.sleep(0.5)
                    
    except Exception as e:
        pass
    
    return vulnerabilities

def check_xss_vulnerabilities(url):
    """Test Cross-Site Scripting vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = session.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Test forms for XSS
        forms = soup.find_all('form')
        
        for form in forms:
            action = form.get('action', '')
            if action:
                if not action.startswith('http'):
                    action = urljoin(url, action)
            else:
                action = url
            
            method = form.get('method', 'get').lower()
            inputs = form.find_all(['input', 'textarea'])
            
            form_data = {}
            text_inputs = []
            
            for inp in inputs:
                name = inp.get('name')
                input_type = inp.get('type', 'text')
                
                if name and input_type not in ['submit', 'button', 'reset', 'hidden']:
                    if input_type in ['text', 'email', 'search', 'url'] or inp.name == 'textarea':
                        text_inputs.append(name)
                        form_data[name] = 'test'
                    else:
                        form_data[name] = 'test'
            
            # Test XSS payloads on text inputs
            for field in text_inputs:
                for payload in XSS_PAYLOADS[:3]:  # Limit payloads
                    test_data = form_data.copy()
                    test_data[field] = payload
                    
                    try:
                        if method == 'post':
                            response = session.post(action, data=test_data, headers=headers, timeout=10, verify=False)
                        else:
                            response = session.get(action, params=test_data, headers=headers, timeout=10, verify=False)
                        
                        # Check if payload is reflected in response
                        if payload in response.text or payload.replace("'", "&#x27;") in response.text:
                            vulnerabilities.append({
                                'category': 'Cross-Site Scripting (XSS)',
                                'name': f'Reflected XSS - Field: {field}',
                                'severity': 'High',
                                'description': f'Field "{field}" rentan terhadap Reflected XSS. Input user direfleksikan dalam response tanpa sanitasi.',
                                'how': f'Hacker dapat mengirim link berbahaya yang berisi script JavaScript. Ketika korban mengklik link tersebut, script akan dieksekusi di browser korban dan dapat mencuri cookie, session, atau melakukan aksi atas nama korban.',
                                'mitigation': 'Lakukan HTML encoding/escaping pada semua output user, gunakan Content Security Policy (CSP), validasi input secara ketat.',
                                'payload_used': payload,
                                'field': field
                            })
                            break
                    except:
                        continue
                    
                    time.sleep(0.5)
        
        # Check for stored XSS indicators (basic check)
        if any(pattern in response.text.lower() for pattern in ['<script', 'javascript:', 'onerror=', 'onload=']):
            # Additional check for unescaped user content
            suspicious_patterns = [
                r'<script[^>]*>.*?</script>',
                r'on\w+\s*=\s*["\'][^"\']*["\']',
                r'javascript:\s*\w+'
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, response.text, re.IGNORECASE):
                    vulnerabilities.append({
                        'category': 'Cross-Site Scripting (XSS)',
                        'name': 'Potential Stored XSS',
                        'severity': 'High',
                        'description': 'Ditemukan indikasi kemungkinan Stored XSS. Terdapat script atau event handler yang tidak ter-escape dengan baik.',
                        'how': 'Jika aplikasi menyimpan dan menampilkan user input tanpa sanitasi, hacker dapat menyimpan script berbahaya yang akan dieksekusi setiap kali halaman dimuat oleh user lain.',
                        'mitigation': 'Implementasikan output encoding, Content Security Policy, dan validasi input yang ketat pada sisi server.',
                        'pattern_found': pattern
                    })
                    break
                    
    except Exception as e:
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
            
            response = session.get(test_url, headers=headers, timeout=8, verify=False)
            
            # Check if file exists and contains sensitive content
            if response.status_code == 200:
                content = response.text.lower()
                
                # Define sensitive content patterns
                sensitive_patterns = {
                    '.env': ['db_password', 'api_key', 'secret', 'password='],
                    '.git/config': ['[remote', 'url =', '.git'],
                    'config.php': ['password', 'database', 'mysql'],
                    'wp-config.php': ['db_password', 'wp_', 'mysql'],
                    'web.config': ['connectionstring', 'password', 'appSettings'],
                    'backup.sql': ['insert into', 'create table', 'mysql'],
                    'dump.sql': ['insert into', 'create table', 'database'],
                    'admin/': ['login', 'username', 'password', 'admin'],
                    'phpmyadmin/': ['phpmyadmin', 'mysql', 'database']
                }
                
                # Check if content matches sensitive patterns
                is_sensitive = False
                for pattern_file, patterns in sensitive_patterns.items():
                    if pattern_file in file_path.lower():
                        if any(pattern in content for pattern in patterns):
                            is_sensitive = True
                            break
                
                # Default check for any suspicious content
                if not is_sensitive and any(keyword in content for keyword in ['password', 'secret', 'api_key', 'database']):
                    is_sensitive = True
                
                if is_sensitive or file_path in ['.htaccess', '.DS_Store', 'robots.txt']:
                    severity = 'Critical' if file_path in ['.env', 'config.php', 'wp-config.php', 'backup.sql', 'dump.sql'] else 'High'
                    
                    vulnerabilities.append({
                        'category': 'Information Disclosure',
                        'name': f'Exposed Sensitive File: {file_path}',
                        'severity': severity,
                        'description': f'File sensitif "{file_path}" dapat diakses secara publik dan berpotensi mengandung informasi rahasia.',
                        'how': f'Hacker dapat mengakses file ini langsung melalui browser dan memperoleh informasi seperti kredensial database, API keys, atau konfigurasi sistem yang dapat digunakan untuk serangan lebih lanjut.',
                        'mitigation': f'Pindahkan file "{file_path}" ke luar document root, atau blokir akses menggunakan .htaccess/web server configuration. Jangan pernah menyimpan file sensitif di direktori yang dapat diakses publik.',
                        'url': test_url,
                        'file_size': len(response.content)
                    })
                    
        except:
            continue
        
        time.sleep(0.3)  # Rate limiting
    
    return vulnerabilities

def check_directory_traversal(url):
    """Check for directory traversal vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    # Directory traversal payloads
    traversal_payloads = [
        '../../../etc/passwd',
        '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts',
        '....//....//....//etc/passwd',
        '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
        '..%252f..%252f..%252fetc%252fpasswd'
    ]
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = session.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for file parameter in URL
        parsed_url = urlparse(url)
        if parsed_url.query:
            params = parse_qs(parsed_url.query)
            
            for param_name in params:
                if any(keyword in param_name.lower() for keyword in ['file', 'path', 'page', 'include', 'doc']):
                    for payload in traversal_payloads[:2]:
                        test_params = params.copy()
                        test_params[param_name] = [payload]
                        
                        new_query = '&'.join([f"{k}={v[0]}" for k, v in test_params.items()])
                        test_url = urlunparse((
                            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                            parsed_url.params, new_query, parsed_url.fragment
                        ))
                        
                        try:
                            response = session.get(test_url, headers=headers, timeout=10, verify=False)
                            
                            # Check for typical file content
                            if ('root:' in response.text and '/bin/' in response.text) or \
                               ('localhost' in response.text and '127.0.0.1' in response.text):
                                vulnerabilities.append({
                                    'category': 'Directory Traversal',
                                    'name': f'Directory Traversal via Parameter: {param_name}',
                                    'severity': 'Critical',
                                    'description': f'Parameter "{param_name}" rentan terhadap directory traversal attack.',
                                    'how': 'Hacker dapat mengakses file sistem operasi dengan menggunakan payload traversal seperti "../../../etc/passwd" untuk membaca file sensitif server.',
                                    'mitigation': 'Validasi dan sanitasi input parameter file, gunakan whitelist path yang diizinkan, implementasikan proper access control.',
                                    'payload_used': payload,
                                    'parameter': param_name
                                })
                                break
                        except:
                            continue
                        
                        time.sleep(0.5)
                        
    except Exception as e:
        pass
    
    return vulnerabilities

def check_command_injection(url):
    """Check for command injection vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    # Command injection payloads
    cmd_payloads = [
        '; cat /etc/passwd',
        '| whoami',
        '& dir',
        '`id`',
        '$(whoami)',
        '; ls -la',
        '| net user',
        '& echo vulnerable',
        '; ping -c 1 127.0.0.1',
        '`ping -c 1 127.0.0.1`'
    ]
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = session.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Test forms
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action', '')
            if action:
                if not action.startswith('http'):
                    action = urljoin(url, action)
            else:
                action = url
            
            method = form.get('method', 'get').lower()
            inputs = form.find_all(['input', 'textarea'])
            
            form_data = {}
            for inp in inputs:
                name = inp.get('name')
                input_type = inp.get('type', 'text')
                if name and input_type not in ['submit', 'button', 'reset', 'hidden']:
                    form_data[name] = 'test'
            
            # Test command injection
            for field in form_data:
                for payload in cmd_payloads[:3]:  # Limit payloads
                    test_data = form_data.copy()
                    test_data[field] = payload
                    
                    try:
                        if method == 'post':
                            response = session.post(action, data=test_data, headers=headers, timeout=15, verify=False)
                        else:
                            response = session.get(action, params=test_data, headers=headers, timeout=15, verify=False)
                        
                        # Check for command execution indicators
                        cmd_indicators = [
                            'root:', 'uid=', 'gid=', '/bin/', '/usr/',  # Unix/Linux
                            'Volume Serial Number', 'Directory of', 'Users\\',  # Windows
                            'vulnerable',  # Our test echo
                            'ping statistics', 'packets transmitted'  # Ping command
                        ]
                        
                        if any(indicator in response.text for indicator in cmd_indicators):
                            vulnerabilities.append({
                                'category': 'Command Injection',
                                'name': f'Command Injection - Field: {field}',
                                'severity': 'Critical',
                                'description': f'Field "{field}" rentan terhadap command injection. Server mengeksekusi command sistem.',
                                'how': f'Hacker dapat menjalankan command sistem operasi dengan payload seperti "{payload}". Ini memungkinkan akses penuh ke server, pencurian data, atau perusakan sistem.',
                                'mitigation': 'Hindari eksekusi command sistem dengan input user. Jika diperlukan, gunakan whitelist command yang diizinkan dan sanitasi input ketat.',
                                'payload_used': payload,
                                'field': field
                            })
                            break
                    except:
                        continue
                    
                    time.sleep(0.5)
                    
    except Exception as e:
        pass
    
    return vulnerabilities

def check_file_upload_vulnerabilities(url):
    """Check for file upload vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    try:
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        response = session.get(url, headers=headers, timeout=10, verify=False)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for file upload forms
        file_inputs = soup.find_all('input', {'type': 'file'})
        
        if file_inputs:
            for file_input in file_inputs:
                form = file_input.find_parent('form')
                if form:
                    vulnerabilities.append({
                        'category': 'File Upload',
                        'name': 'File Upload Form Detected',
                        'severity': 'Medium',
                        'description': 'Ditemukan form upload file. Perlu dilakukan testing manual untuk memastikan keamanan.',
                        'how': 'Hacker dapat mengunggah file berbahaya seperti web shell (PHP, ASP, JSP) yang dapat memberikan akses kontrol penuh ke server. File berbahaya juga dapat mengandung malware atau script untuk menyerang pengunjung lain.',
                        'mitigation': 'Implementasikan validasi file type, batasi ekstensi yang diizinkan, scan file untuk malware, simpan file di luar web root, dan gunakan proper access control.',
                        'input_name': file_input.get('name', 'unknown'),
                        'form_action': form.get('action', 'current_page')
                    })
    except:
        pass
    
    return vulnerabilities

def check_open_redirect(url):
    """Check for open redirect vulnerabilities"""
    vulnerabilities = []
    session = get_session()
    
    redirect_params = ['redirect', 'url', 'next', 'return', 'continue', 'goto', 'target']
    test_urls = ['http://evil.com', 'https://malicious.site', '//attacker.com']
    
    try:
        parsed_url = urlparse(url)
        if parsed_url.query:
            params = parse_qs(parsed_url.query)
            
            for param_name in params:
                if any(redirect_param in param_name.lower() for redirect_param in redirect_params):
                    for test_url in test_urls[:1]:  # Test one malicious URL
                        test_params = params.copy()
                        test_params[param_name] = [test_url]
                        
                        new_query = '&'.join([f"{k}={v[0]}" for k, v in test_params.items()])
                        test_request_url = urlunparse((
                            parsed_url.scheme, parsed_url.netloc, parsed_url.path,
                            parsed_url.params, new_query, parsed_url.fragment
                        ))
                        
                        try:
                            headers = {'User-Agent': random.choice(USER_AGENTS)}
                            response = session.get(test_request_url, headers=headers, timeout=10, allow_redirects=False, verify=False)
                            
                            # Check if redirected to external URL
                            if response.status_code in [301, 302, 303, 307, 308]:
                                location = response.headers.get('Location', '')
                                if test_url in location or location.startswith('//'):
                                    vulnerabilities.append({
                                        'category': 'Open Redirect',
                                        'name': f'Open Redirect via Parameter: {param_name}',
                                        'severity': 'Medium',
                                        'description': f'Parameter "{param_name}" dapat digunakan untuk redirect ke URL eksternal.',
                                        'how': 'Hacker dapat membuat link yang tampak legitimate tapi mengarahkan korban ke website berbahaya. Ini sering digunakan untuk phishing atau menyebarkan malware.',
                                        'mitigation': 'Validasi destination URL dengan whitelist domain yang diizinkan, atau gunakan indirect redirect dengan mapping internal.',
                                        'parameter': param_name,
                                        'redirect_to': location
                                    })
                                    break
                        except:
                            continue
                        
                        time.sleep(0.5)
                        
    except Exception as e:
        pass
    
    return vulnerabilities

def check_vulnerabilities(url):
    """Main function untuk cek semua kerentanan"""
    all_vulnerabilities = []
    
    # Pastikan URL memiliki protocol
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
      # Cek berbagai jenis kerentanan
    print("Checking security headers...")
    all_vulnerabilities.extend(check_headers(url))
    
    print("Checking SSL certificate...")
    all_vulnerabilities.extend(check_ssl_certificate(url))
    
    print("Checking for SQL Injection...")
    all_vulnerabilities.extend(check_sql_injection(url))
    
    print("Checking for XSS vulnerabilities...")
    all_vulnerabilities.extend(check_xss_vulnerabilities(url))
    
    print("Checking for Command Injection...")
    all_vulnerabilities.extend(check_command_injection(url))
    
    print("Checking for sensitive files...")
    all_vulnerabilities.extend(check_sensitive_files(url))
    
    print("Checking for directory traversal...")
    all_vulnerabilities.extend(check_directory_traversal(url))
    
    print("Checking file upload vulnerabilities...")
    all_vulnerabilities.extend(check_file_upload_vulnerabilities(url))
    
    print("Checking for open redirect...")
    all_vulnerabilities.extend(check_open_redirect(url))
    
    print("Checking forms and inputs...")
    all_vulnerabilities.extend(check_forms_and_inputs(url))
    
    print("Checking directory listing...")
    all_vulnerabilities.extend(check_directory_listing(url))
    all_vulnerabilities.extend(check_command_injection(url))
    all_vulnerabilities.extend(check_file_upload_vulnerabilities(url))
    all_vulnerabilities.extend(check_open_redirect(url))
    
    return all_vulnerabilities

@app.route('/', methods=['GET', 'POST'])
def index():
    vulnerabilities = []
    url = ''
    scan_summary = {}
    
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            vulnerabilities = check_vulnerabilities(url)
            
            # Buat summary
            scan_summary = {
                'total': len(vulnerabilities),
                'critical': len([v for v in vulnerabilities if v.get('severity') == 'Critical']),
                'high': len([v for v in vulnerabilities if v.get('severity') == 'High']),
                'medium': len([v for v in vulnerabilities if v.get('severity') == 'Medium']),
                'low': len([v for v in vulnerabilities if v.get('severity') == 'Low'])
            }
    
    return render_template('index.html', 
                         vulnerabilities=vulnerabilities, 
                         url=url, 
                         scan_summary=scan_summary)

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """API endpoint untuk scanning"""
    data = request.get_json()
    url = data.get('url', '').strip()
    
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
