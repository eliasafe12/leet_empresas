class Produto:
    def __init__(self, nome, codigo, valor_custo, valor_venda, quantidade):
        self.nome = nome
        self.codigo = codigo
        self.valor_custo = valor_custo
        self.valor_venda = valor_venda
        self.quantidade = max(0, quantidade)

    def avisarFalta(self):
        if self.quantidade == 0:
            return f"{self.nome} esgotado!"
        elif self.quantidade <= 5:
            return f"{self.nome} acabando!"
        else:
            return f"{self.nome} tem estoque: {self.quantidade}"

    def alterarEstoque(self, tipo, quant):
        if quant <= 0:
            return False
        if tipo == "Venda":
            if quant > self.quantidade:
                return False
            self.quantidade -= quant
            return True
        elif tipo == "Compra":
            self.quantidade += quant
            return True
        return False

    def atualizarPreco(self, novo_preco):
        if novo_preco < 0:
            return "Preço inválido"

        self.valor_venda = novo_preco
        return "Preço atualizado!"

    def getInformacoes(self):
        return self.nome, self.valor_custo, self.valor_venda, self.quantidade

    def __str__(self):
        return (
            f"Nome: {self.nome} - "
            f"Código: {self.codigo} - "
            f"Preço: R$ {self.valor_venda:.2f} - "
            f"Quantidade: {self.quantidade}"
        )