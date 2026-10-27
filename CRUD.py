# arquivo com as funções de criação, consulta, atualização e remoção de registros do banco de dados
# importa o módulo sqlite3 para tratar os erros do banco de dados
import sqlite3
# importa a função que abre a conexão com o banco de dados
from leet_connect import conectar
# importa o tipo decimal, que não chega a ser utilizado neste arquivo
from decimal import Decimal

def selectUsuario(user_id): # procura usuário por id
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # busca o usuário pelo nome de login, usando parâmetro para evitar sql injection
        cursor.execute("select * from Usuario where user_id = ?",(user_id,))
        # devolve o registro encontrado ou none quando o usuário não existe
        return cursor.fetchone()

def insertUsuario(user_id, nome_empresa, senha): # cadastra o usuário
    # abre a conexão com o banco de dados
    with conectar() as connector:
        # tenta cadastrar o usuário e trata o caso de nome de login repetido
        try:
            cursor = connector.cursor()
            # grava o usuário com a senha já criptografada
            cursor.execute("insert into Usuario (user_id, nome_empresa, senha) Values (?, ?, ?)",(user_id, nome_empresa, senha))
            # confirma as alterações no banco de dados
            connector.commit()
        # captura a violação da regra de unicidade do nome de login
        except sqlite3.IntegrityError:
            # converte o erro do banco em uma mensagem compreensível para o cadastro
            raise ValueError("Usuário já existe")

def insertProduto(nome, valor_custo, valor_venda, quant, foto=None, foto_mime=None): # cadastra o produto
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # grava o produto convertendo os preços para real e a quantidade para inteiro
        cursor.execute(
            "insert into Produto (nome_prod, valor_custo, valor_venda, quant_prod, foto, foto_mime) Values (?, ?, ?, ?, ?, ?)",
            (nome, float(valor_custo), float(valor_venda), int(quant), foto, foto_mime)
        )
        # confirma as alterações no banco de dados
        connector.commit()

def selectProdutos(): # seleciona os produtos cadastrados
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # seleciona somente os produtos ativos, sem trazer os bytes da foto
        cursor.execute("select id_prod, nome_prod, valor_custo, valor_venda, quant_prod, ativo, foto_mime from Produto where ativo = 1")
        # prepara a lista que receberá cada produto como dicionário
        produtos = []
        # percorre os registros encontrados
        for row in cursor.fetchall():
            # converte o registro em dicionário para poder acrescentar campos
            produto = dict(row)
            # cria o endereço da foto quando o produto possui uma e deixa vazio caso contrário
            produto["foto_url"] = (
                f"/produto/{produto['id_prod']}/foto"
                if produto.get("foto_mime") else None
            )
            # adiciona o produto à lista
            produtos.append(produto)
        # devolve a lista de produtos ativos
        return produtos

def buscarProduto(id_prod): # procura produto por id
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # procura o produto ativo com o código informado
        cursor.execute("select * from Produto where id_prod = ? and ativo = 1", (id_prod,))
        row = cursor.fetchone()
        # devolve o produto como dicionário ou none quando não for encontrado
        return dict(row) if row else None

def updatePrecoVenda(id_prod, valor): # atualiza preço de venda
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # altera o preço de venda do produto
        cursor.execute("update Produto set valor_venda = ? where id_prod = ?", (round(float(valor), 2), id_prod))
        # confirma as alterações no banco de dados
        connector.commit()

def updatePrecoCusto(id_prod, valor): # atualiza preço de compra
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # altera o preço de custo do produto
        cursor.execute("update Produto set valor_custo = ? where id_prod = ?", (round(float(valor), 2), id_prod))
        # confirma as alterações no banco de dados
        connector.commit()

def insertVenda(venda): # cadastra venda
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # grava a venda com a data e o preço total calculados pela classe venda
        cursor.execute("INSERT INTO Venda (data_venda, preco_total) VALUES (?, ?)", (venda.data, round(float(venda.preco_final), 2)))
        # guarda o código gerado para a venda para ligá-la aos produtos
        venda_id = cursor.lastrowid
        for produto in venda.produtos: # cadastra os produtos vendidos
            # cada item é uma tupla com o código do produto, o preço unitário e a quantidade
            produto_id = produto[0]
            quantidade = produto[2]
            # retira do estoque somente quando há quantidade suficiente no produto ativo
            cursor.execute("UPDATE Produto SET quant_prod = quant_prod - ? WHERE id_prod = ? AND ativo = 1 AND quant_prod >= ?", (int(quantidade), produto_id, int(quantidade)))
            # interrompe a operação para impedir estoque negativo ou venda de produto inativo
            if cursor.rowcount == 0:
                raise ValueError("Estoque insuficiente ou produto indisponível")
            # registra a quantidade vendida de cada produto na venda
            cursor.execute("INSERT INTO ProdutoVendido (produto_id, venda_id, quantidade_vendida) VALUES (?, ?, ?)", (produto_id,venda_id,int(quantidade)))

