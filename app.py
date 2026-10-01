from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta
from models.saldo import SaldoDiario
from models.user import User
from flask import Flask, render_template, request, redirect, url_for

# arrays para teste
produtos = []
vendas = []
compras = []
contas = []
usuarios = []

app = Flask(__name__)

@app.route("/")
def home():
    # Redireciona a rota inicial para a tela de login
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = get_user(request.form['usuario'])

    if user != None:
        if user.check_password(request.form['senha']):
            login_user(user)
            app.logger.info('%s logado com sucesso!', user.username)
            return redirect(url_for('index'))
        else:
            app.logger.info('Usuário ou senha incorretos!')
            abort(401)
        return render_template('login.html')
    else: return 'Usuário ou senha incorretos!'

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        nome_empresa = request.form.get('nome_empresa')
        senha = request.form.get('senha')
        usuarios.append(User(user_id, nome_empresa, senha)) # temporario
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')


if __name__ == '__main__':
    app.run(debug=True)
    