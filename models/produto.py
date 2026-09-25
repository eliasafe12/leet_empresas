class Produto():
    def __init__(self, nome, codigo, preco, quantidade):
        self.nome = nome
        self.codigo = codigo
        self.preco = preco
        if quantidade < 0:
            self.quantidade = 0
        else: self.quantidade = quantidade

    def avisarFalta(self):
        if self.quantidade == 0: return f"{self.nome} esgotado!"
        elif self.quantidade <= 5: return f"{self.nome} acabando!"
        else: return f"{self.nome} tem estoque: {self.quantidade}"

    def getInformacoes(self): 
        return self.codigo, self.preco


    def __str__(self): return f'Nome: {self.nome} - Código: {self.codigo} - Preço: R${self.preco:.2f} - Quantidade: {self.quantidade}'