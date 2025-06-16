# 🔧 Troubleshooting GitHub Actions Build

Panduan mengatasi masalah umum saat build SecurityScanner di GitHub Actions.

## 🚨 Error Umum dan Solusi

### 1. ❌ "Workflow not found" atau "Actions tab kosong"

**Penyebab:**
- File workflow tidak ada di path yang benar
- Branch tidak sesuai

**Solusi:**
```bash
# Pastikan struktur folder benar:
.github/
└── workflows/
    └── build-exe.yml

# Dan file ada di branch main/master
```

**Fix:**
1. Buat folder `.github/workflows/` di root project
2. Upload file `build-exe.yml` ke folder tersebut
3. Commit ke branch `main` atau `master`

### 2. ❌ "Repository not found" atau "Permission denied"

**Penyebab:**
- Repository private tapi tidak ada permission
- Organization settings membatasi Actions

**Solusi:**
1. **Untuk Repository Private:**
   - Settings → Actions → General
   - Enable "Allow all actions and reusable workflows"

2. **Untuk Organization:**
   - Organization Settings → Actions → General
   - Set appropriate permissions

### 3. ❌ "main.py not found"

```yaml
Error: can't open file 'app\main.py': [Errno 2] No such file or directory
```

**Penyebab:**
- Struktur folder salah saat upload
- File tidak ter-commit

**Solusi:**
```bash
# Pastikan struktur benar:
project-root/
├── app/
│   ├── main.py          ← File ini harus ada
│   └── templates/
│       └── index.html
├── .github/
│   └── workflows/
│       └── build-exe.yml
└── requirements.txt
```

**Debug Steps:**
Tambahkan step debug di workflow:
```yaml
- name: 🔍 Debug File Structure
  run: |
    echo "=== Root files ==="
    dir
    echo "=== App folder ==="
    if exist app (dir app) else echo "❌ app folder missing"
    echo "=== Check main.py ==="
    if exist app\main.py (echo "✅ main.py found") else echo "❌ main.py missing"
```

### 4. ❌ "requirements.txt not found"

**Penyebab:**
- File requirements tidak ada
- Nama file salah (spasi, typo)

**Solusi:**
1. **Pastikan file ada:**
   ```
   requirements.txt         ← Dependencies runtime
   requirements-build.txt   ← Dependencies build (PyInstaller, etc)
   ```

2. **Check isi file requirements.txt:**
   ```txt
   flask>=2.0.0
   requests>=2.25.0
   ```

3. **Check isi file requirements-build.txt:**
   ```txt
   flask>=2.0.0
   requests>=2.25.0
   pyinstaller>=5.0
   ```

### 5. ❌ "PyInstaller failed" atau "Build failed"

**Error typical:**
```
ModuleNotFoundError: No module named 'app'
```

**Penyebab:**
- SecurityScanner.spec tidak benar
- Path tidak sesuai dengan struktur project

**Solusi:**
Check file `SecurityScanner.spec`:
```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app/main.py'],              # ← Path harus benar
    pathex=[],
    binaries=[],
    datas=[('app/templates', 'templates')],  # ← Template path
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SecurityScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,                 # ← Set True untuk debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

### 6. ❌ "Disk space exceeded" atau "Build timeout"

**Penyebab:**
- Project terlalu besar
- Dependencies terlalu banyak
- Infinite loop dalam kode

**Solusi:**
1. **Optimize dependencies:**
   ```txt
   # requirements-build.txt - hanya yang perlu
   flask==2.3.3
   requests==2.31.0
   pyinstaller==5.13.0
   ```

2. **Exclude unnecessary files dalam .spec:**
   ```python
   excludes=['matplotlib', 'numpy', 'pandas']  # jika tidak dipakai
   ```

3. **Set timeout lebih besar:**
   ```yaml
   jobs:
     build-exe:
       runs-on: windows-latest
       timeout-minutes: 30  # default 6 jam, set lebih kecil
   ```

### 7. ❌ "Upload artifact failed"

**Penyebab:**
- File artifact tidak ada
- Path salah
- File terlalu besar (>2GB)

**Solusi:**
1. **Verify file exists:**
   ```yaml
   - name: 🔍 Check Build Output
     run: |
       if exist dist\SecurityScanner.exe (
         echo "✅ EXE found"
         dir dist
       ) else (
         echo "❌ EXE not found"
         dir
         exit /b 1
       )
   ```

2. **Split large artifacts:**
   ```yaml
   - name: 📤 Upload EXE Only
     uses: actions/upload-artifact@v3
     with:
       name: SecurityScanner-EXE
       path: dist/SecurityScanner.exe
   ```

### 8. ❌ "Actions minutes exceeded"

**Penyebab:**
- Free plan limit (2000 menit/bulan untuk private repo)
- Build terlalu sering
- Build stuck/hanging

**Solusi:**
1. **Check usage:**
   - Settings → Billing → Plans and usage
   - Actions minutes usage

2. **Optimize workflow:**
   ```yaml
   # Hanya build saat perlu
   on:
     push:
       branches: [ main ]
       paths: ['app/**', '*.txt', '*.spec']  # hanya jika file penting berubah
   ```

3. **Use public repository:**
   - Public repo = unlimited Actions minutes

## 🔧 Advanced Troubleshooting

### Debugging dengan SSH (untuk expert)

**Tambahkan step debug:**
```yaml
- name: 🐛 Debug with SSH
  uses: mxschmitt/action-tmate@v3
  if: failure()  # hanya jika build gagal
