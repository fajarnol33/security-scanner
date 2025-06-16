# 🌐 PANDUAN LENGKAP: Build SecurityScanner.exe di GitHub Actions

## 🎯 OVERVIEW
GitHub Actions akan otomatis build SecurityScanner.exe di cloud tanpa perlu install Python di komputer Anda!

## 📋 LANGKAH-LANGKAH DETAIL

### **STEP 1: Persiapan GitHub Repository**

#### 1.1 Buat Repository Baru
1. Buka **GitHub.com**
2. Klik **"New Repository"** (tombol hijau)
3. **Repository name**: `security-scanner`
4. **Description**: `Website Vulnerability Assessment Tool`
5. ✅ Centang **"Public"** (atau Private jika mau)
6. ✅ Centang **"Add a README file"**
7. Klik **"Create repository"**

#### 1.2 Upload Project Files
Ada beberapa cara upload:

**Cara A: Drag & Drop (Termudah)**
1. Buka repository yang baru dibuat
2. Klik **"uploading an existing file"**
3. **Drag & drop** semua file dari folder `cekweb` ke browser
4. **Commit message**: `Initial commit - Security Scanner`
5. Klik **"Commit changes"**

**Cara B: Git Command (Advanced)**
```bash
git clone https://github.com/[username]/security-scanner.git
cd security-scanner
# Copy semua file dari cekweb ke sini
git add .
git commit -m "Initial commit - Security Scanner"
git push origin main
```

### **STEP 2: Verifikasi File Structure**

Pastikan struktur file di GitHub seperti ini:
```
security-scanner/
├── .github/
│   └── workflows/
│       └── build-exe.yml          # ← File workflow
├── app/
│   ├── main.py                    # ← Main application
│   └── templates/
│       └── index.html             # ← Web interface
├── requirements-build.txt         # ← Build dependencies
├── SecurityScanner.spec          # ← PyInstaller config
├── build_exe.py                  # ← Build script
└── README.md                     # ← Documentation
```

### **STEP 3: Trigger Build Process**

#### 3.1 Manual Trigger (Recommended)
1. Buka repository di GitHub
2. Klik tab **"Actions"**
3. Klik **"Build SecurityScanner EXE"** di sidebar kiri
4. Klik tombol **"Run workflow"** (tombol biru)
5. Pilih branch: **"main"** atau **"master"**
6. Klik **"Run workflow"**

#### 3.2 Auto Trigger
Build akan otomatis jalan saat:
- Push ke branch main/master
- Create Pull Request
- Manual trigger dari Actions tab

### **STEP 4: Monitor Build Progress**

1. **Masuk ke tab "Actions"**
2. **Klik workflow run** yang sedang berjalan
3. **Monitor steps**:
   - 📥 Checkout Repository
   - 🐍 Setup Python 3.11
   - 📦 Install Build Dependencies
   - 🔨 Build Executable with PyInstaller
   - 📤 Upload Artifacts

#### Status Indicators:
- 🟡 **Yellow**: Sedang berjalan (2-5 menit)
- ✅ **Green**: Berhasil
- ❌ **Red**: Gagal (check logs)

### **STEP 5: Download .EXE File**

Setelah build **berhasil** (status hijau):

1. **Scroll ke bawah** di halaman workflow run
2. **Lihat section "Artifacts"**
3. **Download pilihan**:
   - **SecurityScanner-EXE**: File .exe tunggal
   - **SecurityScanner-Portable-Package**: Folder lengkap
   - **SecurityScanner-Portable-ZIP**: Archive terkompresi

#### File yang Anda dapatkan:
```
SecurityScanner_Portable/
├── SecurityScanner.exe           # 🎯 Main executable (~50-80MB)
└── README.txt                   # 📝 Usage instructions
```

## 🔧 TROUBLESHOOTING

### **Build Gagal? Check Ini:**

#### Error: "Module not found"
**Solusi**: Update `requirements-build.txt`
```txt
Flask==2.3.3
requests==2.31.0
beautifulsoup4==4.12.2
PyInstaller==6.2.0
```

#### Error: "File not found"
**Solusi**: Pastikan struktur folder benar
- `app/main.py` harus ada
- `app/templates/index.html` harus ada
- `.github/workflows/build-exe.yml` harus ada

#### Error: "PyInstaller failed"
**Solusi**: Check PyInstaller spec file
- Pastikan `SecurityScanner.spec` valid
- Check hiddenimports di spec file

### **Workflow Tidak Muncul?**
1. Pastikan file `.github/workflows/build-exe.yml` di root repository
2. File harus ber-ekstensi `.yml` bukan `.yaml`
3. Tunggu 1-2 menit setelah push

## 🚀 OPTIMISASI BUILD

### **Membuat Build Lebih Cepat:**
```yaml
# Tambah di workflow file
- name: Cache Python packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements-build.txt') }}
```

### **Multi-Platform Build:**
```yaml
strategy:
  matrix:
    os: [windows-latest, ubuntu-latest, macos-latest]
runs-on: ${{ matrix.os }}
```

## 📋 AUTOMATIC RELEASES

Untuk auto-create releases saat build:

```yaml
- name: Create Release
  if: github.ref == 'refs/heads/main'
  uses: actions/create-release@v1
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  with:
    tag_name: v1.0.${{ github.run_number }}
    release_name: SecurityScanner v1.0.${{ github.run_number }}
    body: |
      ## SecurityScanner v1.0.${{ github.run_number }}
      
      🛡️ Website Vulnerability Assessment Tool
      
      ### Features:
      - SQL Injection Detection
      - XSS Vulnerability Testing
      - Command Injection Scanning
      - Sensitive File Detection
      - Security Headers Analysis
      
      ### Usage:
      1. Download SecurityScanner.exe
      2. Double-click to run
      3. Browser opens to http://localhost:5000
      4. Enter URL and scan!
      
      ⚠️ Use only on websites you own or have permission to test.
```

## 🎉 KEUNGGULAN GITHUB ACTIONS

### ✅ **Advantages:**
- **Gratis** untuk public repositories
- **Cloud-based** - tidak perlu Python lokal
- **Automated** - build otomatis saat push
- **Multi-platform** - bisa build untuk Windows/Linux/Mac
- **Artifact storage** - file tersimpan 30 hari
- **Version control** - track semua builds

### 📊 **Build Stats:**
- **Waktu build**: 3-5 menit
- **File size**: ~50-80MB
- **Compatibility**: Windows 7/8/10/11
- **Requirements**: Tidak ada (standalone)

## 🏁 HASIL AKHIR

Setelah selesai, Anda akan punya:
1. **SecurityScanner.exe** - Portable executable
2. **Auto-opens browser** ke localhost:5000
3. **Full vulnerability scanning** capabilities
4. **Professional reporting** dengan severity levels
5. **Modern web interface**

**Total waktu**: ~10 menit (upload + build + download)
**Effort**: Minimal (mostly drag & drop)
**Result**: Production-ready portable .exe! 🛡️🚀

---
**Happy Building with GitHub Actions!** 🌐✨
