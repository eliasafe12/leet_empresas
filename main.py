from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta
from models.saldo import SaldoDiario

produtos = []
vendas = []
compras = []
contas = []

while True:
    a = int(input('''
1 - Cadastrar Produto
2 - Ver produtos
3 - Excluir Produto
4 - Atualizar preço do produto
5 - Cadastrar venda realizada
6 - Cadastrar compra realizada
7 - Cadastrar Conta a pagar
8 - Listar contas
9 - Fazer Saldo do dia
10 - Sair
'''))
    match a:
        case 1:
            nome, codigo, preco, quantidade = list(map(str, input("Nome, Código, Preço e Quantidade: ").split())) 
            for i in produtos: # verifica se não tem um produto com o mesmo código
                if i.codigo == int(codigo):
                    cod_valido = False
                    break
            else: cod_valido = True
            if cod_valido:
                produtos.append(Produto(nome,int(codigo),float(preco),int(quantidade))) # cadastra o produto
                print("Produto Cadastrado!")
            else: print("Código já existente")
            
        case 2:
            print("Produtos:")
            for i in produtos:
                print(i)    
        
        case 3:
            print("Produtos:")
            for i in produtos:
                print(i)    
            codigo = int(input("Código do produto a ser excluído: "))
            for i in produtos:
                if i.codigo == codigo:
                    produtos.remove(i)
                    print("Produto removido!")
                    break
            else: print("Produto não encontrado!")

        case 4:
            print("Produtos:")
            for i in produtos:
                print(i)    
            codigo = int(input("Produto a ser atualizado: "))
            for i in produtos:
                if i.codigo == codigo:
                    print(i)
                    preco = float(input("Novo preço: "))
                    atualizacao = i.atualizarPreco(preco)
                    print(atualizacao)
                    break
            else: print("Produto não encontrado!")

        case 5:
            venda_produtos = []
            quant_produtos = int(input("Quantos produtos foram vendidos? "))
            for i in range(quant_produtos):
                prod = list(map(int, input("Código e quantidade do produto: ").split()))
                for j in produtos:
                    if prod[0] == j.codigo and prod[1] <= j.quantidade:
                        venda_produtos.append((prod[0], j.preco, prod[1]))
                        j.alterarEstoque("Venda", prod[1])
                        break
                else: 
                    print("Produto ou quantidade inválida")
                    break
            vendas.append(Venda(venda_produtos))
            print(vendas[-1])

        case 6:
            compra_produtos = []
            quant_produtos = int(input("Quantos produtos foram comprados? "))
            for i in range(quant_produtos):
                prod = list(map(int, input("Código e quantidade do produto: ").split()))
                for j in produtos:
                    if prod[0] == j.codigo:
                        compra_produtos.append((prod[0], j.preco, prod[1]))
                        j.alterarEstoque("Compra", prod[1])
                        break
                else: 
                    print("Produto inválido")
                    break
            compras.append(Compra(compra_produtos))
            print(compras[-1])
            
        case 7: 
            descricao = input("Qual a conta? ")
            valor = float(input("Qual o valor? "))
            vencimento = input("Quando vence? ")
            contas.append(Conta(descricao, valor, vencimento))
            print("Conta cadastrada!")

        case 8:
            print("Contas")
            for i in contas:
                print(i)

        case 9:
            saldo_diario = SaldoDiario(vendas,compras,contas)
            print(saldo_diario)

        case 10:
            break


