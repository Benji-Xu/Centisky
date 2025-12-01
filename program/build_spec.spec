# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 收集所有需要的数据文件
added_files = [
    ('tools', 'tools'),  # 包含所有工具代码
    ('../templates', 'templates'),
]

# 如果存在 ffmpeg 目录，添加到打包
import os
if os.path.exists('ffmpeg'):
    added_files.append(('ffmpeg', 'ffmpeg'))

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'openpyxl', 
        'pandas', 
        'PIL', 
        'tkinter',
        'tools.label_box.main',
        'tools.label_box.wrapper',
        'tools.label_box.core',
        'tools.image_processor.main',
    ],
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
    [],
    exclude_binaries=True,
    name='Centisky',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 不设置图标
    version=None,  # 不设置版本信息
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Centisky',
)
