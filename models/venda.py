# importa a classe pai que contém os atributos comuns de compra e venda
from .movimentacao import Movimentacao


# representa uma venda, que reduz o estoque dos produtos vendidos
class Venda(Movimentacao):
    def __init__(self, produtos):
        # repassa os produtos para a classe pai, que calcula o preço final e registra a data
        super().__init__(produtos) 

    # soma o valor de cada produto multiplicado pela quantidade vendida
    def calcularPrecoFinal(self):
        # começa o total em zero
        preco_final = 0
        # percorre os produtos, em que i[1] é o preço unitário e i[2] é a quantidade
        for i in self.produtos:
            preco_final += i[1] * i[2]
        # devolve o valor total da venda
        return preco_final

    # devolve os produtos, o preço final e a data da venda
    def getInformacoes(self):
        return self.produtos, self.preco_final, self.data

   