from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta
from models.saldo import SaldoDiario
from models.user import User
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from leet_connect import conectar, inicializar_banco
from werkzeug.security import generate_password_hash, check_password_hash
from CRUD import *
from flask_wtf.csrf import CSRFProtect
import base64
import binascii
import io
from datetime import date, datetime
import os
import math
import secrets
from pathlib import Path
from decimal import Decimal, InvalidOperation
from functools import wraps

diretorio_atual = Path.home()/".leet_empresas"
diretorio_atual.mkdir(parents=True, exist_ok=True)
caminho_arquivo_env = diretorio_atual/"secret.key"
def obter_ou_criar_chave_secreta():
    if caminho_arquivo_env.exists():
        with open(caminho_arquivo_env, "r", encoding="utf-8") as arquivo:
            return arquivo.read().strip()
    else:
        chave_secreta = secrets.token_hex(16)
        with open(caminho_arquivo_env, "w", encoding="utf-8") as arquivo:
            arquivo.write(chave_secreta)
        return chave_secreta

app = Flask(__name__)

app.secret_key = obter_ou_criar_chave_secreta()
csrf = CSRFProtect(app)
inicializar_banco()


def validar_data(data):
    try:
        return datetime.strptime(data, "%d/%m/%Y").date()
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

def calcular_total_movimentacao(tipo, data):
    if tipo == 'venda':
        itens = selectVendas()
    elif tipo == 'compra':
        itens = selectCompras()
    total = 0
    for i in itens:
        if i[f"data_{tipo}"][:10] == date.today().strftime("%d/%m/%Y"):
            total += i["preco_total"]
    return total

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)

    return wrapper

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
@login_required
def dashboard():
    produtos = selectProdutos()
    contas = selectContas()
    vendas = selectVendas()
    compras = selectCompras()
    saldos = selectSaldos()
    notificacoes = []
    data_atual = date.today().strftime("%d/%m/%Y")
    total_vendas_hoje = calcular_total_movimentacao("venda", data_atual)
    total_compras_hoje = calcular_total_movimentacao("compra", data_atual)
    total_contas = sum(Decimal(conta["valor_conta"]) for conta in contas if conta["vencimento"][:10] == data_atual)
    saldo_diario = SaldoDiario(total_vendas_hoje, total_compras_hoje, total_contas)

    for i in produtos:
        objeto_produto = Produto(i["nome_prod"], Decimal(i["valor_custo"]), Decimal(i["valor_venda"]), i["quant_prod"])
        aviso = objeto_produto.avisarFalta()
        if aviso:
            notificacoes.append(aviso)
    for i in contas:
        objeto_conta = Conta(i["descricao_conta"], Decimal(i["valor_conta"]), i["vencimento"])
        aviso = objeto_conta.avisarVencimento()
        if aviso:
            notificacoes.append(aviso)

    print("DATA:", data_atual)
    print("VENDAS:", total_vendas_hoje)
    print("COMPRAS:", total_compras_hoje)
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
        notificacoes=notificacoes,
        saldos=saldos
    )

@app.route('/produto/<int:id_prod>/foto')
@login_required
def foto_produto(id_prod):
    foto = buscarFotoProduto(id_prod)
    if not foto or not foto["foto"] or not foto["foto_mime"]:
        flash("Foto não encontrada", "error")
        return redirect(url_for('dashboard'))
    return send_file(io.BytesIO(foto["foto"]), mimetype=foto["foto_mime"])


@app.route('/cadastrar-produto', methods=['POST'])
@login_required
def cadastrar_produto():
    try:
        nome = request.form.get('nome', '').strip()
        valor_custo = Decimal(request.form.get('valor_custo').replace(',', '.'))
        valor_venda = Decimal(request.form.get('valor_venda').replace(',', '.'))
        if not math.isfinite(valor_custo) or not math.isfinite(valor_venda):
            flash("Preencha os valores corretamente", "error")
            return redirect(url_for('dashboard'))
        quant = int(request.form.get('quantidade'))
    except (TypeError, ValueError, InvalidOperation):
        flash("Preencha os valores corretamente", "error")
        return redirect(url_for('dashboard'))
    if not nome or valor_custo < 0 or valor_venda < 0 or quant < 0:
        flash("Valores não podem ser negativos", "error")
        return redirect(url_for('dashboard'))
    foto = None
    foto_mime = None
    foto_base64 = request.form.get("foto_base64", "").strip()
    if foto_base64:
        try:
            cabecalho, dados = foto_base64.split(",", 1)
            mime = cabecalho.split(";", 1)[0].replace("data:", "").strip().lower()
            if mime not in {"image/png", "image/jpeg"}:
                raise ValueError("Formato de foto não permitido")
            foto = base64.b64decode(dados, validate=True)
            if len(foto) > 2 * 1024 * 1024:
                raise ValueError("A foto deve ter no máximo 2 MB")
            assinaturas = {
                "image/png": b"\x89PNG\r\n\x1a\n",
                "image/jpeg": b"\xff\xd8\xff",
            }
            if not foto.startswith(assinaturas[mime]):
                raise ValueError("Arquivo de imagem inválido")
            foto_mime = mime
        except (ValueError, binascii.Error):
            flash("Foto inválida. Use PNG ou JPEG de até 2 MB.", "error")
            return redirect(url_for('dashboard'))

    cadastrar_produto = Produto(nome, Decimal(valor_custo), Decimal(valor_venda), int(quant))
    insertProduto(*cadastrar_produto.getInformacoes(), foto=foto, foto_mime=foto_mime)
    flash("Produto cadastrado com sucesso", "success")
    return redirect(url_for('dashboard'))

