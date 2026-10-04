import sqlite3

connector = sqlite3.connect('leet.db',detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
cursor = connector.cursor()

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
                                        desc_conta Text Not Null,
                                        valor_conta Real Not Null,
                                        vencimento Text Not Null)""")

cursor.execute("""create table Compra (id_conta Integer Primary Key,
                                        )""")

cursor.execute("""create table Venda (id_venda Integer Primary Key,
                                        foreign key (id_prodVendido) references Produto (id_prod),
                                        )""")

cursor.execute("""create table Saldo (id_saldo Integer Primary Key,
                                        )""")


#CREATE TABLE Produto 
#( 
# produto_id INT PRIMARY KEY,  
# iduser INT,  
# nome VARCHAR,  
# preço FLOAT,  
# quantidade INT,  
#); 
#
#CREATE TABLE user 
#( 
# user_id INT PRIMARY KEY,  
#); 
#
#CREATE TABLE venda 
#( 
# venda_id INT PRIMARY KEY,  
# iduser INT,  
#); 
#
#CREATE TABLE vend_prods 
#( 
# produtos VARCHAR PRIMARY KEY,  
# venda_id INT,  
#); 
#
#CREATE TABLE compra 
#( 
# compra_id INT PRIMARY KEY,  
# iduser INT,  
#); 
#
#CREATE TABLE com_prods 
#( 
# produtos VARCHAR PRIMARY KEY,  
# compra_id INT,  
#); 
#
#CREATE TABLE conta 
#( 
# conta_id INT PRIMARY KEY,  
# iduser INT,  
# desc VARCHAR,  
# valor FLOAT,  
# vencimento DATE,  
#); 
#
#CREATE TABLE saldo 
#( 
# saldo_id INT PRIMARY KEY,  
# iduser INT,  
# valor_saldo FLOAT,  
# data_saldo DATETIME,  
#); 
#
#CREATE TABLE ProdutoComprado 
#( 
# compra_id INT PRIMARY KEY,  
# produto_id INT PRIMARY KEY,  
#); 
#
#CREATE TABLE ProdutoVendido 
#( 
# produto_id INT PRIMARY KEY,  
# venda_id INT PRIMARY KEY,  
#); 
#
#ALTER TABLE Produto ADD FOREIGN KEY(iduser) REFERENCES user (iduser);
#ALTER TABLE venda ADD FOREIGN KEY(iduser) REFERENCES user (iduser);
#ALTER TABLE vend_prods ADD FOREIGN KEY(venda_id) REFERENCES venda (venda_id);
#ALTER TABLE compra ADD FOREIGN KEY(iduser) REFERENCES user (iduser);
#ALTER TABLE com_prods ADD FOREIGN KEY(compra_id) REFERENCES compra (compra_id);
#ALTER TABLE conta ADD FOREIGN KEY(iduser) REFERENCES user (iduser);
#ALTER TABLE saldo ADD FOREIGN KEY(iduser) REFERENCES user (iduser);
#ALTER TABLE ProdutoComprado ADD FOREIGN KEY(compra_id) REFERENCES compra (compra_id);
#ALTER TABLE ProdutoComprado ADD FOREIGN KEY(produto_id) REFERENCES Produto (produto_id);
#ALTER TABLE ProdutoVendido ADD FOREIGN KEY(produto_id) REFERENCES Produto (produto_id);
#ALTER TABLE ProdutoVendido ADD FOREIGN KEY(venda_id) REFERENCES venda (venda_id);


#cursor.commit()
#cursor.close()
#connector.close()
