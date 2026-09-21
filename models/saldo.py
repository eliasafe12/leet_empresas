class Saldo():
    def __init__(self, *args):
        self.valores = list(args)
        self.saldo = calcularSaldoFinal()

    def calcularSaldoFinal(self):
        for i in self.valores:
            saldoFinal += i
        return saldoFinal