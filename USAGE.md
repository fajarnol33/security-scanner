# Security Scanner - Panduan Penggunaan

## 🎯 Tujuan Tool

Security Scanner ini dirancang untuk **tujuan edukasi keamanan siber** dan membantu developers/security professionals memahami berbagai jenis kerentanan website yang umum ditemukan. Tool ini mengimplementasikan teknik-teknik scanning yang dijelaskan dalam permintaan Anda.

## 🔍 Jenis Serangan yang Diimplementasikan

### 1. SQL Injection Testing
Tool ini mengirimkan berbagai payload SQL Injection seperti:
- `' OR '1'='1`
- `' OR 1=1--`
- `admin'--`
- `' UNION SELECT NULL--`

**Cara Kerja**: Payload dikirim ke form input dan parameter GET, kemudian response dianalisis untuk mencari error message database yang spesifik.

### 2. Cross-Site Scripting (XSS) Testing
Payload XSS yang digunakan:
- `<script>alert('XSS')</script>`
- `<img src=x onerror=alert('XSS')>`
- `<svg onload=alert('XSS')>`

**Cara Kerja**: Payload dikirim melalui form dan parameter, kemudian dicek apakah payload tersebut muncul di response HTML.

### 3. Command Injection Testing
Payload command injection:
- `; cat /etc/passwd`
- `| whoami`
- `& dir`
- `$(whoami)`

**Cara Kerja**: Mencari indikator eksekusi command seperti output sistem atau error message yang spesifik.

### 4. Directory Traversal Testing
Payload traversal:
- `../../../etc/passwd`
- `..\\..\\..\\windows\\system32\\drivers\\etc\\hosts`
- `%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd`

**Cara Kerja**: Mencoba mengakses file sistem melalui parameter yang menangani file.

### 5. Sensitive File Detection
Tool mengecek file-file sensitif seperti:
- `.env`, `.git/config`
- `config.php`, `wp-config.php`
- `backup.sql`, `dump.sql`
- `admin/`, `phpmyadmin/`

**Cara Kerja**: Mengirim request HTTP ke path yang umum berisi file sensitif.

## 🛠️ Fitur Teknis

### HTTP Request Handling
- **Session Management**: Menggunakan requests.Session() dengan retry strategy
- **User-Agent Rotation**: Multiple user agents untuk menghindari deteksi
- **Rate Limiting**: Delay antar request untuk menghindari blocking
- **Timeout Handling**: Timeout yang dapat dikonfigurasi

### Response Analysis
- **Pattern Matching**: Regex untuk mendeteksi error patterns
- **Content Analysis**: BeautifulSoup untuk parsing HTML
- **Status Code Checking**: Analisis HTTP response codes
- **Header Analysis**: Pemeriksaan security headers

### Security Measures
- **Request Limiting**: Membatasi jumlah payload per test
- **Timeout Protection**: Mencegah hanging requests
- **Error Handling**: Graceful handling untuk connection errors

## 📋 Cara Menggunakan

### 1. Instalasi
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Aplikasi
```bash
# Menggunakan script utama
python app/main.py

# Atau menggunakan runner dengan opsi
python run.py --host 127.0.0.1 --port 5000

# Untuk Windows, double-click start.bat
```

### 3. Akses Web Interface
Buka browser dan akses: `http://localhost:5000`

### 4. Input Target
- Masukkan URL website target
- Klik "Scan Website"
- Tunggu proses scanning selesai

## 🎓 Untuk Pembelajaran

### Memahami Payload
Setiap hasil scan menampilkan:
- **Payload yang digunakan**: Script/command yang dikirim
- **Parameter rentan**: Field atau parameter yang terpengaruh
- **Cara hacker memanfaatkan**: Penjelasan teknis eksploitasi
- **Mitigasi**: Cara mengatasi kerentanan

### Analisis Response
Tool menganalisis berbagai aspek response:
- **Error Messages**: Database errors, system errors
- **Content Reflection**: Apakah input direfleksikan di output
- **HTTP Headers**: Keberadaan security headers
- **Status Codes**: Response code analysis

## 🚨 Aspek Etika dan Legal

### ✅ Penggunaan yang Diperbolehkan:
- Testing website milik sendiri
- Pembelajaran dan penelitian keamanan
- Penetration testing dengan izin tertulis
- Security awareness training

### ❌ Penggunaan yang DILARANG:
- Testing website tanpa izin
- Aktivitas ilegal atau merusak
- Pelanggaran privasi
- Penyalahgunaan informasi yang ditemukan

## 🔧 Konfigurasi Lanjutan

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export REQUEST_TIMEOUT=15
```

### Kustomisasi Payload
Edit file `app/main.py` untuk menambah/mengurangi payload:
- `SQL_PAYLOADS`: Payload SQL injection
- `XSS_PAYLOADS`: Payload XSS
- `SENSITIVE_FILES`: File yang dicek

## 📊 Output dan Reporting

### Tingkat Severity
- **Critical**: Kerentanan yang dapat langsung dieksploitasi
- **High**: Kerentanan serius yang membutuhkan perhatian
- **Medium**: Kerentanan dengan risiko sedang
- **Low**: Kerentanan dengan dampak minimal

### Informasi Detail
Setiap kerentanan melaporkan:
- Kategori dan nama kerentanan
- Tingkat severity
- Penjelasan teknis
- Cara eksploitasi
- Rekomendasi mitigasi
- Payload yang digunakan
- Parameter/field yang rentan

## 🤝 Kontribusi

Untuk mengembangkan tool ini lebih lanjut:
1. Tambah jenis payload baru
2. Implementasi fuzzing techniques
3. Integrasi dengan vulnerability databases
4. Improve false positive detection
5. Add automated report generation

## 📚 Referensi Belajar

- OWASP Top 10
- Web Application Security Testing
- Penetration Testing Methodologies
- Secure Coding Practices

---
**Disclaimer**: Tool ini dibuat untuk tujuan edukasi. Pengguna bertanggung jawab penuh atas penggunaan tool ini sesuai dengan hukum yang berlaku.
