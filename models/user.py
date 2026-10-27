# representa um usuário do sistema e protege a senha antes de ela ser guardada
# importa as funções que criam e verificam o hash da senha
from werkzeug.security import generate_password_hash, check_password_hash
# guarda o nome de login, o nome da empresa e a senha já criptografada
class User():
    def __init__(self, user_id, nome_empresa, senha):
        self.user_id = user_id
        self.nome_empresa = nome_empresa
        # guarda apenas o hash da senha, nunca o texto original
        self.senha = self.setarSenha(senha)
    # transforma a senha em um hash seguro
    def setarSenha(self, senha):
        return generate_password_hash(senha)

    # confere se a senha informada corresponde ao hash guardado
    def checkSenha(self, senha):
        return check_password_hash(self.senha, senha)
    
    # devolve os dados do usuário na ordem usada para gravar no banco
    def getInformacoes(self):
        return self.user_id, self.nome_empresa, self.senha