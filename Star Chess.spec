# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['C:/Users/Lenovo/Python/Games/Star Chess/Star Chess.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/Lenovo/Python/Games/Star Chess/audio', 'audio/'), ('C:/Users/Lenovo/Python/Games/Star Chess/font', 'font/'), ('C:/Users/Lenovo/Python/Games/Star Chess/images', 'images/'), ('C:/Users/Lenovo/Python/Games/Star Chess/pieces', 'pieces/'), ('C:/Users/Lenovo/Python/Games/Star Chess/scripts', 'scripts/'), ('C:/Users/Lenovo/Python/Games/Star Chess/settings', 'settings/'), ('C:/Users/Lenovo/Python/Games/Star Chess/web', 'web/')],
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
    name='Star Chess',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
