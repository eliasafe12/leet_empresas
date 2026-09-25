from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta

produtos = []
vendas = []

while True:
    a = int(input('''
1 - Cadastrar Produto
2 - Ver produtos
3 - Cadastrar venda realizada
4 - Cadastrar compra realizada
5 - Cadastrar Conta
6 - Fazer Saldo do dia
7 - Sair
'''))
    match a:
        case 1:
            nome, codigo, preco, quantidade = list(map(str, input("Nome, Código, Preço e Quantidade: ").split())) 
            for i in produtos: # verifica se não tem um produto com o mesmo código
                if i.codigo == codigo:
                    cod_valido = False
                    break
            else: cod_valido = True
            if cod_valido:
                produtos.append(Produto(nome,int(codigo),int(preco),int(quantidade))) # cadastra o produto
                print("Produto Cadastrado!")
            else: print("Código já existente")
            
        case 2:
            print("Produtos:")
            for i in produtos:
                print(i)    
        case 3:
            venda_produtos = []
            quant_produtos = int(input("Quantos produtos foram vendidos? "))
            for i in range(quant_produtos):
                prod = list(map(int, input("Código e quantidade do produto: ").split()))
                for j in produtos:
                    if prod[0] == j.codigo and prod[1] <= j.quantidade:
                        venda_produtos.append((prod[0], j.preco, prod[1]))
                        break
                else: print("Produto ou quantidade inválida")
            vendas.append(Venda(venda_produtos))
            print(vendas[-1])
            


