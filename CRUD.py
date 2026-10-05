import sqlite3
# arquivo usado somente para testes com o banco por enquanto

connector = sqlite3.connect('leet.db',detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
cursor = connector.cursor()

cursor.execute("insert into Produto Values (1,'Nome do Produto',25 ,100 )")
cursor.execute("insert into Conta Values (1,'aa',25 ,'01/01/2000' )")
cursor.execute("insert into Compra Values (1)")
cursor.execute("insert into Venda Values (1)")
cursor.execute("insert into SaldoDiario Values (1,0,'01/01/2000')")
cursor.execute("insert into ProdutoVendido Values (1,1)")
cursor.execute("insert into ProdutoComprado Values (1,1)")

connector.commit()

cursor.execute("select * from Produto")
print(cursor.fetchall())

cursor.execute("select * from Conta")
print(cursor.fetchall())

cursor.execute("select * from Compra")
print(cursor.fetchall())

cursor.execute("select * from Venda")
print(cursor.fetchall())

cursor.execute("select * from SaldoDiario")
print(cursor.fetchall())

cursor.execute("select * from ProdutoVendido")
print(cursor.fetchall())

cursor.execute("select * from ProdutoComprado")
print(cursor.fetchall())

