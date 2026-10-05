import sqlite3

#arquivo utilizado para a criação das tabelas.

connector = sqlite3.connect('leet.db',detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
cursor = connector.cursor()

#tipos de variaveis sqlite:
#NULL
#INTEGER
#REAL
#TEXT
#BLOB

cursor.execute("""create table Produto (id_prod Integer Primary Key,
                                        nome_prod Text Not Null,
                                        valor_prod Real Not Null,
                                        quant_prod Integer Not Null)""")

cursor.execute("""create table Conta (id_conta Integer Primary Key,
                                        descricao_conta Text Not Null,
                                        valor_conta Real Not Null,
                                        vencimento Text Not Null)""")

cursor.execute("""create table Compra (id_conta Integer Primary Key
                                        )""")

cursor.execute("""create table Venda (id_venda Integer Primary Key
                                        )""")

cursor.execute("""CREATE TABLE SaldoDiario (
    saldo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_saldo REAL,
    data_saldo TEXT Not Null
);""")

cursor.execute("""CREATE TABLE ProdutoVendido (
    produto_id INTEGER,
    venda_id INTEGER,

    PRIMARY KEY (produto_id, venda_id),

    FOREIGN KEY (produto_id) REFERENCES Produto(produto_id),
    FOREIGN KEY (venda_id) REFERENCES Venda(venda_id)
);""")

cursor.execute("""CREATE TABLE ProdutoComprado (
    produto_id INTEGER,
    compra_id INTEGER,

    PRIMARY KEY (produto_id, compra_id),

    FOREIGN KEY (produto_id) REFERENCES Produto(produto_id),
    FOREIGN KEY (compra_id) REFERENCES Compra(compra_id)
);""")



cursor.close()
connector.close()
