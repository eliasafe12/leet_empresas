class Produto:
    def __init__(self, nome, valor_custo, valor_venda, quantidade):
        self.nome = nome
        self.valor_custo = valor_custo
        self.valor_venda = valor_venda
        self.quantidade = max(0, quantidade)

    def avisarFalta(self):
        if self.quantidade == 0:
            return f"{self.nome} esgotado!"
        elif self.quantidade <= 5:
            return f"{self.nome} acabando! Estoque baixo: {self.quantidade} unidades."


    def getInformacoes(self):
        return self.nome, self.valor_custo, self.valor_venda, self.quantidade

