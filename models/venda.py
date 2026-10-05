from .movimentacao import Movimentacao


class Venda(Movimentacao):
    def __init__(self, codigo, preco, quantidade):
        super().__init__(codigo, preco, quantidade)

    def calcularPrecoFinal(self):
        preco_final = self.preco * self.quantidade
        return preco_final

    def getInformacoes(self):
        return self.codigo, self.preco, self.quantidade, self.preco_final, self.data

    def __str__(self):
        return f'''Venda realizada em {self.data}
Cód: {self.codigo} - Preço: R$ {self.preco:.2f} - Quant: {self.quantidade}
Total: R$ {self.preco_final:.2f}'''