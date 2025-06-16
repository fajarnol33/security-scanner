# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Get the directory containing this spec file
spec_dir = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

a = Analysis(
    ['app/main.py'],
    pathex=[spec_dir],
    binaries=[],
    datas=[
        ('app/templates', 'app/templates'),
        ('app/static', 'app/static') if os.path.exists('app/static') else None,
    ],
    hiddenimports=[
        'flask',
        'requests',
        'bs4',
        'urllib3',
        'ssl',
        'socket',
        'datetime',
        'warnings',
        'urllib.parse',
        'requests.adapters',
        'urllib3.util.retry',
        'werkzeug.serving',
        'werkzeug.utils',
        'jinja2',
        'markupsafe',
        'click',
        'itsdangerous',
        'certifi',
        'charset_normalizer',
        'idna',
        'lxml',
        'soupsieve'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove None entries from datas
a.datas = [x for x in a.datas if x is not None]

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
    console=False,  # Set to False for GUI mode
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None
)
