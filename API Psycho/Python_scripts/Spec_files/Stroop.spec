# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

a = Analysis(
    ['../Psychopy_Stroop.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Users\\coren\\AppData\\Roaming\\Python\\Python310\\site-packages\\psychopy', 'psychopy'),
        ('../Paradigme_parent.py', '.'),
        ('../writtingprt.py', '.')
    ],
    hiddenimports=['numpy', 'platform', 'pkg_resources', 'six', 'pyglet', 'yaml', 'serial', 'serial.tools.list_ports', 'scipy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['torch', 'torchvision', 'torchaudio', 'torch.utils.tensorboard'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Psychopy_Stroop',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Psychopy_Stroop',
)
