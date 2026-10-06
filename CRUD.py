import sqlite3
from leet_connect import conectar
# arquivo placeholder utilizado para testes por enquanto

def selectUsuario(user_id):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Usuario where user_id = ?",(user_id,))
        return cursor.fetchone()

def insertUsuario(user_id, nome_empresa, senha):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("insert into Usuario (user_id, nome_empresa, senha) Values (?, ?, ?)",(user_id, nome_empresa, senha))
        connector.commit()

def insertProduto(nome, valor_custo, valor_venda, quant):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("insert into Produto (nome_prod, valor_custo, valor_venda, quant_prod) Values (?, ?, ?, ?)",(nome, valor_custo, valor_venda, quant))
        connector.commit()

def selectProdutos():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Produto where ativo = 1")
        return cursor.fetchall()

def buscarProduto(id_prod):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Produto where id_prod = ?",(id_prod,))
        return cursor.fetchone()

def updatePrecoVenda(id_prod, valor):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (valor, id_prod))
        connector.commit()

def updatePrecoCusto(id_prod, valor):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("update Produto set valor_custo = ? where id_prod = ?", (valor, id_prod))
        connector.commit()

def insertVenda(venda):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("INSERT INTO Venda (data_venda, preco_total) VALUES (?, ?)", (venda.data, venda.preco_final))
        venda_id = cursor.lastrowid
        for produto in venda.produtos:
            produto_id = produto[0]
            quantidade = produto[2]
            cursor.execute("INSERT INTO ProdutoVendido (produto_id, venda_id, quantidade_vendida) VALUES (?, ?, ?)", (produto_id,venda_id,quantidade))
            cursor.execute("UPDATE Produto SET quant_prod = quant_prod - ? WHERE id_prod = ?", (quantidade, produto_id))
    connector.commit()
    connector.close()

def selectVendas():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("SELECT * FROM Venda")
        return cursor.fetchall()

def insertCompra(compra):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("INSERT INTO Compra (preco_total, data_compra) VALUES (?, ?)", (compra.preco_final, compra.data))
        compra_id = cursor.lastrowid
        for produto in compra.produtos:
            produto_id = produto[0]
            quantidade = produto[2]
            cursor.execute("INSERT INTO ProdutoComprado (produto_id, compra_id, quantidade_comprada) VALUES (?, ?, ?)", (produto_id, compra_id, quantidade))
            cursor.execute("UPDATE Produto SET quant_prod = quant_prod + ? WHERE id_prod = ?", (quantidade, produto_id))
    connector.commit()
    connector.close()

def selectCompras():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("SELECT * FROM Compra")
        return cursor.fetchall()

def deleteItem(id_prod, tipo_item):
    with conectar() as connector:
        cursor = connector.cursor()
        if tipo_item == "produto":
            cursor.execute("UPDATE Produto SET ativo = 0 WHERE id_prod = ?", (id_prod,))
        elif tipo_item == "venda":
            cursor.execute("DELETE FROM Venda WHERE id_venda = ?", (id_prod,))
        elif tipo_item == "compra":
            cursor.execute("DELETE FROM Compra WHERE id_compra = ?", (id_prod,))
        elif tipo_item == "conta":
            cursor.execute("DELETE FROM Conta WHERE id_conta = ?", (id_prod,))
        else:
            raise ValueError("Tipo de item inválido")
        connector.commit()

def updatePreco(id_prod, valor):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (valor, id_prod))
        connector.commit()

def insertConta(descricao, valor, vencimento):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("insert into Conta (descricao_conta, valor_conta, vencimento) Values (?, ?, ?)", (descricao, valor, vencimento))
        connector.commit()

def selectContas():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Conta")
        return cursor.fetchall()

