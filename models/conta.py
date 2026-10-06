from datetime import datetime
class Conta():
    def __init__(self, descricao, valor, vencimento):
        self.descricao = descricao
        self.valor = valor
        self.vencimento = vencimento

    def avisarVencimento(self):
        hoje = datetime.today().date()
        vencimento = datetime.strptime(
            self.vencimento,
            "%Y-%m-%d"
        ).date()
        diferenca = (vencimento - hoje).days
        if diferenca < 0:
            return f"{self.descricao} está atrasada!"
        if diferenca == 0:
            return f"{self.descricao} vence hoje!"
        if diferenca == 1:
            return f"{self.descricao} vence amanhã!"
        return None
    
    def getInformacoes(self):
        return self.descricao, self.valor, self.vencimento
    
    def getValor(self): return self.valor # para fazer o saldo diario