```

**Akses via SSH:**
1. Build akan pause saat gagal
2. Login via SSH dari log
3. Debug manual di server

### Custom Runner (untuk enterprise)

**Jika perlu environment khusus:**
```yaml
runs-on: self-hosted  # gunakan runner sendiri
```

### Matrix Build (multiple OS)

**Build untuk Windows + Linux:**
```yaml
strategy:
  matrix:
    os: [windows-latest, ubuntu-latest]
runs-on: ${{ matrix.os }}
```

## 📊 Monitoring dan Optimization

### 1. **Build Performance**

**Check build time:**
```yaml
- name: ⏱️ Build Time
  run: echo "Build started at %TIME%"
```

**Optimize dengan cache:**
```yaml
- name: 📦 Cache Dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
```

### 2. **Resource Usage**

**Monitor resource:**
```yaml
- name: 💻 System Info
  run: |
    echo "=== System Resources ==="
    systeminfo | findstr "Total Physical Memory"
    echo "=== Disk Space ==="
    dir c:\ | findstr "bytes free"
```

### 3. **Build Artifacts Size**

**Check artifact size:**
```yaml
- name: 📏 Check Size
  run: |
    for %%f in (dist\SecurityScanner.exe) do echo EXE Size: %%~zf bytes
    if %%~zf GTR 104857600 echo "⚠️ Warning: EXE larger than 100MB"
```

## 🆘 Getting Help

### 1. **GitHub Community**
- [GitHub Community Forum](https://github.community/)
- Search untuk "PyInstaller GitHub Actions"

### 2. **Check Actions Marketplace**
- [Setup Python](https://github.com/marketplace/actions/setup-python)
- [Upload Artifacts](https://github.com/marketplace/actions/upload-a-build-artifact)

### 3. **Documentation**
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [PyInstaller Docs](https://pyinstaller.readthedocs.io/)

### 4. **Status Pages**
- [GitHub Status](https://www.githubstatus.com/)
- Check jika ada outage

## 🎯 Best Practices

### 1. **Workflow Organization**
```yaml
name: Build SecurityScanner EXE
on: 
  push:
    branches: [ main ]
    paths: ['app/**', '*.txt', '*.spec']  # smart triggers
  workflow_dispatch:  # manual trigger
  
env:
  PYTHON_VERSION: '3.11'
  PYINSTALLER_VERSION: '5.13.0'
```

### 2. **Error Handling**
```yaml
- name: 🔨 Build with Error Handling
  run: |
    pyinstaller SecurityScanner.spec --clean --noconfirm || (
      echo "❌ Build failed, showing logs:"
      type build.log
      exit /b 1
    )
```

### 3. **Notifications**
```yaml
- name: 📢 Notify on Success
  if: success()
  run: echo "✅ Build completed successfully!"
  
- name: 📢 Notify on Failure  
  if: failure()
  run: echo "❌ Build failed, check logs above"
```

---

## 🚀 Ready to Debug?

1. **Check error message** di build log
2. **Cari di section ini** untuk solusi
3. **Apply fix** dan push ulang
4. **Monitor** build selanjutnya

Masih error? Drop kode error dan saya bantu troubleshoot! 💪
