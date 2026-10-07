import sqlite3
from leet_connect import conectar
from decimal import Decimal
# arquivo placeholder utilizado para testes por enquanto

def selectUsuario(user_id):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Usuario where user_id = ?",(user_id,))
        return cursor.fetchone()

def insertUsuario(user_id, nome_empresa, senha):
    with conectar() as connector:
        try:
            cursor = connector.cursor()
            cursor.execute("insert into Usuario (user_id, nome_empresa, senha) Values (?, ?, ?)",(user_id, nome_empresa, senha))
            connector.commit()
        except sqlite3.IntegrityError:
            raise ValueError("Usuário já existe")

def insertProduto(nome, valor_custo, valor_venda, quant, foto=None, foto_mime=None):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute(
            "insert into Produto (nome_prod, valor_custo, valor_venda, quant_prod, foto, foto_mime) Values (?, ?, ?, ?, ?, ?)",
            (nome, float(valor_custo), float(valor_venda), int(quant), foto, foto_mime)
        )
        connector.commit()

def selectProdutos():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select id_prod, nome_prod, valor_custo, valor_venda, quant_prod, ativo, foto_mime from Produto where ativo = 1")
        produtos = []
        for row in cursor.fetchall():
            produto = dict(row)
            produto["foto_url"] = (
                f"/produto/{produto['id_prod']}/foto"
                if produto.get("foto_mime") else None
            )
            produtos.append(produto)
        return produtos

def buscarProduto(id_prod):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Produto where id_prod = ? and ativo = 1", (id_prod,))
        row = cursor.fetchone()
        return dict(row) if row else None

def updatePrecoVenda(id_prod, valor):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (float(valor), id_prod))
        connector.commit()

def updatePrecoCusto(id_prod, valor):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("update Produto set valor_custo = ? where id_prod = ?", (float(valor), id_prod))
        connector.commit()

def insertVenda(venda):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("INSERT INTO Venda (data_venda, preco_total) VALUES (?, ?)", (venda.data, float(venda.preco_final)))
        venda_id = cursor.lastrowid
        for produto in venda.produtos:
            produto_id = produto[0]
            quantidade = produto[2]
            cursor.execute("UPDATE Produto SET quant_prod = quant_prod - ? WHERE id_prod = ? AND ativo = 1", (int(quantidade), produto_id))
            cursor.execute("INSERT INTO ProdutoVendido (produto_id, venda_id, quantidade_vendida) VALUES (?, ?, ?)", (produto_id,venda_id,int(quantidade)))
    connector.commit()
    connector.close()

def buscarFotoProduto(id_prod):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("SELECT foto, foto_mime FROM Produto WHERE id_prod = ? AND ativo = 1", (id_prod,))
        return cursor.fetchone()


def selectVendas():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("SELECT * FROM Venda")
        return cursor.fetchall()

def insertCompra(compra):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("INSERT INTO Compra (preco_total, data_compra) VALUES (?, ?)", (float(compra.preco_final), compra.data))
        compra_id = cursor.lastrowid
        for produto in compra.produtos:
            produto_id = produto[0]
            quantidade = produto[2]
            cursor.execute("INSERT INTO ProdutoComprado (produto_id, compra_id, quantidade_comprada) VALUES (?, ?, ?)", (produto_id, compra_id, int(quantidade)))
            cursor.execute("UPDATE Produto SET quant_prod = quant_prod + ? WHERE id_prod = ? AND ativo = 1", (int(quantidade), produto_id))

def selectCompras():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("SELECT * FROM Compra")
        return cursor.fetchall()

def deleteItem(id_item, tipo_item):
    with conectar() as connector:
        cursor = connector.cursor()
        if tipo_item == "produto":
            cursor.execute("UPDATE Produto SET ativo = 0 WHERE id_prod = ?",(id_item,))
        elif tipo_item == "venda":
            # Recupera todos os produtos da venda
            cursor.execute("SELECT produto_id, quantidade_vendida FROM ProdutoVendido WHERE venda_id = ?", (id_item,))
            itens = cursor.fetchall()
            # Devolve cada quantidade ao estoque
            for item in itens:
                cursor.execute("UPDATE Produto SET quant_prod = quant_prod + ? WHERE id_prod = ?",(item["quantidade_vendida"], item["produto_id"]))
            cursor.execute("DELETE FROM ProdutoVendido WHERE venda_id = ?",(id_item,))
            # Remove a venda
            cursor.execute("DELETE FROM Venda WHERE id_venda = ?",(id_item,))
        elif tipo_item == "compra":
            # Recupera todos os produtos da compra
            cursor.execute("SELECT produto_id, quantidade_comprada FROM ProdutoComprado WHERE compra_id = ?",(id_item,))
            itens = cursor.fetchall()
            # Retira do estoque aquilo que foi comprado
            for item in itens:
                cursor.execute("UPDATE Produto SET quant_prod = quant_prod - ? WHERE id_prod = ?",(item["quantidade_comprada"], item["produto_id"]))
            # Remove os itens relacionados
            cursor.execute("DELETE FROM ProdutoComprado WHERE compra_id = ?",(id_item,))
            # Remove a compra
            cursor.execute("DELETE FROM Compra WHERE id_compra = ?",(id_item,))
        elif tipo_item == "conta":
            cursor.execute("DELETE FROM Conta WHERE id_conta = ?",(id_item,))
        else:
            raise ValueError("Tipo de item inválido")

        connector.commit()
def updatePreco(id_prod, valor):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (float(valor), id_prod))
        connector.commit()

def insertConta(descricao, valor, vencimento):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("insert into Conta (descricao_conta, valor_conta, vencimento) Values (?, ?, ?)", (descricao, float(valor), vencimento))
        connector.commit()

def selectContas():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from Conta")
        return cursor.fetchall()

def insertSaldoDiario(valor,data):
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("insert into SaldoDiario (valor_saldo, data_saldo) values(?, ?)", (float(valor), data))
        connector.commit()

def selectSaldos():
    with conectar() as connector:
        cursor = connector.cursor()
        cursor.execute("select * from SaldoDiario")
        return cursor.fetchall()
