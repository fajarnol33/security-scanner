<<<<<<< HEAD
# 🛡️ Security Scanner - Website Vulnerability Assessment Tool

Tool komprehensif untuk analisis kerentanan website dengan tujuan **edukasi keamanan siber**. Mengimplementasikan berbagai teknik penetration testing untuk mendeteksi kerentanan umum pada aplikasi web.

## 🚀 Quick Start

### 🌟 Option 1: GitHub Actions Build (RECOMMENDED)
**No Python installation needed! Build EXE in the cloud.**

1. **Upload to GitHub** - Create repository and upload project files
2. **Auto-build** - GitHub Actions will build EXE automatically (3-5 min)
3. **Download EXE** - Get `SecurityScanner.exe` from Artifacts
4. **Double-click** - Run the EXE and browser opens automatically

👶 **New to GitHub?** → [GITHUB_UNTUK_PEMULA.md](GITHUB_UNTUK_PEMULA.md)  
⚡ **Quick Guide** → [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)

### 💻 Option 2: Local Python Installation
```bash
# 1. Install Python (jika belum ada)
# Download dari: https://python.org/downloads/
# PENTING: Centang "Add Python to PATH"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
python app/main.py

# 4. Akses di browser
# http://localhost:5000
```

### 🔨 Option 3: Build Your Own EXE
```bash
# Install build dependencies
pip install -r requirements-build.txt

# Build EXE
python build_exe.py
# atau
pyinstaller SecurityScanner.spec
```

**📚 All Build Methods:** [ALL_BUILD_METHODS.md](ALL_BUILD_METHODS.md)

## 🔍 Fitur Deteksi Kerentanan

### 🔴 Critical Vulnerabilities
- **SQL Injection**: Testing dengan payload `' OR 1=1--`, `admin'--`, `UNION SELECT`
- **Command Injection**: Eksekusi system command via `; cat /etc/passwd`, `| whoami`
- **Directory Traversal**: Akses file sistem dengan `../../../etc/passwd`

### 🟠 High Risk Vulnerabilities  
- **Cross-Site Scripting (XSS)**: Reflected & Stored XSS detection
- **Sensitive File Exposure**: `.env`, `config.php`, `backup.sql`, `.git/config`
- **Authentication Bypass**: SQL injection pada login forms

### 🟡 Medium Risk Issues
- **Missing Security Headers**: CSP, X-Frame-Options, HSTS
- **Open Redirect**: URL redirection vulnerabilities
- **CSRF Protection**: Missing CSRF tokens
- **File Upload**: Unrestricted file upload detection

### 🟢 Low Risk & Info Gathering
- **Server Information Disclosure**: Version fingerprinting
- **Directory Listing**: Exposed directories
- **SSL/TLS Issues**: Certificate validation
- **HTTP Methods**: Dangerous methods enabled

## 🎯 Jenis Payload yang Digunakan

### SQL Injection Payloads
```sql
' OR '1'='1
' OR 1=1--
admin'--
' UNION SELECT NULL--
'; DROP TABLE users--
1' AND '1'='1
```

### XSS Testing Payloads
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
javascript:alert('XSS')
<iframe src='javascript:alert("XSS")'></iframe>
```

### Command Injection Payloads
```bash
; cat /etc/passwd
| whoami
& dir
`id`
$(whoami)
; ping -c 1 127.0.0.1
```

### Directory Traversal Payloads
```bash
../../../etc/passwd
..\\..\\..\\windows\\system32\\drivers\\etc\\hosts
%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
....//....//....//etc/passwd
```

## � Build & Deploy Options

### 🌐 GitHub Actions (Cloud Build)
- ✅ **No Python needed** - Build in cloud
- ✅ **Free builds** - 2000 minutes/month
- ✅ **Auto-build** - On every code change
- ✅ **Cross-platform** - Windows, Linux, macOS

**Guides:**
- 👶 [Pemula GitHub](GITHUB_UNTUK_PEMULA.md)
- ⚡ [Quick Start](QUICK_START_GITHUB.md)  
- 📖 [Detailed Guide](CARA_BUILD_GITHUB_ACTIONS.md)
- 🔧 [Troubleshooting](TROUBLESHOOTING_GITHUB_ACTIONS.md)

### 💻 Local Build
- ⚡ **Fast** - 2-3 minutes build time
- 🔧 **Full control** - Customize build process
- 📱 **Offline** - No internet needed

```bash
# Quick build
python build_exe.py

# Manual build  
pyinstaller SecurityScanner.spec
```

### 📱 Portable Version
- 🚀 **No installation** - Runs anywhere
- 📦 **Self-contained** - Includes Python runtime

```bash
python create_portable.py
```

**📚 Compare All Methods:** [ALL_BUILD_METHODS.md](ALL_BUILD_METHODS.md)

## �📊 Output Report

Setiap kerentanan dilaporkan dengan detail:
- **Severity Level**: Critical, High, Medium, Low
- **Kategori**: Jenis serangan (SQL Injection, XSS, dll)
- **Deskripsi**: Penjelasan teknis kerentanan
- **Cara Eksploitasi**: Bagaimana hacker memanfaatkan
- **Payload Used**: Script/command yang digunakan dalam test
- **Affected Parameter**: Field/parameter yang rentan
- **Mitigation**: Cara mengatasi kerentanan

### Contoh Output
```
🚨 CRITICAL - SQL Injection via Parameter: username
Payload: ' OR 1=1--
Description: Parameter dapat di-inject dengan SQL payload
How Hackers Exploit: Bypass authentication, extract database
Mitigation: Use prepared statements, input validation
```

## 🔧 Advanced Configuration

### Custom Payloads
Edit `app/main.py` untuk menambah payload:
```python
SQL_PAYLOADS = [
    "' OR '1'='1",
    # Tambah payload custom
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    # Tambah payload custom
]
```

### Environment Configuration
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export REQUEST_TIMEOUT=15
export MAX_PAYLOAD_TESTS=5
```

