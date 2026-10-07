from pathlib import Path
from PyInstaller.utils.hooks import collect_all, collect_submodules


BASE_DIR = Path(SPEC).resolve().parent


# Modelos do projeto
hiddenimports = collect_submodules("models")


# PyWebView
webview_datas, webview_binaries, webview_hiddenimports = collect_all("webview")
hiddenimports += webview_hiddenimports


# QtPy
qtpy_datas, qtpy_binaries, qtpy_hiddenimports = collect_all("qtpy")
hiddenimports += qtpy_hiddenimports


a = Analysis(
    [str(BASE_DIR / "desktop.py")],

    pathex=[
        str(BASE_DIR),
    ],

    binaries=[
        *webview_binaries,
        *qtpy_binaries,
    ],

    datas=[
        (str(BASE_DIR / "templates"), "templates"),
        (str(BASE_DIR / "static"), "static"),

        *webview_datas,
        *qtpy_datas,
    ],

    hiddenimports=hiddenimports,

    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],

    excludes=[
        "tkinter",
    ],

    noarchive=False,
)


pyz = PYZ(
    a.pure,
    a.zipped_data,
)


exe = EXE(
    pyz,
    a.scripts,
    [],

    exclude_binaries=True,

    name="LeetEmpresas",

    debug=False,
    bootloader_ignore_signals=False,

    strip=False,
    upx=True,

    console=False,
)


coll = COLLECT(
    exe,

    a.binaries,
    a.datas,

    strip=False,
    upx=True,
    upx_exclude=[],

    name="LeetEmpresas",
)