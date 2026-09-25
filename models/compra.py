from models.movimentacao import Movimentacao
class Compra(Movimentacao):
    def __init__(self, produtos):
        super().__init__(produtos)

    def calcularPrecoFinal(self):
        preco_final = 0
        for i in self.produtos:
            preco_final += i[1] * i[2] # preço * quantidade
        return preco_final

    def getValor(self): return -(self.valor) # para fazer o saldo diario    