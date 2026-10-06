class SaldoDiario():
    def __init__(self, vendas=None, compras=None, contas=None):
        if vendas is None:
            vendas = 0
        if compras is None:
            compras = 0
        if contas is None:
            contas = 0
        self.vendas = vendas
        self.compras = compras
        self.contas = contas
        self.saldo = self.calcularSaldoFinal()

    def calcularSaldoFinal(self):
        saldoFinal = self.vendas - self.compras - self.contas
        return saldoFinal

    def __str__(self):
        msg = f"Saldo:\n   Vendas:\n"
        for i in self.vendas:
            msg += f"R$ {i:.2f}\n"
        msg += f"   Compras:\n"
        for i in self.compras:
            msg += f"R$ {i:.2f}\n"
        msg += f"   Contas:\n"
        for i in self.contas:
            msg += f"R$ {i:.2f}\n"
        msg += f"Saldo final: R$ {self.saldo:.2f}"
        return msg