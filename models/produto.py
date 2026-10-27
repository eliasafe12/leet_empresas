# representa um produto do estoque
# guarda o nome, os preços de custo e de venda e a quantidade em estoque
class Produto:
    def __init__(self, nome, valor_custo, valor_venda, quantidade):
        self.nome = nome
        self.valor_custo = valor_custo
        self.valor_venda = valor_venda
        # impede que a quantidade do objeto seja negativa
        self.quantidade = max(0, quantidade)

    # devolve um aviso quando o produto está esgotado ou com estoque baixo
    def avisarFalta(self):
        # avisa que o produto acabou
        if self.quantidade == 0:
            return f"{self.nome} esgotado!"
        # avisa que o estoque está baixo quando restam cinco unidades ou menos
        elif self.quantidade <= 5:
            return f"{self.nome} acabando! Estoque baixo: {self.quantidade} unidades."


    # devolve os dados do produto na ordem usada para gravar no banco
    def getInformacoes(self):
        return self.nome, self.valor_custo, self.valor_venda, self.quantidade