def buscarFotoProduto(id_prod): # busca a foto do produto
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # busca os bytes da foto e o tipo dela para o produto ativo
        cursor.execute("SELECT foto, foto_mime FROM Produto WHERE id_prod = ? AND ativo = 1", (id_prod,))
        # devolve a foto e o tipo dela ou none quando o produto não existe
        return cursor.fetchone()


def selectVendas(): # seleciona as vendas cadastradas
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # seleciona todas as vendas cadastradas
        cursor.execute("SELECT * FROM Venda")
        # devolve a lista com todos os registros encontrados
        return cursor.fetchall()

def insertCompra(compra): # cadastra compra
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # grava a compra com a data e o preço total calculados pela classe compra
        cursor.execute("INSERT INTO Compra (preco_total, data_compra) VALUES (?, ?)", (round(float(compra.preco_final), 2), compra.data))
        # guarda o código gerado para a compra para ligá-la aos produtos
        compra_id = cursor.lastrowid
        for produto in compra.produtos: # cadastra os produtos comprados
            produto_id = produto[0]
            quantidade = produto[2]
            # registra a quantidade comprada de cada produto na compra
            cursor.execute("INSERT INTO ProdutoComprado (produto_id, compra_id, quantidade_comprada) VALUES (?, ?, ?)", (produto_id, compra_id, int(quantidade)))
            # soma ao estoque a quantidade comprada
            cursor.execute("UPDATE Produto SET quant_prod = quant_prod + ? WHERE id_prod = ? AND ativo = 1", (int(quantidade), produto_id))
            if cursor.rowcount == 0:
                raise ValueError("Produto indisponível para compra")

def selectCompras(): # seleciona as compras
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # seleciona todas as compras cadastradas
        cursor.execute("SELECT * FROM Compra")
        # devolve a lista com todos os registros encontrados
        return cursor.fetchall()

def deleteItem(id_item, tipo_item): # deleta item por tipo
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # escolhe o que remover de acordo com o tipo informado
        if tipo_item == "produto":
            # marca o produto como inativo em vez de apagá-lo, preservando o histórico de vendas e compras
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
            # verifica se a remoção da compra deixaria algum estoque negativo
            for item in itens:
                cursor.execute("SELECT quant_prod FROM Produto WHERE id_prod = ?", (item["produto_id"],))
                produto = cursor.fetchone()
                if not produto or produto["quant_prod"] < item["quantidade_comprada"]:
                    raise ValueError("Não é possível remover a compra: o estoque já foi consumido")
            # retira do estoque aquilo que foi comprado após validar todos os itens
            for item in itens:
                cursor.execute("UPDATE Produto SET quant_prod = quant_prod - ? WHERE id_prod = ? AND quant_prod >= ?", (item["quantidade_comprada"], item["produto_id"], item["quantidade_comprada"]))
                if cursor.rowcount == 0:
                    raise ValueError("Não é possível remover a compra: estoque insuficiente")
            # Remove os itens relacionados
            cursor.execute("DELETE FROM ProdutoComprado WHERE compra_id = ?",(id_item,))
            # Remove a compra
            cursor.execute("DELETE FROM Compra WHERE id_compra = ?",(id_item,))
        elif tipo_item == "conta":
            # apaga a conta definitivamente
            cursor.execute("DELETE FROM Conta WHERE id_conta = ?",(id_item,))
        elif tipo_item == "saldo":
            # apaga um saldo diário pelo identificador
            cursor.execute("DELETE FROM SaldoDiario WHERE saldo_id = ?", (id_item,))
        else:
            # interrompe a remoção quando o tipo não é reconhecido
            raise ValueError("Tipo de item inválido")

        # impede informar sucesso quando nenhum registro corresponde ao código
        if cursor.rowcount == 0:
            raise ValueError("Item não encontrado")
        # confirma as alterações no banco de dados
        connector.commit()


def insertConta(descricao, valor, vencimento): # cadastra conta
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # grava a conta com a descrição, o valor e a data de vencimento
        cursor.execute("insert into Conta (descricao_conta, valor_conta, vencimento) Values (?, ?, ?)", (descricao, round(float(valor), 2), vencimento))
        # confirma as alterações no banco de dados
        connector.commit()

def selectContas(): # seleciona as contas
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # seleciona todas as contas cadastradas
        cursor.execute("select * from Conta")
        # devolve a lista com todos os registros encontrados
        return cursor.fetchall()

def insertSaldoDiario(valor,data): # cadastra o saldo diario
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # grava o saldo com a data em que ele foi salvo
        cursor.execute("insert into SaldoDiario (valor_saldo, data_saldo) values(?, ?)", (round(float(valor), 2), data))
        # confirma as alterações no banco de dados
        connector.commit()

def selectSaldos(): # seleciona os saldos diarios
    # abre a conexão com o banco de dados
    with conectar() as connector:
        cursor = connector.cursor()
        # seleciona todos os saldos diários salvos
        cursor.execute("select * from SaldoDiario")
        # devolve a lista com todos os registros encontrados
        return cursor.fetchall()
