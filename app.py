from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta
from models.saldo import SaldoDiario
from models.user import User
from flask import Flask, render_template, request, redirect, url_for, session, flash
from leet_connect import conectar, inicializar_banco
from CRUD import *
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import os
from dotenv import load_dotenv
import math

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
inicializar_banco()


def validar_data(data):
    try:
        return datetime.strptime(data, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValueError("Data inválida")
    
def ler_itens(form):
    codigos = form.getlist("codigo[]")
    quantidades = form.getlist("quantidade[]")
    if not codigos or len(codigos) != len(quantidades):
        raise ValueError("Adicione pelo menos um produto")

    itens = {}
    for codigo, qtd in zip(codigos, quantidades):
        try:
            codigo = int(codigo)
            qtd = int(qtd)
        except ValueError:
            raise ValueError("Código e quantidade devem ser números inteiros")
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        itens[codigo] = itens.get(codigo, 0) + qtd   # soma repetidos
    return itens

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
            flash("Preencha usuário e senha", "error")
            return redirect(url_for("login"))
        usuario = selectUsuario(user_id)
        if not usuario:
            flash("Usuário ou senha incorretos", "error")
            return redirect(url_for("login"))
        if not check_password_hash(usuario["senha"], senha):
            flash("Usuário ou senha incorretos", "error")
            return redirect(url_for("login"))
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
            flash("Preencha todos os campos", "error")
            return redirect(url_for('cadastro'))
        try:
            cadastrar_usuario = User(user_id, nome_empresa, senha)
            insertUsuario(*cadastrar_usuario.getInformacoes())
        except ValueError as e:
            flash(str(e), "error")
            return render_template('cadastro.html')
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    produtos = selectProdutos()
    contas = selectContas()
    vendas = selectVendas()
    compras = selectCompras()
    notificacoes = []
    total_vendas_hoje = 0
    for i in vendas:
        if i["data_venda"][:10] == date.today().strftime("%d/%m/%Y"):
            total_vendas_hoje += i["preco_total"]
    total_compras_hoje = 0
    for i in compras:
        if i["data_compra"][:10] == date.today().strftime("%d/%m/%Y"):
            total_compras_hoje += i["preco_total"]
    total_contas = 0
    for i in contas:
        total_contas += i["valor_conta"]
    saldo_diario = SaldoDiario(total_vendas_hoje, total_compras_hoje, total_contas)

    for i in produtos:
        objeto_produto = Produto(i["nome_prod"], i["valor_custo"], i["valor_venda"], i["quant_prod"])
        aviso = objeto_produto.avisarFalta()
        if aviso:
            notificacoes.append(aviso)
    for i in contas:
        objeto_conta = Conta(i["descricao_conta"], i["valor_conta"], i["vencimento"])
        
        aviso = objeto_conta.avisarVencimento()
        if aviso:
            notificacoes.append(aviso)
    return render_template(
        "paginaPrincipal.html",
        nome_empresa=session.get("empresa"),
        nome_usuario=session.get("usuario"),
        total_produtos=len(produtos),
        saldo_dia=saldo_diario.saldo,
        total_vendas_hoje=total_vendas_hoje,
        total_compras_hoje=total_compras_hoje,
        produtos=produtos,
        contas=contas,
        vendas=vendas,
        compras=compras,
        notificacoes=notificacoes
    )

@app.route('/cadastrar-produto', methods=['POST'])
def cadastrar_produto():
    if "usuario" not in session:
        return redirect(url_for("login"))
    try:
        nome = request.form.get('nome', '').strip()
        valor_custo = float(request.form.get('valor_custo').replace(',', '.'))
        valor_venda = float(request.form.get('valor_venda').replace(',', '.'))
        if not math.isfinite(valor_custo) or not math.isfinite(valor_venda):
            return "Preencha os valores corretamente", 400
        
        quant = int(request.form.get('quantidade'))
    except (TypeError, ValueError):
        flash("Preencha os valores corretamente", "error")
        return redirect(url_for('dashboard'))
    if not nome or valor_custo < 0 or valor_venda < 0 or quant < 0:
        flash("Valores não podem ser negativos", "error")
        return redirect(url_for('dashboard'))
    cadastrar_produto = Produto(nome, float(valor_custo), float(valor_venda), int(quant))
    insertProduto(*cadastrar_produto.getInformacoes())
    flash("Produto cadastrado com sucesso", "success")
    return redirect(url_for('dashboard'))

@app.route('/editar-preco', methods=['POST'])
def editar_preco():
    if "usuario" not in session:
        return redirect(url_for("login"))
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    codigo = dados.get('codigo')
    tipo_preco = dados.get('tipo_preco')
    try:
        novo_preco = float(dados.get("novo_preco"))
    except (TypeError, ValueError):
        return {"erro": "preço inválido"}, 400
    if novo_preco < 0:
        return {"erro": "preço inválido"}, 400
    if not buscarProduto(codigo):
        return {"erro": "produto não encontrado"}, 404
    if tipo_preco == "custo":
        updatePrecoCusto(codigo, novo_preco)
    elif tipo_preco == "venda":
        updatePrecoVenda(codigo, novo_preco)
    else:
        return {"erro": "tipo deve ser 'custo' ou 'venda'"}, 400

    return redirect(url_for('dashboard'))

@app.route('/remover-item', methods=['POST'])
def remover_item():
    if "usuario" not in session:
        return redirect(url_for("login"))
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    codigo = dados.get('codigo')
    tipo_item = dados.get('tipo')
    deleteItem(codigo, tipo_item)
    flash("Item removido com sucesso", "success")
    return redirect(url_for('dashboard'))

@app.route('/registrar-venda', methods=['POST'])
def registrar_venda():
    if "usuario" not in session:
        return redirect(url_for("login"))
    try:
        itens = ler_itens(request.form)
    except ValueError as e:
        return str(e), 400
    cadastrar_venda = []
    for codigo, quantidade in itens.items():
        produto = buscarProduto(codigo)
        if not produto:
            flash("Produto não encontrado", "error")
            return redirect(url_for('dashboard'))
        if not math.isfinite(float(quantidade)):
            flash("Quantidade inválida", "error")
            return redirect(url_for('dashboard'))
            
        cadastrar_venda.append((produto["id_prod"], produto["valor_venda"], int(quantidade)))
    insertVenda(Venda(cadastrar_venda))
    return redirect(url_for('dashboard'))

@app.route('/registrar-compra', methods=['POST'])
def registrar_compra():
    if "usuario" not in session:
        return redirect(url_for("login"))
    try:
        itens = ler_itens(request.form)
    except ValueError as e:
        return str(e), 400
    cadastrar_compra = []
    for codigo, quantidade in itens.items():
        produto = buscarProduto(codigo)
        if not produto:
            return "Produto não encontrado", 404
        if not math.isfinite(float(quantidade)):
            return "Quantidade inválida", 400
        cadastrar_compra.append((produto["id_prod"], produto["valor_custo"], int(quantidade)))
    insertCompra(Compra(cadastrar_compra))
    return redirect(url_for('dashboard'))

@app.route('/registrar-conta', methods=['POST'])
def registrar_conta():
    if "usuario" not in session:
        return redirect(url_for("login"))
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    try:
        vencimento = validar_data(vencimento)
    except ValueError as e:
        return str(e), 400
    if not math.isfinite(float(valor)):
        return "Valor inválido", 400
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
    