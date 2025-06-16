# Contoh Hasil Scan Security Scanner

## Target: https://example-vulnerable-site.com

### 📊 Ringkasan Hasil
- **Total Kerentanan**: 8
- **Critical**: 3
- **High**: 2
- **Medium**: 2
- **Low**: 1

---

## 🚨 Critical Vulnerabilities

### 1. SQL Injection - Field: username
**Kategori**: SQL Injection  
**Severity**: Critical  

**Penjelasan**: Field "username" rentan terhadap SQL Injection. Ditemukan error database yang mengindikasikan kerentanan.

**Cara Hacker Memanfaatkan**: Hacker dapat memasukkan payload seperti "' OR 1=1--" untuk mengakses atau memanipulasi database. Ini dapat menyebabkan pencurian data, bypass autentikasi, atau penghapusan data.

**Payload yang Digunakan**: `' OR 1=1--`  
**Field Rentan**: username

**Cara Mengatasi**: Gunakan prepared statements/parameterized queries, validasi input yang ketat, dan principle of least privilege untuk database user.

---

### 2. Command Injection - Field: filename
**Kategori**: Command Injection  
**Severity**: Critical  

**Penjelasan**: Field "filename" rentan terhadap command injection. Server mengeksekusi command sistem.

**Cara Hacker Memanfaatkan**: Hacker dapat menjalankan command sistem operasi dengan payload seperti "; cat /etc/passwd". Ini memungkinkan akses penuh ke server, pencurian data, atau perusakan sistem.

**Payload yang Digunakan**: `; cat /etc/passwd`  
**Field Rentan**: filename

**Cara Mengatasi**: Hindari eksekusi command sistem dengan input user. Jika diperlukan, gunakan whitelist command yang diizinkan dan sanitasi input ketat.

---

### 3. Exposed Sensitive File: .env
**Kategori**: Information Disclosure  
**Severity**: Critical  

**Penjelasan**: File sensitif ".env" dapat diakses secara publik dan berpotensi mengandung informasi rahasia.

**Cara Hacker Memanfaatkan**: Hacker dapat mengakses file ini langsung melalui browser dan memperoleh informasi seperti kredensial database, API keys, atau konfigurasi sistem yang dapat digunakan untuk serangan lebih lanjut.

**URL**: https://example-vulnerable-site.com/.env  
**File Size**: 2048 bytes

**Cara Mengatasi**: Pindahkan file ".env" ke luar document root, atau blokir akses menggunakan .htaccess/web server configuration.

---

## ⚠️ High Vulnerabilities

### 4. Reflected XSS - Field: search
**Kategori**: Cross-Site Scripting (XSS)  
**Severity**: High  

**Penjelasan**: Field "search" rentan terhadap Reflected XSS. Input user direfleksikan dalam response tanpa sanitasi.

**Cara Hacker Memanfaatkan**: Hacker dapat mengirim link berbahaya yang berisi script JavaScript. Ketika korban mengklik link tersebut, script akan dieksekusi di browser korban dan dapat mencuri cookie, session, atau melakukan aksi atas nama korban.

**Payload yang Digunakan**: `<script>alert('XSS')</script>`  
**Field Rentan**: search

**Cara Mengatasi**: Lakukan HTML encoding/escaping pada semua output user, gunakan Content Security Policy (CSP), validasi input secara ketat.

---

### 5. Directory Traversal via Parameter: file
**Kategori**: Directory Traversal  
**Severity**: High  

**Penjelasan**: Parameter "file" rentan terhadap directory traversal attack.

**Cara Hacker Memanfaatkan**: Hacker dapat mengakses file sistem operasi dengan menggunakan payload traversal seperti "../../../etc/passwd" untuk membaca file sensitif server.

**Payload yang Digunakan**: `../../../etc/passwd`  
**Parameter Rentan**: file

**Cara Mengatasi**: Validasi dan sanitasi input parameter file, gunakan whitelist path yang diizinkan, implementasikan proper access control.

---

## 🔶 Medium Vulnerabilities

### 6. Missing CSRF Protection
**Kategori**: Form Security  
**Severity**: Medium  

**Penjelasan**: Ditemukan form POST tanpa perlindungan CSRF token.

**Cara Hacker Memanfaatkan**: Hacker dapat membuat website yang mengirim request POST ke form Anda atas nama user yang sedang login, melakukan aksi yang tidak diinginkan.

**Cara Mengatasi**: Implementasikan CSRF token pada semua form yang mengubah data.

---

### 7. Open Redirect via Parameter: redirect_url
**Kategori**: Open Redirect  
**Severity**: Medium  

**Penjelasan**: Parameter "redirect_url" dapat digunakan untuk redirect ke URL eksternal.

**Cara Hacker Memanfaatkan**: Hacker dapat membuat link yang tampak legitimate tapi mengarahkan korban ke website berbahaya. Ini sering digunakan untuk phishing atau menyebarkan malware.

**Parameter Rentan**: redirect_url  
**Redirect ke**: http://evil.com

**Cara Mengatasi**: Validasi destination URL dengan whitelist domain yang diizinkan, atau gunakan indirect redirect dengan mapping internal.

---

## 🔵 Low Vulnerabilities

### 8. Server Information Disclosure
**Kategori**: Information Disclosure  
**Severity**: Low  

**Penjelasan**: Server mengungkapkan informasi: Apache/2.4.41 (Ubuntu)

**Cara Hacker Memanfaatkan**: Informasi server dapat digunakan hacker untuk mencari exploit spesifik untuk versi software yang digunakan.

**Cara Mengatasi**: Sembunyikan atau ubah header Server untuk tidak mengungkapkan informasi versi.

---

## 📋 Rekomendasi Umum

1. **Implementasi Security Headers**
   - Content-Security-Policy
   - X-Frame-Options
   - X-Content-Type-Options

2. **Input Validation & Sanitization**
   - Validasi semua input user
   - Implementasi whitelist validation
   - HTML encoding untuk output

3. **Database Security**
   - Gunakan prepared statements
   - Principle of least privilege
   - Regular security updates

4. **File Security**
   - Pindahkan file sensitif ke luar document root
   - Implementasi proper access control
   - Regular backup dan monitoring

5. **Regular Security Testing**
   - Automated vulnerability scanning
   - Manual penetration testing
   - Code review untuk security issues

---
**Catatan**: Hasil ini adalah contoh demonstrasi dari Security Scanner tool. Pastikan untuk melakukan testing hanya pada website yang Anda miliki atau dengan izin yang sah.
