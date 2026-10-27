# representa uma conta a pagar e avisa quando o vencimento está próximo
# importa recursos para trabalhar com datas
from datetime import date, datetime


# guarda a descrição, o valor e a data de vencimento de uma conta
class Conta:
    def __init__(self, descricao, valor, vencimento):
        self.descricao = descricao
        self.valor = valor
        self.vencimento = vencimento

    # devolve uma mensagem quando a conta está atrasada, vence hoje ou vence amanhã
    def avisarVencimento(self):
        # obtém a data atual para comparar com o vencimento
        hoje = date.today()

        # converte o vencimento para um objeto date, qualquer que seja o formato em que ele foi recebido
        if isinstance(self.vencimento, datetime):
            vencimento = self.vencimento.date()
        elif isinstance(self.vencimento, date):
            vencimento = self.vencimento
        else:
            # trata o vencimento recebido como texto, por exemplo o que vem do banco de dados
            valor_data = str(self.vencimento).strip()

            # tenta primeiro o formato ano-mês-dia
            try:
                vencimento = datetime.strptime(valor_data[:10], "%Y-%m-%d").date()
            # usa o formato dia/mês/ano quando o primeiro não corresponde
            except ValueError:
                vencimento = datetime.strptime(valor_data[:10], "%d/%m/%Y").date()

        # calcula quantos dias faltam para o vencimento, com valor negativo quando já passou
        diferenca = (vencimento - hoje).days

        # avisa que a conta está atrasada
        if diferenca < 0:
            return f"{self.descricao} está atrasada!"

        # avisa que a conta vence hoje
        if diferenca == 0:
            return f"{self.descricao} vence hoje!"

        # avisa que a conta vence amanhã
        if diferenca == 1:
            return f"{self.descricao} vence amanhã!"

        # não gera aviso quando ainda faltam mais de um dia
        return None

    # devolve a descrição, o valor e o vencimento para serem gravados no banco
    def getInformacoes(self):
        return self.descricao, self.valor, self.vencimento

    # devolve apenas o valor da conta
    def getValor(self):
        return self.valor