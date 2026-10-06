import sqlite3
from pathlib import Path

diretorio_atual = Path.home()/".leet_empresas"
diretorio_atual.mkdir(parents=True, exist_ok=True)
banco_dados = diretorio_atual/"leet.db"

#arquivo utilizado para a criação das tabelas.

def conectar():
    connector = sqlite3.connect(banco_dados, detect_types=sqlite3.PARSE_DECLTYPES |
                                 sqlite3.PARSE_COLNAMES)
    connector.row_factory = sqlite3.Row
    cursor = connector.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    return connector

#tipos de variaveis sqlite:
#NULL
#INTEGER
#REAL
#TEXT
#BLOB

def inicializar_banco():
    connector = conectar()
    cursor = connector.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            nome_empresa TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produto (
            id_prod INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_prod TEXT NOT NULL,
            valor_custo REAL NOT NULL,
            valor_venda REAL NOT NULL,
            quant_prod INTEGER NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1,
            foto BLOB,
            foto_mime TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Conta (
            id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao_conta TEXT NOT NULL,
            valor_conta REAL NOT NULL,
            vencimento TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Compra (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            data_compra TEXT NOT NULL,
            preco_total REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Venda (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda TEXT NOT NULL,
            preco_total REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SaldoDiario (
            saldo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_saldo REAL,
            data_saldo TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProdutoVendido (
            produto_id INTEGER,
            venda_id INTEGER,
            quantidade_vendida INTEGER NOT NULL,
            PRIMARY KEY (produto_id, venda_id),
            FOREIGN KEY (produto_id) REFERENCES Produto(id_prod),
            FOREIGN KEY (venda_id) REFERENCES Venda(id_venda) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProdutoComprado (
            produto_id INTEGER,
            compra_id INTEGER,
            quantidade_comprada INTEGER NOT NULL,
            PRIMARY KEY (produto_id, compra_id),
            FOREIGN KEY (produto_id) REFERENCES Produto(id_prod),
            FOREIGN KEY (compra_id) REFERENCES Compra(id_compra) ON DELETE CASCADE
        )
    """)

    # Migração simples para bancos criados por versões anteriores.
    colunas_produto = {row[1] for row in cursor.execute("PRAGMA table_info(Produto)").fetchall()}
    if "foto" not in colunas_produto:
        cursor.execute("ALTER TABLE Produto ADD COLUMN foto BLOB")
    if "foto_mime" not in colunas_produto:
        cursor.execute("ALTER TABLE Produto ADD COLUMN foto_mime TEXT")

    connector.commit()
    connector.close()
