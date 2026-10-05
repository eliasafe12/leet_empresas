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

def insertVenda(codigo, preco, quantidade, preco_final, data):
    connector = conectar()
    cursor = connector.cursor()
    cursor.execute("insert into Venda (codigo_prod, preco_unitario, quant_venda, preco_final, data_venda) Values (?, ?, ?, ?, ?)",(codigo, preco, quantidade, preco_final, data))
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