# configura a geração do executável do LeetEmpresas com os arquivos usados pela interface
from PyInstaller.utils.hooks import collect_all
from pathlib import Path

raiz = Path.cwd()
datas = [
    (str(raiz / "templates"), "templates"),
    (str(raiz / "static"), "static"),
    (str(raiz / "models"), "models"),
]
binaries = []
hiddenimports = ["flask_wtf.csrf", "webview"]

# coleta arquivos e módulos adicionais necessários às dependências gráficas
for pacote in ("webview", "PySide6", "qtpy"):
    try:
        dados, binarios, imports = collect_all(pacote)
        datas += dados
        binaries += binarios
        hiddenimports += imports
    except Exception:
        # mantém a configuração utilizável quando um pacote não existe na plataforma atual
        pass

a = Analysis(
    [str(raiz / "desktop.py")],
    pathex=[str(raiz)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="LeetEmpresas",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    name="LeetEmpresas",
)