### Rate Limiting
Aplikasi otomatis membatasi request untuk menghindari detection:
- Delay 0.5 detik antar request
- Maximum 3 payload per test
- Request timeout 15 detik

## 🌐 API Usage

REST API endpoint tersedia untuk integrasi:

```bash
# POST /api/scan
curl -X POST http://localhost:5000/api/scan \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Response:
```json
{
  "url": "https://example.com",
  "vulnerabilities": [...],
  "summary": {
    "total": 5,
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 1
  }
}
```

## 📋 System Requirements

- **Python**: 3.7+ (3.11+ recommended)
- **OS**: Windows, Linux, macOS
- **Memory**: 512MB RAM minimum
- **Network**: Internet connection for target scanning
- **Dependencies**: Flask, Requests, BeautifulSoup4

## 🚨 Legal & Ethical Usage

### ✅ ALLOWED Usage:
- Testing your own websites
- Educational purposes & learning
- Authorized penetration testing
- Security awareness training
- Research in controlled environments

### ❌ PROHIBITED Usage:
- Testing websites without permission
- Illegal hacking activities  
- Attacking systems you don't own
- Violating terms of service
- Any malicious activities

### 📜 Disclaimer
This tool is for **educational and defensive security purposes only**. Users are responsible for complying with all applicable laws and regulations. The developers are not responsible for any misuse of this tool.

## � Documentation

### 🚀 Getting Started
- 📋 [README.md](README.md) - Project overview (this file)
- 🎯 [GET_STARTED.md](GET_STARTED.md) - First time setup
- 🎮 [USAGE.md](USAGE.md) - How to use the scanner
- 📊 [EXAMPLE_RESULTS.md](EXAMPLE_RESULTS.md) - Sample scan results

### 🔨 Build Guides
- 🌟 [ALL_BUILD_METHODS.md](ALL_BUILD_METHODS.md) - Compare all build options
- 👶 [GITHUB_UNTUK_PEMULA.md](GITHUB_UNTUK_PEMULA.md) - GitHub for beginners
- ⚡ [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) - Fast GitHub Actions build
- 📖 [CARA_BUILD_GITHUB_ACTIONS.md](CARA_BUILD_GITHUB_ACTIONS.md) - Detailed GitHub Actions guide
- 💻 [BUILD_GUIDE.md](BUILD_GUIDE.md) - Local build instructions
- 🛠️ [SOLUSI_BUILD_EXE.md](SOLUSI_BUILD_EXE.md) - Build troubleshooting

### 🔧 Troubleshooting
- 🆘 [TROUBLESHOOTING_GITHUB_ACTIONS.md](TROUBLESHOOTING_GITHUB_ACTIONS.md) - GitHub Actions issues
- 📱 [INSTALL_PYTHON.md](INSTALL_PYTHON.md) - Python installation guide

### 🌐 GitHub & CI/CD
- 🔄 [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - Advanced GitHub Actions
- 📖 [README_GITHUB.md](README_GITHUB.md) - GitHub repository setup

## �🛠️ Development

### Project Structure
```
cekweb/
├── app/
│   ├── main.py          # Main Flask application
│   ├── logger.py        # Logging utilities
│   └── templates/
│       └── index.html   # Web interface
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── launcher.py         # Smart launcher script
├── test_setup.py       # Setup verification
└── start.bat           # Windows batch launcher
```

### Adding New Vulnerability Tests
1. Create test function in `app/main.py`
2. Add to `check_vulnerabilities()` function
3. Update payload lists if needed
4. Test with known vulnerable applications

### Contributing
1. Fork the repository
2. Create feature branch
3. Add tests for new vulnerabilities
4. Submit pull request with documentation

## 🔗 Educational Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [SANS Web Application Security](https://www.sans.org/cyber-aces/)

## 🆘 Troubleshooting

### Common Issues

**"Python not found"**
- Install Python from https://python.org
- Check "Add Python to PATH" during installation

**"Module not found"**  
```bash
pip install -r requirements.txt
```

**"Port 5000 already in use"**
```bash
# Change port in app/main.py
app.run(host='0.0.0.0', port=8080)
```

**"Connection timeout"**
- Check internet connection
- Target website may be blocking requests
- Try different target or reduce payload count

## 📞 Support

- 📖 Check `USAGE.md` for detailed usage guide
- 🐍 See `INSTALL_PYTHON.md` for Python installation help
- 📋 Review `EXAMPLE_RESULTS.md` for sample outputs
- 🔧 Run `python test_setup.py` for system diagnostics

---

**⚠️ Remember: With great power comes great responsibility. Use this tool ethically and legally!** 🛡️

**🎓 Happy Learning & Stay Secure!** 🚀
