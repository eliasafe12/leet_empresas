from werkzeug.security import generate_password_hash, check_password_hash
class User():
    def __init__(self, user_id, nome_empresa, senha):
        self.user_id = user_id
        self.nome_empresa = nome_empresa
        self.senha = self.setarSenha(senha)
    def setarSenha(self, senha):
        return generate_password_hash(senha)

    def checkSenha(self, senha):
        return check_password_hash(self.senha, senha)
    
    def getInformacoes(self):
        return self.user_id, self.nome_empresa, self.senha