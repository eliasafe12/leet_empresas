from .movimentacao import Movimentacao
class Venda(Movimentacao):
    def __init__(self, produtos):
        super().__init__(produtos)
        
    def calcularPrecoFinal(self):
        preco_final = 0
        for i in self.produtos:
            preco_final += i[1] * i[2] # preço * quantidade
        return preco_final
    
    def getValor(self): return self.preco_final # para fazer o saldo diario

    def __str__(self):
        msg = f"Venda realizada em {self.data}\n"
        for i in self.produtos:
            msg += f"Cód: {i[0]} - Preço: R$ {i[1]:.2f} - Quant: {i[2]}\n"
        msg += f"R$ {self.preco_final:.2f}"
        return msg