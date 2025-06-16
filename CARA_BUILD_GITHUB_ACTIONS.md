# 🚀 Cara Build EXE di GitHub Actions

Panduan lengkap untuk membuild aplikasi SecurityScanner menjadi file `.exe` menggunakan GitHub Actions (gratis dan otomatis di cloud).

## 📋 Persyaratan

- ✅ Akun GitHub (gratis)
- ✅ Repository GitHub untuk project ini
- ✅ Koneksi internet

**TIDAK perlu:**
- ❌ Python terinstall di komputer
- ❌ PyInstaller di komputer lokal
- ❌ Kompilasi manual

## 🎯 Keuntungan Build di GitHub Actions

1. **Gratis** - GitHub Actions memberikan 2000 menit gratis per bulan
2. **Otomatis** - Build berjalan di server GitHub, bukan di komputer Anda
3. **Konsisten** - Environment yang sama setiap kali build
4. **Multi-Platform** - Bisa build untuk Windows, Linux, macOS
5. **Tanpa Setup** - Tidak perlu install Python/PyInstaller di komputer

## 📁 Step 1: Upload ke GitHub

### Opsi A: Menggunakan GitHub Web Interface

1. **Buat Repository Baru:**
   - Buka https://github.com
   - Klik tombol **"New repository"** (hijau)
   - Nama repository: `security-scanner` (atau nama lain)
   - Pilih **Public** atau **Private**
   - ✅ Centang "Add a README file"
   - Klik **"Create repository"**

2. **Upload Files:**
   - Di halaman repository baru, klik **"uploading an existing file"**
   - Drag & drop semua file project ke area upload:
     ```
     app/
     .github/
     requirements.txt
     requirements-build.txt
     SecurityScanner.spec
     README.md
     (dan file lainnya)
     ```
   - Tulis commit message: "Initial upload - Security Scanner"
   - Klik **"Commit changes"**

### Opsi B: Menggunakan Git Command Line

Jika Anda familiar dengan Git:

```bash
# Di folder project
git init
git add .
git commit -m "Initial upload - Security Scanner"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO-NAME.git
git push -u origin main
```

## 🔨 Step 2: Menjalankan Build

### Otomatis (Recommended)

Build akan **otomatis berjalan** setelah upload karena ada trigger:
```yaml
on: 
  push:
    branches: [ main, master ]
```

### Manual Trigger

Jika ingin build manual:

1. **Buka Repository GitHub:**
   - Masuk ke repository Anda di GitHub

2. **Ke Tab Actions:**
   - Klik tab **"Actions"** di menu atas

3. **Run Workflow:**
   - Klik **"Build SecurityScanner EXE"** (workflow name)
   - Klik **"Run workflow"** (tombol biru)
   - Pilih branch **"main"**
   - Klik **"Run workflow"**

## 📊 Step 3: Monitor Progress

1. **Lihat Progress:**
   - Di tab "Actions", klik pada build job yang sedang berjalan
   - Anda akan melihat progress real-time:
     ```
     📥 Checkout Repository    ✅
     🐍 Setup Python 3.11      ✅  
     📦 Install Dependencies   ✅
     🔍 Verify Files          ✅
     🔨 Build Executable      🔄 (sedang berjalan)
     ```

2. **Build Duration:**
   - Biasanya 3-5 menit untuk project ini
   - Tergantung kompleksitas dan ukuran project

## 📥 Step 4: Download Hasil Build

Setelah build selesai (✅ semua langkah hijau):

1. **Scroll ke bawah** pada halaman build results
2. **Cari section "Artifacts":**
   ```
   📦 Artifacts
   ├── SecurityScanner-EXE (1 file)
   ├── SecurityScanner-Portable-Package (folder)
   └── SecurityScanner-Portable-ZIP (compressed)
   ```

3. **Download yang Anda butuhkan:**
   - **SecurityScanner-EXE**: File .exe tunggal
   - **SecurityScanner-Portable-Package**: Folder lengkap dengan README
   - **SecurityScanner-Portable-ZIP**: ZIP siap distribusi

## 🎯 Step 5: Menggunakan Hasil Build

### Untuk File EXE tunggal:
1. Download `SecurityScanner-EXE`
2. Extract file ZIP
3. Double-click `SecurityScanner.exe`
4. Browser akan otomatis terbuka ke http://localhost:5000

### Untuk Package lengkap:
1. Download `SecurityScanner-Portable-ZIP`
2. Extract di folder yang diinginkan
3. Jalankan `SecurityScanner.exe`
4. Baca `README.txt` untuk panduan lengkap

## 🔄 Build Ulang

### Kapan perlu build ulang?
- ✅ Setelah mengubah kode
- ✅ Setelah menambah fitur baru
- ✅ Setelah fix bug
- ✅ Ingin update ke versi terbaru

### Cara build ulang:
1. **Upload perubahan** ke GitHub (commit & push)
2. **Build otomatis** akan berjalan
3. **Download** hasil build terbaru

## 🛠️ Troubleshooting

### ❌ Build Gagal

**Cek Build Log:**
1. Klik pada build job yang gagal
2. Cari langkah yang error (⚠️ merah)
3. Klik untuk melihat detail error

**Error Umum:**

1. **"main.py not found"**
   ```
   Solusi: Pastikan struktur folder benar
   app/
   ├── main.py
   └── templates/
       └── index.html
   ```

2. **"requirements.txt missing"**
   ```
   Solusi: Upload file requirements.txt dan requirements-build.txt
   ```

3. **"PyInstaller failed"**
   ```
   Solusi: Cek SecurityScanner.spec syntax
   ```

### 🔍 Debug Tips

**Verbose Output:**
Tambahkan di workflow untuk debug lebih detail:
```yaml
- name: Debug Build
  run: |
    echo "=== Python Version ==="
    python --version
    echo "=== Installed Packages ==="
    pip list
    echo "=== Project Structure ==="
    tree /f
```

### 💡 Optimization

**Mempercepat Build:**
1. Gunakan cache untuk dependencies:
   ```yaml
   - name: Cache pip
     uses: actions/cache@v3
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
   ```

2. Parallel builds untuk multiple OS:
   ```yaml
   strategy:
     matrix:
       os: [windows-latest, ubuntu-latest]
   ```

## 📊 Monitoring Build

### GitHub Actions Limits (Free Account):
- ✅ **2000 menit/bulan** untuk private repos
- ✅ **Unlimited** untuk public repos
- ✅ **20 concurrent jobs**

### Build Statistics:
- **Rata-rata waktu build**: 3-5 menit
- **Ukuran artifact**: ~50-100 MB
- **Retention**: 30 hari (bisa diubah)

## 🎉 Sukses Build!

Jika semua langkah berhasil, Anda akan memiliki:

✅ **SecurityScanner.exe** - Aplikasi siap pakai
✅ **Portable Package** - Lengkap dengan dokumentasi  
✅ **ZIP Archive** - Siap distribusi
✅ **Otomatis build** - Setiap update kode

## 🔗 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [PyInstaller Documentation](https://pyinstaller.readthedocs.io/)
- [Security Scanner README](README.md)

---

**💡 Tips:**
- Build akan otomatis berjalan setiap push ke branch main
- Hasil build tersimpan 30 hari
- Bisa download berkali-kali dalam periode retention
- Gunakan manual trigger untuk build custom

**🛡️ Keamanan:**
- Kode akan public jika repository public
- Gunakan private repository untuk project sensitive
- Jangan commit API keys atau credentials

Ready untuk build? Upload project ke GitHub dan tunggu magic happen! 🚀
