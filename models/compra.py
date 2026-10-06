from models.movimentacao import Movimentacao


class Compra(Movimentacao):
    def __init__(self, produtos):
        super().__init__(produtos)

    def calcularPrecoFinal(self):
        preco_final = 0
        for i in self.produtos:
            preco_final += i[1] * i[2]
        return preco_final

    def getInformacoes(self):
        return self.produtos, self.preco_final, self.data
