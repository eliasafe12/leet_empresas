# arquivo responsável pela conexão com o banco de dados e pela criação das tabelas
# importa o módulo sqlite3 para criar e acessar o banco de dados local
import sqlite3
# importa recursos para localizar o diretório pessoal do usuário
from pathlib import Path

# define a pasta pessoal onde ficam o banco de dados e os demais arquivos do aplicativo
diretorio_atual = Path.home()/".leet_empresas"
diretorio_atual.mkdir(parents=True, exist_ok=True) # cria pasta para arquivos do projeto
# define o caminho do arquivo do banco de dados sqlite
banco_dados = diretorio_atual/"leet.db" 

#arquivo utilizado para a criação das tabelas.

# gerencia commit, rollback e fechamento automático das conexões usadas com with
class ConexaoSQLite(sqlite3.Connection):
    def __exit__(self, tipo_erro, valor_erro, traceback):
        try:
            return super().__exit__(tipo_erro, valor_erro, traceback)
        finally:
            self.close()

# abre uma nova conexão com o banco de dados e a devolve já configurada
def conectar():
    connector = sqlite3.connect(banco_dados, detect_types=sqlite3.PARSE_DECLTYPES |
                                 sqlite3.PARSE_COLNAMES, factory=ConexaoSQLite) # cria ou inicializa banco de dados
    # permite acessar as colunas de cada registro pelo nome, como em um dicionário
    connector.row_factory = sqlite3.Row
    # cria o cursor usado para enviar o comando de configuração
    cursor = connector.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;") # ativa chaves estrangeiras
    # devolve a conexão para quem a chamou, que fica responsável por usá-la e encerrá-la
    return connector

#tipos de variaveis sqlite:
#NULL
#INTEGER
#REAL
#TEXT
#BLOB

# cria todas as tabelas do sistema quando elas ainda não existem
def inicializar_banco(): #cria ou inicializa as tabelas 
    # abre a conexão usada para criar as tabelas
    connector = conectar()
    cursor = connector.cursor()

    # tabela de usuários cadastrados, com a senha guardada em formato de hash
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            nome_empresa TEXT NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # tabela de produtos, em que o campo ativo marca a remoção sem apagar o histórico e a foto é guardada em bytes
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

    # tabela de contas a pagar com a data de vencimento
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Conta (
            id_conta INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao_conta TEXT NOT NULL,
            valor_conta REAL NOT NULL,
            vencimento TEXT NOT NULL
        )
    """)

    # tabela de compras de produtos para o estoque
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Compra (
            id_compra INTEGER PRIMARY KEY AUTOINCREMENT,
            data_compra TEXT NOT NULL,
            preco_total REAL NOT NULL
        )
    """)

    # tabela de vendas realizadas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Venda (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda TEXT NOT NULL,
            preco_total REAL NOT NULL
        )
    """)

    # tabela com os saldos diários salvos pelo usuário
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SaldoDiario (
            saldo_id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor_saldo REAL,
            data_saldo TEXT NOT NULL
        )
    """)

    # tabela que liga cada venda aos produtos vendidos e às quantidades, apagando os itens junto com a venda
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

    # tabela que liga cada compra aos produtos comprados e às quantidades, apagando os itens junto com a compra
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

    # remove saldos nulos gravados por versões antigas que poderiam quebrar o painel
    cursor.execute("DELETE FROM SaldoDiario WHERE valor_saldo IS NULL")

    # Migração simples para bancos criados por versões anteriores.
    # lê os nomes das colunas que a tabela produto possui atualmente
    colunas_produto = {row[1] for row in cursor.execute("PRAGMA table_info(Produto)").fetchall()}
    # adiciona a coluna da foto caso o banco tenha sido criado antes dela existir
    if "foto" not in colunas_produto:
        cursor.execute("ALTER TABLE Produto ADD COLUMN foto BLOB")
    # adiciona a coluna do tipo da foto caso ela ainda não exista
    if "foto_mime" not in colunas_produto:
        cursor.execute("ALTER TABLE Produto ADD COLUMN foto_mime TEXT")

    # confirma a criação das tabelas e encerra a conexão
    connector.commit()
    connector.close()
