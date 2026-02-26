# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_all

# Colectăm automat tot ce ține de bibliotecile care lipsesc
tkcal_datas, tkcal_binaries, tkcal_hidden = collect_all('tkcalendar')
babel_datas, babel_binaries, babel_hidden = collect_all('babel')
crypto_datas, crypto_binaries, crypto_hidden = collect_all('cryptography')

proiect_path = r'E:\Programare\GitHub Projects\ClassMaster'

a = Analysis(
    ['main.py'],
    pathex=[proiect_path],
    binaries=tkcal_binaries + babel_binaries + crypto_binaries,
    datas=tkcal_datas + babel_datas + crypto_datas + [('Internal', 'Internal')],
    hiddenimports=tkcal_hidden + babel_hidden + crypto_hidden + [
        'tkcalendar', 'babel.numbers', 'cryptography', '_cffi_backend'
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
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # O punem pe False acum că am văzut eroarea
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