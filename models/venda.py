from .movimentacao import Movimentacao
class Venda(Movimentacao):
    def __init__(self, codigo, *args):
        super().__init__(codigo, *args)
        
    def calcularPrecoFinal(self):
        preco_final = 0
        for i in self.produtos:
            preco_final += i[1] * i[2] # preço * quantidade
        return preco_final
    
    def getValor(self): return self.valor # para fazer o saldo diario