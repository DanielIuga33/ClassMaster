# -*- mode: python ; coding: utf-8 -*-
import os

proiect_path = r'D:\Programare\GithubProjects\ClassMaster'
site_packages = os.path.join(proiect_path, '.venv', 'Lib', 'site-packages')

# Definirea căilor către folderele care lipsesc
crypto_dir = os.path.join(site_packages, 'cryptography')
cffi_dir = os.path.join(site_packages, 'cffi')
# Verifică dacă acest nume de fișier este identic cu cel găsit la Pasul 1
cffi_backend = os.path.join(site_packages, '_cffi_backend.cp313-win_amd64.pyd')

a = Analysis(
    ['main.py'],
    pathex=[proiect_path],
    binaries=[(cffi_backend, '.')], # Forțăm includerea binarelor CFFI
    datas=[
        ('Internal', 'Internal'),
        (crypto_dir, 'cryptography'), # Copiem manual tot folderul de criptare
        (cffi_dir, 'cffi')
    ],
    hiddenimports=[
        'cryptography',
        'cffi',
        '_cffi_backend',
        'hmac',
        'hashlib',
        'base64',
        'tkcalendar',
        'babel.numbers'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ClassMaster',
    debug=True, # Lăsăm Debug=True pentru a vedea erorile într-o consolă dacă dă greș
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True, # Lăsăm consola deschisă temporar pentru diagnosticare
    icon=['icon.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='ClassMaster',
)