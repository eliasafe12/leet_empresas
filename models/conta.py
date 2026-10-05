from datetime import datetime
class Conta():
    def __init__(self, user_id, descricao, valor, vencimento):
        self.user_id = user_id
        self.descricao = descricao
        self.valor = valor
        self.vencimento = vencimento

    def avisarVencimento(self):
        tempo = datetime.now()
        if self.vencimento == tempo.strftime('%Y-%m-%d'):
            return f"{self.descricao} vence hoje!"
    
    def getValor(self): return self.valor # para fazer o saldo diario

    def __str__(self):
        return f"Conta: {self.descricao} - Valor: R${self.valor:.2f} - Vencimento: {self.vencimento}"