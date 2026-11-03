# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas_gl, binaries_gl, hidden_gl = collect_all("moderngl")
datas_ctx, binaries_ctx, hidden_ctx = collect_all("glcontext")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries_gl + binaries_ctx,
    datas=[("assets", "assets")] + datas_gl + datas_ctx,
    hiddenimports=hidden_gl + hidden_ctx + ["pygame", "moderngl", "glcontext"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="90sgs",
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
