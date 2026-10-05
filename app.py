from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta
from models.saldo import SaldoDiario
from models.user import User
from flask import Flask, render_template, request, redirect, url_for, session, abort
from leet_connect import conectar, inicializar_banco
from CRUD import *
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "troque-essa-chave" # temporário
inicializar_banco()

usuarios = []
@app.route("/")
def home():
    # Redireciona a rota inicial para a tela de login
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_id = request.form.get("usuario")
        senha = request.form.get("senha")
        if not user_id or not senha:
            return "Preencha usuário e senha", 400
        usuario = selectUsuario(user_id)
        if not usuario:
            return "Usuário ou senha incorretos", 404
        if not check_password_hash(usuario["senha"], senha):
            return "Usuário ou senha incorretos", 401
        session["usuario"] = usuario["user_id"]
        session["empresa"] = usuario["nome_empresa"]
        return redirect(url_for("dashboard"))
        
    return render_template("login.html")

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        nome_empresa = request.form.get('nome_empresa')
        senha = request.form.get('senha')
        if not user_id or not nome_empresa or not senha:
            return "Preencha todos os campos", 400
        usuario = selectUsuario(user_id)
        if usuario:
            return "Usuário já existe", 400
        cadastrar_usuario = User(user_id, nome_empresa, senha)
        insertUsuario(*cadastrar_usuario.getInformacoes())
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    produtos = selectProdutos()
    contas = selectContas()
    return render_template(
        "paginaPrincipal.html",
        nome_empresa=session.get("empresa"),
        nome_usuario=session.get("usuario"),
        total_produtos=0,
        saldo_dia=0,
        total_vendas_hoje=0,
        total_compras_hoje=0,
        produtos=produtos,
        contas=contas,
        notificacoes=[]
    )

@app.route('/cadastrar-produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form.get('nome')
    valor_custo = request.form.get('valor_custo')
    valor_venda = request.form.get('valor_venda')
    quant = request.form.get('quantidade')
    cadastrar_produto = Produto(nome, float(valor_custo), float(valor_venda), int(quant))
    insertProduto(cadastrar_produto.getInformacoes())
    return redirect(url_for('dashboard'))

@app.route('/registrar-venda', methods=['POST'])
def registrar_venda(): # ainda não está funcionando kkk
    codigo = request.form.get('codigo')
    quantidade = request.form.get('quantidade')
    produto = buscarProduto(codigo)
    if not produto:
        return "Produto não encontrado", 404
    if int(quantidade) > produto["quant_prod"]:
        return "Quantidade insuficiente em estoque", 400
    cadastrar_venda = Venda(produto["id_prod"], produto["valor_venda"], int(quantidade))
    insertVenda(*cadastrar_venda.getInformacoes())
    return redirect(url_for('dashboard'))

@app.route('/registrar-compra', methods=['POST'])
def registrar_compra():
    # Adicione aqui a lógica para registrar compras
    return redirect(url_for('dashboard'))

@app.route('/registrar-conta', methods=['POST'])
def registrar_conta():
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    cadastrar_conta = Conta(descricao, float(valor), vencimento)
    insertConta(*cadastrar_conta.getInformacoes())
    return redirect(url_for('dashboard'))

# ROTA DE LOGOUT
@app.route('/logout')
def logout():
    session.clear()  # Limpa os dados da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
    