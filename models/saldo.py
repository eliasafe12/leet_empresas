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

    