from datetime import datetime
class Conta():
    def __init__(self, descricao, valor, vencimento):
        self.descricao = descricao
        self.valor = valor
        self.vencimento = vencimento

    def avisarVencimento(self):
        tempo = datetime.now()
        if self.vencimento == tempo.strftime('%d/%m/%Y'):
            return f"{self.descricao} vence hoje!"
    
    def getValor(self): return -(self.valor) # para fazer o saldo diario

    def getInformacoes(self):
        return self.descricao, self.valor, self.vencimento