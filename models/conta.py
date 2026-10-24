
from datetime import date, datetime


class Conta:
    def __init__(self, descricao, valor, vencimento):
        self.descricao = descricao
        self.valor = valor
        self.vencimento = vencimento

    def avisarVencimento(self):
        hoje = date.today()

        if isinstance(self.vencimento, datetime):
            vencimento = self.vencimento.date()
        elif isinstance(self.vencimento, date):
            vencimento = self.vencimento
        else:
            valor_data = str(self.vencimento).strip()

            try:
                vencimento = datetime.strptime(valor_data[:10], "%Y-%m-%d").date()
            except ValueError:
                vencimento = datetime.strptime(valor_data).date()

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

    def getValor(self):
        return self.valor
