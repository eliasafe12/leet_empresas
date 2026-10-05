from models.movimentacao import Movimentacao


class Compra(Movimentacao):
    def __init__(self, user_id, produtos):
        super().__init__(user_id, produtos)

    def calcularPrecoFinal(self):
        preco_final = 0
        for codigo, preco, quantidade in self.produtos:
            preco_final += preco * quantidade
        return preco_final

    def getValor(self):
        return self.preco_final

    def __str__(self):
        msg = f"Compra realizada em {self.data}\n"

        for codigo, preco, quantidade in self.produtos:
            msg += (f"Cód: {codigo} - Preço: R$ {preco:.2f} - Quant: {quantidade}\n")

        msg += f"Total: R$ {self.preco_final:.2f}"

        return msg