class SaldoDiario():
    def __init__(self, user_id, vendas, compras, contas):
        self.user_id = user_id
        self.vendas = vendas
        self.compras = compras
        self.contas = contas
        self.saldo = self.calcularSaldoFinal()

    def calcularSaldoFinal(self):
        saldoFinal =0
        for i in self.vendas:
            saldoFinal += i.getValor()
        for i in self.compras:
            saldoFinal -= i.getValor()
        for i in self.contas:
            saldoFinal -= i.getValor()
        return saldoFinal

    def __str__(self):
        msg = f"Saldo:\n   Vendas:\n"
        for i in self.vendas:
            msg += f"R$ {i.getValor():.2f}\n"
        msg += f"   Compras:\n"
        for i in self.compras:
            msg += f"R$ {i.getValor():.2f}\n"
        msg += f"   Contas:\n"
        for i in self.contas:
            msg += f"R$ {i.getValor():.2f}\n"
        msg += f"Saldo final: R$ {self.saldo:.2f}"
        return msg