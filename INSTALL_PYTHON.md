# 🐍 Panduan Instalasi Python untuk Security Scanner

## Masalah yang Terjadi
Jika Anda melihat pesan error seperti:
```
Python was not found; run without arguments to install from the Microsoft Store
```

Ini berarti Python belum terinstall atau belum dikonfigurasi dengan benar di sistem Windows Anda.

## 📥 Cara Install Python di Windows

### Opsi 1: Install dari Microsoft Store (Termudah)
1. Buka **Microsoft Store**
2. Cari "**Python**"
3. Install **Python 3.11** atau **Python 3.12** (versi terbaru)
4. Tunggu hingga instalasi selesai
5. Restart Command Prompt/PowerShell

### Opsi 2: Install dari Python.org (Direkomendasikan)
1. Buka https://python.org/downloads/
2. Download **Python 3.11** atau **Python 3.12**
3. Jalankan installer yang sudah didownload
4. **PENTING**: Centang "**Add Python to PATH**" sebelum install
5. Klik "Install Now"
6. Tunggu hingga instalasi selesai
7. Restart Command Prompt/PowerShell

## 🔧 Verifikasi Instalasi

Buka Command Prompt atau PowerShell, lalu ketik:
```bash
python --version
```

Jika berhasil, akan muncul output seperti:
```
Python 3.11.x
```

## 🚀 Menjalankan Security Scanner

Setelah Python terinstall, Anda bisa menjalankan Security Scanner dengan:

### Metode 1: Double-click start.bat
1. Double-click file `start.bat`
2. Tunggu hingga server berjalan
3. Browser akan terbuka otomatis ke http://localhost:5000

### Metode 2: Command Line
```bash
# Masuk ke folder cekweb
cd "C:\Users\fajar\Downloads\cekweb"

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
python app/main.py
```

### Metode 3: Menggunakan Launcher
```bash
python launcher.py
```

## 🔍 Troubleshooting

### Problem: "python is not recognized"
**Solusi**: Python belum ditambahkan ke PATH
1. Cari "Environment Variables" di Windows Search
2. Klik "Edit the system environment variables"
3. Klik "Environment Variables"
4. Di "System Variables", cari "Path"
5. Klik "Edit" > "New"
6. Tambahkan path Python (biasanya: `C:\Python311\` dan `C:\Python311\Scripts\`)
7. Restart Command Prompt

### Problem: "pip is not recognized"
**Solusi**: 
```bash
python -m pip install -r requirements.txt
```

### Problem: "Module not found"
**Solusi**: Install ulang dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Problem: Port 5000 sudah digunakan
**Solusi**: Ganti port di file `app/main.py` baris terakhir:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Ganti 5000 ke 8080
```

## 📱 Mengakses Security Scanner

Setelah server berjalan, buka browser dan akses:
- http://localhost:5000 (default)
- http://127.0.0.1:5000 (alternatif)

## ⚠️ PENTING - Penggunaan Etis

Security Scanner ini HANYA boleh digunakan untuk:
- ✅ Testing website milik sendiri
- ✅ Pembelajaran keamanan siber
- ✅ Penetration testing dengan izin tertulis
- ✅ Security awareness training

DILARANG digunakan untuk:
- ❌ Testing website tanpa izin
- ❌ Aktivitas ilegal
- ❌ Menyerang sistem orang lain

## 🆘 Butuh Bantuan?

Jika masih ada masalah, coba:
1. Restart komputer setelah install Python
2. Jalankan Command Prompt sebagai Administrator
3. Update Windows ke versi terbaru
4. Disable antivirus sementara saat instalasi

## 🎯 Fitur Security Scanner

Tool ini dapat mendeteksi:
- 🔴 SQL Injection
- 🟠 Cross-Site Scripting (XSS)  
- 🟣 Command Injection
- 🟡 Directory Traversal
- 🔵 Sensitive File Exposure
- 🟢 Security Headers Missing
- 🟤 SSL/TLS Issues

Happy Scanning! 🛡️
