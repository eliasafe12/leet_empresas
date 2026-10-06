import sqlite3
from leet_connect import conectar
# arquivo placeholder utilizado para testes por enquanto

def selectUsuario(user_id):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("select * from Usuario where user_id = ?",(user_id,))
    return cursor.fetchone()
    connector.close()
    cursor.close()

def insertUsuario(user_id, nome_empresa, senha):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("insert into Usuario (user_id, nome_empresa, senha) Values (?, ?, ?)",(user_id, nome_empresa, senha))
    connector.commit()
    connector.close()

def insertProduto(nome, valor_custo, valor_venda, quant):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("insert into Produto (nome_prod, valor_custo, valor_venda, quant_prod) Values (?, ?, ?, ?)",(nome, valor_custo, valor_venda, quant))
    connector.commit()
    connector.close()

def selectProdutos():
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("select * from Produto")
    return cursor.fetchall()
    connector.close()
    cursor.close()

def buscarProduto(id_prod):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("select * from Produto where id_prod = ?",(id_prod,))
    return cursor.fetchone()
    connector.close()
    cursor.close()

def updatePrecoVenda(id_prod, valor):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (valor, id_prod))
    connector.commit()
    connector.close()

def updatePrecoCusto(id_prod, valor):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("update Produto set valor_custo = ? where id_prod = ?", (valor, id_prod))
    connector.commit()
    connector.close()

def insertVenda(venda):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("INSERT INTO Venda (data_venda, preco_total) VALUES (?, ?)", (venda.data, venda.preco_final))
    venda_id = cursor.lastrowid
    for produto in venda.produtos:
        produto_id = produto[0]
        quantidade = produto[2]
        cursor.execute("INSERT INTO ProdutoVendido (produto_id, venda_id, quantidade_vendida) VALUES (?, ?, ?)", (produto_id,venda_id,quantidade))
    connector.commit()
    connector.close()

def selectVendas():
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM Venda")
    return cursor.fetchall()
    connector.close()
    cursor.close()

def insertCompra(compra):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("INSERT INTO Compra (preco_total, data_compra) VALUES (?, ?)", (compra.preco_final, compra.data))
    compra_id = cursor.lastrowid
    for produto in compra.produtos:
        produto_id = produto[0]
        quantidade = produto[2]
        cursor.execute("INSERT INTO ProdutoComprado (produto_id, compra_id, quantidade_comprada) VALUES (?, ?, ?)", (produto_id, compra_id, quantidade))
    connector.commit()
    connector.close()

def selectCompras():
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM Compra")
    return cursor.fetchall()
    connector.close()
    cursor.close()

def updateEstoque(id_prod, quantidade, tipo):
    connector = conectar()
    cursor = connector.cursor()
    if tipo == "Venda":
        cursor.execute("UPDATE Produto SET quant_prod = quant_prod - ? WHERE id_prod = ?", (quantidade, id_prod))
    elif tipo == "Compra":
        cursor.execute("UPDATE Produto SET quant_prod = quant_prod + ? WHERE id_prod = ?", (quantidade, id_prod))
    connector.commit()
    connector.close()

def deleteProduto(id_prod):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("delete from Produto where id_prod = ?",(id_prod,))
    connector.commit()
    connector.close()

def updatePreco(id_prod, valor):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (valor, id_prod))
    connector.commit()
    connector.close()

def insertConta(descricao, valor, vencimento):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("insert into Conta (descricao_conta, valor_conta, vencimento) Values (?, ?, ?)",(descricao, valor, vencimento))
    connector.commit()
    connector.close()

def selectContas():
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("select * from Conta")
    return cursor.fetchall()
    connector.close()
    cursor.close()