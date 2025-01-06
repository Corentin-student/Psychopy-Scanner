# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Collecte des fichiers statiques et templates
datas = [
    ('static', 'static'),      # Inclure tout le dossier 'static'
    ('static/jsons', 'static/jsons'),
    ('templates', 'templates') # Inclure tout le dossier 'templates'
]

a = Analysis(
    ['application.py'],  # Le fichier principal qui lance votre application Flask
    pathex=['.'],  # Le chemin où se trouvent vos fichiers
    binaries=[],
    datas=datas,  # Inclusion des fichiers statiques et templates
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

# Création de l'exécutable
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='application',  # Nom de l'exécutable
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True  # Mettre à False si vous ne voulez pas de console
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='application'
)
