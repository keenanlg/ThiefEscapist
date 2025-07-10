# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Include the current directory
    binaries=[],
    datas=[
        ('../assets', 'assets'),  # Include assets
        ('../tmx', 'tmx'),        # Include tmx files
        ('../tsx', 'tsx')         # Include tsx files
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ThiefEscapist',
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
    distpath='.',  # This specifies the output path for the executable
    workpath='./build',  # Temporary build files stay in build/
    specpath='.',  # Location of the .spec file
)
