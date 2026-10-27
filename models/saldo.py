# representa o saldo do dia, calculado a partir das vendas, das compras e das contas
# valores ausentes são tratados como zero
class SaldoDiario():
    def __init__(self, vendas=None, compras=None, contas=None):
        # troca os valores não informados por zero
        if vendas is None:
            vendas = 0
        if compras is None:
            compras = 0
        if contas is None:
            contas = 0
        # guarda os totais recebidos
        self.vendas = vendas
        self.compras = compras
        self.contas = contas
        # calcula o saldo assim que o objeto é criado
        self.saldo = self.calcularSaldoFinal()

    # calcula o saldo subtraindo as compras e as contas do total de vendas
    def calcularSaldoFinal(self):
        saldoFinal = self.vendas - self.compras - self.contas
        # devolve o saldo final do dia
        return saldoFinal

    