@app.route('/editar-preco', methods=['POST'])
@login_required
def editar_preco():
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    codigo = dados.get('codigo')
    tipo_preco = dados.get('tipo_preco')
    try:
        novo_preco = Decimal(dados.get("novo_preco"))
    except (TypeError, ValueError, InvalidOperation):
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

    return {"sucesso": "preço atualizado com sucesso"}, 200

@app.route('/remover-item', methods=['POST'])
@login_required
def remover_item():
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    codigo = dados.get('codigo')
    tipo_item = dados.get('tipo')
    deleteItem(codigo, tipo_item)
    return {"sucesso": "Item removido com sucesso"}, 200

@app.route('/registrar-venda', methods=['POST'])
@login_required
def registrar_venda():
    try:
        itens = ler_itens(request.form)
    except ValueError as e:
        return str(e), 400
    cadastrar_venda = []
    for codigo, quantidade in itens.items():
        produto = buscarProduto(codigo)
        if not produto:
            flash(f"Produto com código {codigo} não encontrado", "error")
            return redirect(url_for('dashboard'))
        if quantidade > produto["quant_prod"]:
            flash(f"Quantidade insuficiente em estoque para o produto {produto['nome_prod']}", "error")
            return redirect(url_for('dashboard'))

        cadastrar_venda.append((produto["id_prod"], produto["valor_venda"], int(quantidade)))
    insertVenda(Venda(cadastrar_venda))
    flash("Venda registrada com sucesso", "success")
    return redirect(url_for('dashboard'))


@app.route('/registrar-compra', methods=['POST'])
@login_required
def registrar_compra():
    try:
        itens = ler_itens(request.form)
    except ValueError as e:
        return str(e), 400
    cadastrar_compra = []
    for codigo, quantidade in itens.items():
        produto = buscarProduto(codigo)
        if not produto:
            flash(f"Produto com código {codigo} não encontrado", "error")
            return redirect(url_for('dashboard'))
        cadastrar_compra.append((produto["id_prod"], produto["valor_custo"], int(quantidade)))
    insertCompra(Compra(cadastrar_compra))
    flash("Compra registrada com sucesso", "success")
    return redirect(url_for('dashboard'))

@app.route('/registrar-conta', methods=['POST'])
@login_required
def registrar_conta():
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    try:
        vencimento = validar_data(vencimento)
    except ValueError as e:
        return str(e), 400
    try:
        valor = Decimal(valor.replace(',', '.'))
    except (TypeError, ValueError, InvalidOperation):
        flash("Valor inválido", "error")
        return redirect(url_for('dashboard'))
    if not descricao or valor is None or vencimento is None:
        flash("Preencha todos os campos", "error")
        return redirect(url_for('dashboard'))
    if valor < 0:
        flash("Valor não pode ser negativo", "error")
        return redirect(url_for('dashboard'))
    cadastrar_conta = Conta(descricao, Decimal(valor), vencimento)
    insertConta(*cadastrar_conta.getInformacoes())
    flash("Conta registrada com sucesso", "success")
    return redirect(url_for('dashboard'))

@app.route('/registrar-saldo', methods=['POST'])
@login_required
def registrar_saldo():
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    try:
        saldo = Decimal(dados.get('saldo'))
    except (TypeError, ValueError, InvalidOperation):
        return {"erro": "saldo inválido"}, 400
    insertSaldoDiario(saldo,date.today().strftime("%Y-%m-%d"))
    return {"sucesso": "Saldo registrado com sucesso"}, 200

# ROTA DE LOGOUT
@app.route('/logout')
def logout():
    session.clear()  # Limpa os dados da sessão
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)