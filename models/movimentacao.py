# classe pai de compra e venda
# importa recursos para criar uma classe abstrata
from abc import ABC, abstractmethod
# importa recursos para registrar a data e a hora da movimentação
from datetime import datetime

# guarda os atributos comuns de compra e venda: os produtos, o preço final e a data
class Movimentacao(ABC): # compra e venda
    def __init__(self, produtos):
        # guarda a lista de produtos, em que cada item é uma tupla com código, preço e quantidade
        self.produtos = produtos
        # calcula o preço final usando a regra definida por cada classe filha
        self.preco_final = self.calcularPrecoFinal()
        tempo = datetime.now() # pega a data e hora da venda
        # guarda a data e a hora no formato dia/mês/ano hora:minuto
        self.data = tempo.strftime('%Y-%m-%d %H:%M:%S')

    # obriga as classes filhas a implementar o cálculo do preço final
    @abstractmethod
    def calcularPrecoFinal(self): pass
    # obriga as classes filhas a devolver suas informações
    @abstractmethod
    def getInformacoes(self): pass
   