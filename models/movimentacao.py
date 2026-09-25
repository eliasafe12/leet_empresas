from abc import ABC, abstractmethod
from datetime import datetime

class Movimentacao(ABC): # compra e venda
    def __init__(self, produtos):
        self.produtos = list(produtos)
        self.preco_final = self.calcularPrecoFinal()
        tempo = datetime.now() # pega a data e hora da venda
        self.data = tempo.strftime('%d/%m/%Y %H:%M')

    @abstractmethod
    def calcularPrecoFinal(self): pass
    @abstractmethod
    def getValor(self): pass