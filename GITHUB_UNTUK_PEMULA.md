# 👶 Panduan GitHub untuk Pemula

Belum pernah pakai GitHub? No problem! Panduan ini akan bantu Anda upload project dan build EXE dalam 10 menit.

## 🤔 Apa itu GitHub?

**GitHub** = tempat menyimpan kode program di internet (gratis!)

**Keuntungan:**
- ✅ Backup kode otomatis
- ✅ Build aplikasi gratis
- ✅ Sharing project mudah
- ✅ Version control (tracking perubahan)

## 📝 Step 1: Buat Akun GitHub (2 menit)

1. **Buka:** https://github.com
2. **Klik:** "Sign up" (pojok kanan atas)
3. **Isi data:**
   - Username: `namaanda123` (unik, no spasi)
   - Email: email aktif Anda
   - Password: password kuat
4. **Verify email** dari inbox
5. **Done!** Anda sudah punya akun GitHub

## 📁 Step 2: Buat Repository (3 menit)

**Repository** = folder project di GitHub

1. **Setelah login,** klik tombol **"New"** (hijau, pojok kiri)
   
2. **Isi form:**
   ```
   Repository name: security-scanner
   Description: Website Security Scanner Tool
   📍 Public (pilih ini - unlimited builds!)
   ✅ Add a README file (centang)
   ```

3. **Klik:** "Create repository"

**Result:** Anda akan di redirect ke halaman repository baru!

## 📤 Step 3: Upload Project Files (3 menit)

Di halaman repository yang baru dibuat:

1. **Klik:** "uploading an existing file" (link biru)

2. **Drag & Drop files:**
   
   **Cara 1 - Satu-satu:**
   - Drag file `requirements.txt`
   - Drag file `requirements-build.txt`  
   - Drag file `SecurityScanner.spec`
   - dll.

   **Cara 2 - Sekaligus (Recommended):**
   - Buka folder project di Windows Explorer
   - Select ALL files dan folders (`Ctrl+A`)
   - Drag & drop ke area upload GitHub

3. **Files yang harus di-upload:**
   ```
   📁 app/
      ├── main.py
      └── templates/
          └── index.html
   📁 .github/
      └── workflows/
          └── build-exe.yml
   📄 requirements.txt
   📄 requirements-build.txt
   📄 SecurityScanner.spec
   📄 README.md
   📄 (dan file lainnya)
   ```

4. **Commit changes:**
   - Scroll ke bawah
   - Commit message: "Upload Security Scanner project"
   - Klik **"Commit changes"** (hijau)

## 🔨 Step 4: Otomatis Build! (3-5 menit)

**Setelah upload selesai, magic happens:**

1. **Build otomatis dimulai** - GitHub akan langsung build EXE!

2. **Lihat progress:**
   - Klik tab **"Actions"** (menu atas)
   - Klik pada job "Build SecurityScanner EXE"
   - Lihat progress real-time:
     ```
     📥 Checkout Repository     ✅
     🐍 Setup Python 3.11       ✅  
     📦 Install Dependencies    ✅
     🔨 Build Executable       🔄 (running...)
     ```

3. **Tunggu sampai selesai** (✅ semua hijau)

## 📥 Step 5: Download EXE (1 menit)

**Setelah build selesai:**

1. **Scroll ke bawah** pada halaman build
2. **Cari section "Artifacts":**
   ```
   📦 Artifacts
   ├── SecurityScanner-EXE              ← Download ini!
   ├── SecurityScanner-Portable-Package  
   └── SecurityScanner-Portable-ZIP     
   ```

3. **Klik "SecurityScanner-EXE"** untuk download

4. **Extract ZIP** yang ter-download

5. **Double-click `SecurityScanner.exe`**

🎉 **Done!** Browser akan terbuka ke aplikasi scanner!

## 🔄 Update Project

**Mau ubah kode atau tambah fitur?**

1. **Edit di GitHub:**
   - Klik file yang mau diedit (misal: `app/main.py`)
   - Klik icon pensil (pojok kanan)
   - Edit kode
   - Scroll ke bawah, commit changes

2. **Upload file baru:**
   - Di halaman repository utama
   - Klik "Add file" → "Upload files"
   - Upload file yang diubah
   - Commit changes

3. **Auto-build:**
   - Build otomatis dimulai setelah commit
   - Download EXE terbaru dari Artifacts

## 💡 Tips untuk Pemula

### ✅ Do's
- **Public repository** = unlimited builds (gratis selamanya)
- **Descriptive commit messages** = mudah tracking perubahan
- **Regular backups** = commit sering-sering
- **Browse other projects** = belajar dari developer lain

### ❌ Don'ts
- **Jangan upload password/API keys** di kode
- **Jangan repo private** kecuali butuh (limited builds)
- **Jangan push file besar** (>100MB)
- **Jangan delete repo** tanpa backup

### 🔍 Istilah GitHub yang Perlu Tahu

- **Repository** = Folder project
- **Commit** = Save perubahan  
- **Push** = Upload ke GitHub
- **Pull** = Download dari GitHub
- **Branch** = Versi paralel project
- **Actions** = Automation (build, test, deploy)
- **Artifacts** = File hasil build

## 🆘 Masalah Umum

### ❌ "Repository not found"
**Solusi:** Pastikan repository public, bukan private

### ❌ "Upload failed"  
**Solusi:** File terlalu besar (>25MB), zip dulu atau upload terpisah

### ❌ "Build failed"
**Solusi:** 
1. Cek tab Actions → klik build yang gagal
2. Lihat error message
3. Baca [TROUBLESHOOTING_GITHUB_ACTIONS.md](TROUBLESHOOTING_GITHUB_ACTIONS.md)

### ❌ "No artifacts"
**Solusi:**
1. Build belum selesai - tunggu sampai ✅ hijau
2. Build gagal - cek error di Actions tab

## 🎓 Next Steps

**Setelah berhasil:**

1. **Explore GitHub:** 
   - Star ⭐ project yang menarik
   - Follow developer lain
   - Belajar dari open source projects

2. **Learn Git:**
   - Install Git di komputer
   - Clone repository ke local
   - Push/pull via command line

3. **Advanced GitHub:**
   - GitHub Pages (hosting website gratis)
   - GitHub Codespaces (VS Code di browser)
   - GitHub CLI (command line tool)

## 🔗 Resources

- **GitHub Help:** https://docs.github.com/
- **Git Tutorial:** https://git-scm.com/docs/gittutorial
- **Markdown Guide:** https://guides.github.com/features/mastering-markdown/
- **GitHub Learning Lab:** https://lab.github.com/

---

## 🎉 Selamat!

Anda sudah berhasil:
✅ Membuat akun GitHub  
✅ Upload project  
✅ Build aplikasi EXE  
✅ Download hasil build  

**Welcome to the developer community!** 🚀

Punya pertanyaan? Buat issue di repository ini atau tanya di GitHub Community!

---

**💪 Pro Tip:**
Sekarang Anda bisa build aplikasi tanpa install Python di komputer. Cukup edit kode di GitHub, tunggu build selesai, download EXE baru. **It's that simple!** ✨
