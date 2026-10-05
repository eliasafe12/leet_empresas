import sqlite3

# arquivo placeholder utilizado para testes por enquanto

connector = sqlite3.connect('leet.db',detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
cursor = connector.cursor()
insertProd = "insert into Produto (nome_prod, valor_prod, quant_prod) Values (?, ?, ?)"
cursor.execute(insertProd, ('Nome do Produto',25 ,100 ))
cursor.execute("insert into Conta (descricao_conta, valor_conta, vencimento) Values ('aa',25 ,'01/01/2000' )")
cursor.execute("insert into Compra (id_compra) Values (NULL)")
cursor.execute("insert into Venda (id_venda) Values (NULL)")
cursor.execute("insert into SaldoDiario (valor_saldo, data_saldo) Values (0,'01/01/2000')")
cursor.execute("insert into ProdutoVendido Values (?,?)",(1,1))
cursor.execute("insert into ProdutoComprado Values (?,?)",(1,1))

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
