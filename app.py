
# importa as classes responsáveis por representar as entidades do sistema
from models.venda import Venda
from models.compra import Compra
from models.produto import Produto
from models.conta import Conta
from models.saldo import SaldoDiario
from models.user import User

# importa os recursos do flask para criar rotas, renderizar páginas, processar requisições e gerenciar sessões
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file

# importa as funções de conexão e inicialização do banco de dados
from leet_connect import conectar, inicializar_banco

# importa as funções para gerar e verificar hashes de senhas
from werkzeug.security import generate_password_hash, check_password_hash

# importa as operações de criação, consulta, atualização e remoção de registros
from CRUD import *

# importa a proteção contra ataques csrf nas requisições
from flask_wtf.csrf import CSRFProtect

# importa recursos para codificação de imagens, tratamento de arquivos e conversão de dados
import base64
import binascii
import io

# importa recursos para trabalhar com datas e horários
from datetime import date, datetime

# importa recursos para manipulação de arquivos e cálculos matemáticos
import os
import math
import secrets

# importa recursos para localizar e manipular caminhos do sistema de arquivos
from pathlib import Path

# importa recursos para trabalhar com valores decimais e tratar erros de conversão
from decimal import Decimal, InvalidOperation

# importa o decorador wraps para preservar os metadados das funções decoradas
from functools import wraps

# define o diretório pessoal usado para armazenar arquivos de configuração do aplicativo
diretorio_atual = Path.home()/".leet_empresas"

# cria o diretório caso ele ainda não exista
diretorio_atual.mkdir(parents=True, exist_ok=True)

# define o caminho do arquivo que armazena a chave secreta do aplicativo
caminho_arquivo_env = diretorio_atual/"secret.key"

# recupera a chave secreta existente ou cria uma nova caso o arquivo não exista
def obter_ou_criar_chave_secreta():
    # verifica se o arquivo da chave secreta já foi criado
    if caminho_arquivo_env.exists():
        # abre o arquivo em modo de leitura e remove espaços e quebras de linha das extremidades
        with open(caminho_arquivo_env, "r", encoding="utf-8") as arquivo:
            return arquivo.read().strip()
    else:
        # gera uma chave aleatória para proteger a sessão do usuário
        chave_secreta = secrets.token_hex(16)
        # salva a chave gerada no arquivo para reutilizá-la nas próximas inicializações
        with open(caminho_arquivo_env, "w", encoding="utf-8") as arquivo:
            arquivo.write(chave_secreta)
        return chave_secreta

# cria a aplicação flask
app = Flask(__name__)

# permite campos de formulário de até 4 MB (foto em base64)
app.config["MAX_FORM_MEMORY_SIZE"] = 4 * 1024 * 1024

# limite total da requisição
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

# configura a chave secreta usada para assinar os dados da sessão
app.secret_key = obter_ou_criar_chave_secreta()

# ativa a proteção csrf para validar os tokens das requisições protegidas
csrf = CSRFProtect(app)

# inicializa o banco de dados e prepara sua estrutura
inicializar_banco()


# converte uma data no formato dia/mês/ano para um objeto date
def validar_data(data):
    try:
        return datetime.strptime(data, "%d/%m/%Y").date()
    # trata valores ausentes ou datas que não correspondem ao formato esperado
    except (TypeError, ValueError):
        raise ValueError("Data inválida")
    
# lê os códigos e as quantidades dos produtos enviados por um formulário
def ler_itens(form):
    codigos = form.getlist("codigo[]")
    quantidades = form.getlist("quantidade[]")
    # verifica se há produtos e se cada código possui uma quantidade correspondente
    if not codigos or len(codigos) != len(quantidades):
        raise ValueError("Adicione pelo menos um produto")

    # organiza os itens em um dicionário, somando as quantidades de códigos repetidos
    itens = {}
    for codigo, qtd in zip(codigos, quantidades):
        try:
            # converte o código e a quantidade para números inteiros
            codigo = int(codigo)
            qtd = int(qtd)
        # informa quando algum dos campos não contém um número inteiro válido
        except ValueError:
            raise ValueError("Código e quantidade devem ser números inteiros")
        # impede o registro de quantidades iguais ou inferiores a zero
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        itens[codigo] = itens.get(codigo, 0) + qtd   # soma repetidos
    return itens

# calcula o total das movimentações de vendas ou compras para uma data
def calcular_total_movimentacao(tipo, data):
    # seleciona os registros de acordo com o tipo de movimentação informado
    if tipo == 'venda':
        itens = selectVendas()
    elif tipo == 'compra':
        itens = selectCompras()
    # acumula os valores das movimentações encontradas
    total = 0
    for i in itens:
        # compara a data do registro com a data atual e soma os valores correspondentes
        if i[f"data_{tipo}"][:10] == date.today().strftime("%d/%m/%Y"):
            total += i["preco_total"]
    return total

# cria um decorador para impedir o acesso a rotas por usuários não autenticados
def login_required(func):
    # preserva os metadados da função original
    @wraps(func)
    def wrapper(*args, **kwargs):
        # redireciona para o login quando não existe usuário na sessão
        if "usuario" not in session:
            return redirect(url_for("login"))
        # executa a rota original quando o usuário está autenticado
        return func(*args, **kwargs)

    return wrapper

# define a rota inicial do aplicativo
@app.route("/")
def home():
    # redireciona a rota inicial para a tela de login
    return redirect(url_for('login'))


# define a rota de autenticação, que aceita requisições get e post
@app.route('/login', methods=['GET', 'POST'])
def login():
    # processa os dados quando o formulário de login é enviado
    if request.method == "POST":
        user_id = request.form.get("usuario")
        senha = request.form.get("senha")
        # verifica se os campos de usuário e senha foram preenchidos
        if not user_id or not senha:
            flash("Preencha usuário e senha", "error")
            return redirect(url_for("login"))
        # consulta o usuário no banco de dados
        usuario = selectUsuario(user_id)
        # rejeita a autenticação caso o usuário não seja encontrado
        if not usuario:
            flash("Usuário ou senha incorretos", "error")
            return redirect(url_for("login"))
        # compara a senha informada com o hash armazenado
        if not check_password_hash(usuario["senha"], senha):
            flash("Usuário ou senha incorretos", "error")
            return redirect(url_for("login"))
        # armazena na sessão os dados usados para identificar o usuário e a empresa
        session["usuario"] = usuario["user_id"]
        session["empresa"] = usuario["nome_empresa"]
        return redirect(url_for("dashboard"))
        
    # exibe o formulário de login quando a requisição não é post
    return render_template("login.html")

# define a rota de cadastro de novos usuários
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    # processa os dados enviados pelo formulário de cadastro
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        nome_empresa = request.form.get('nome_empresa')
        senha = request.form.get('senha')
        # exige o preenchimento de todos os campos
        if not user_id or not nome_empresa or not senha:
            flash("Preencha todos os campos", "error")
            return redirect(url_for('cadastro'))
        try:
            # cria o objeto de usuário com os dados recebidos
            cadastrar_usuario = User(user_id, nome_empresa, senha)
            # insere as informações do usuário no banco de dados
            insertUsuario(*cadastrar_usuario.getInformacoes())
        # trata erros de validação lançados pela classe ou pelo processo de cadastro
        except ValueError as e:
            flash(str(e), "error")
            return render_template('cadastro.html')
        # direciona o usuário para o login após o cadastro
        return redirect(url_for('login'))
        
    # exibe o formulário de cadastro em requisições get
    return render_template('cadastro.html')

# define o painel principal do sistema, acessível somente após o login
@app.route("/dashboard")
@login_required
def dashboard():
    # consulta os dados necessários para preencher o painel
    produtos = selectProdutos()
    contas = selectContas()
    vendas = selectVendas()
    compras = selectCompras()
    saldos = selectSaldos()

    # prepara uma lista para armazenar os avisos apresentados no painel
    notificacoes = []

    # obtém a data atual no formato dia/mês/ano
    data_atual = date.today().strftime("%d/%m/%Y")

    # calcula os totais de vendas e compras do dia
    total_vendas_hoje = calcular_total_movimentacao("venda", data_atual)
    total_compras_hoje = calcular_total_movimentacao("compra", data_atual)

    # soma os valores das contas cujo vencimento corresponde à data atual
    total_contas = sum(Decimal(conta["valor_conta"]) for conta in contas if conta["vencimento"][:10] == data_atual)

    # cria o objeto responsável por calcular o saldo diário
    saldo_diario = SaldoDiario(total_vendas_hoje, total_compras_hoje, total_contas)

    # percorre os produtos para identificar possíveis avisos de estoque
    for i in produtos:
        # converte os dados do banco em um objeto produto
        objeto_produto = Produto(i["nome_prod"], Decimal(i["valor_custo"]), Decimal(i["valor_venda"]), i["quant_prod"])
        # verifica se o produto precisa gerar um aviso de falta
        aviso = objeto_produto.avisarFalta()
        # adiciona à lista os avisos retornados pela classe
        if aviso:
            notificacoes.append(aviso)

    # percorre as contas para verificar avisos relacionados ao vencimento
    for i in contas:
        # cria um objeto conta com a descrição, o valor e a data de vencimento
        objeto_conta = Conta(i["descricao_conta"], Decimal(i["valor_conta"]), i["vencimento"])
        # consulta se a conta deve gerar um aviso de vencimento
        aviso = objeto_conta.avisarVencimento()
        # adiciona à lista os avisos retornados pela classe
        if aviso:
            notificacoes.append(aviso)

    # renderiza o painel e envia os dados consultados para o template html
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

# disponibiliza a foto de um produto cadastrado
@app.route('/produto/<int:id_prod>/foto')
@login_required
def foto_produto(id_prod):
    # consulta no banco os dados da foto associada ao produto
    foto = buscarFotoProduto(id_prod)
    # verifica se existem dados de imagem e seu tipo mime
    if not foto or not foto["foto"] or not foto["foto_mime"]:
        flash("Foto não encontrada", "error")
        return redirect(url_for('dashboard'))
    # envia os bytes da imagem ao navegador com o tipo mime correspondente
    return send_file(io.BytesIO(foto["foto"]), mimetype=foto["foto_mime"])


# registra um novo produto no sistema
@app.route('/cadastrar-produto', methods=['POST'])
@login_required
def cadastrar_produto():
    try:
        # obtém o nome do produto e remove espaços das extremidades
        nome = request.form.get('nome', '').strip()
        # converte os preços para decimal, aceitando vírgula como separador decimal
        valor_custo = Decimal(request.form.get('valor_custo').replace(',', '.'))
        valor_venda = Decimal(request.form.get('valor_venda').replace(',', '.'))
        # impede valores numéricos que não sejam finitos
        if not math.isfinite(valor_custo) or not math.isfinite(valor_venda):
            flash("Preencha os valores corretamente", "error")
            return redirect(url_for('dashboard'))
        # converte a quantidade informada para inteiro
        quant = int(request.form.get('quantidade'))
    # trata erros de campos ausentes ou valores em formatos inválidos
    except (TypeError, ValueError, InvalidOperation):
        flash("Preencha os valores corretamente", "error")
        return redirect(url_for('dashboard'))

    # valida o nome, os preços e a quantidade antes de cadastrar o produto
    if not nome or valor_custo < 0 or valor_venda < 0 or quant < 0:
        flash("Valores não podem ser negativos", "error")
        return redirect(url_for('dashboard'))

    # inicializa os dados opcionais da foto
    foto = None
    foto_mime = None

    # recupera a imagem codificada em base64 enviada pelo formulário
    foto_base64 = request.form.get("foto_base64", "").strip()
    if foto_base64:
        try:
            # separa o cabeçalho com o tipo de imagem do conteúdo codificado
            cabecalho, dados = foto_base64.split(",", 1)
            # identifica o tipo mime declarado pela imagem
            mime = cabecalho.split(";", 1)[0].replace("data:", "").strip().lower()
            # permite somente imagens png e jpeg
            if mime not in {"image/png", "image/jpeg"}:
                raise ValueError("Formato de foto não permitido")
            # decodifica o conteúdo base64 e valida sua codificação
            foto = base64.b64decode(dados, validate=True)
            # limita o tamanho da imagem a dois megabytes
            if len(foto) > 2 * 1024 * 1024:
                raise ValueError("A foto deve ter no máximo 2 MB")
            # define as assinaturas binárias esperadas para cada formato de imagem
            assinaturas = {
                "image/png": b"\x89PNG\r\n\x1a\n",
                "image/jpeg": b"\xff\xd8\xff",
            }
            # verifica se o conteúdo começa com a assinatura do formato declarado
            if not foto.startswith(assinaturas[mime]):
                raise ValueError("Arquivo de imagem inválido")
            # guarda o tipo mime validado para armazenamento posterior
            foto_mime = mime
        # trata erros na estrutura, no conteúdo ou na codificação da imagem
        except (ValueError, binascii.Error):
            flash("Foto inválida. Use PNG ou JPEG de até 2 MB.", "error")
            return redirect(url_for('dashboard'))

    # cria o objeto produto com os dados validados
    cadastrar_produto = Produto(nome, Decimal(valor_custo), Decimal(valor_venda), int(quant))
    # grava os dados do produto e, quando fornecida, sua foto no banco
    insertProduto(*cadastrar_produto.getInformacoes(), foto=foto, foto_mime=foto_mime)
    flash("Produto cadastrado com sucesso", "success")
    return redirect(url_for('dashboard'))

# atualiza o preço de custo ou de venda de um produto por meio de uma requisição json
@app.route('/editar-preco', methods=['POST'])
@login_required
def editar_preco():
    # tenta interpretar o corpo da requisição como json
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    # recupera o código, o tipo de preço e o novo valor enviados pelo cliente
    codigo = dados.get('codigo')
    tipo_preco = dados.get('tipo_preco')
    try:
        # converte o novo preço para decimal
        novo_preco = Decimal(dados.get("novo_preco"))
    # retorna erro quando o valor não pode ser convertido
    except (TypeError, ValueError, InvalidOperation):
        return {"erro": "preço inválido"}, 400
    # rejeita preços negativos
    if novo_preco < 0:
        return {"erro": "preço inválido"}, 400
    # verifica se o produto informado existe
    if not buscarProduto(codigo):
        return {"erro": "produto não encontrado"}, 404
    # atualiza o preço de custo quando esse tipo foi solicitado
    if tipo_preco == "custo":
        updatePrecoCusto(codigo, novo_preco)
    # atualiza o preço de venda quando esse tipo foi solicitado
    elif tipo_preco == "venda":
        updatePrecoVenda(codigo, novo_preco)
    # rejeita tipos de preço diferentes dos permitidos
    else:
        return {"erro": "tipo deve ser 'custo' ou 'venda'"}, 400

    # retorna uma confirmação em json após a atualização
    return {"sucesso": "preço atualizado com sucesso"}, 200

# remove um item conforme o código e o tipo recebidos em json
@app.route('/remover-item', methods=['POST'])
@login_required
def remover_item():
    # interpreta o corpo da requisição como json
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    # recupera o código do item e o tipo de registro a remover
    codigo = dados.get('codigo')
    tipo_item = dados.get('tipo')
    # executa a remoção por meio da função do módulo crud
    deleteItem(codigo, tipo_item)
    return {"sucesso": "Item removido com sucesso"}, 200

# registra uma venda com um ou mais produtos
@app.route('/registrar-venda', methods=['POST'])
@login_required
def registrar_venda():
    # lê e valida os códigos e as quantidades enviados pelo formulário
    try:
        itens = ler_itens(request.form)
    except ValueError as e:
        return str(e), 400

    # prepara a lista de itens que será enviada para a classe venda
    cadastrar_venda = []
    for codigo, quantidade in itens.items():
        # consulta os dados do produto pelo código informado
        produto = buscarProduto(codigo)
        # interrompe o registro se algum produto não existir
        if not produto:
            flash(f"Produto com código {codigo} não encontrado", "error")
            return redirect(url_for('dashboard'))
        # verifica se há estoque suficiente para a venda solicitada
        if quantidade > produto["quant_prod"]:
            flash(f"Quantidade insuficiente em estoque para o produto {produto['nome_prod']}", "error")
            return redirect(url_for('dashboard'))

        # adiciona à lista o identificador, o preço de venda e a quantidade
        cadastrar_venda.append((produto["id_prod"], produto["valor_venda"], int(quantidade)))
    # cria a venda e solicita sua gravação no banco de dados
    insertVenda(Venda(cadastrar_venda))
    flash("Venda registrada com sucesso", "success")
    return redirect(url_for('dashboard'))


# registra uma compra com um ou mais produtos
@app.route('/registrar-compra', methods=['POST'])
@login_required
def registrar_compra():
    # lê e valida os códigos e as quantidades enviados pelo formulário
    try:
        itens = ler_itens(request.form)
    except ValueError as e:
        return str(e), 400

    # prepara a lista de itens que será enviada para a classe compra
    cadastrar_compra = []
    for codigo, quantidade in itens.items():
        # consulta os dados do produto pelo código informado
        produto = buscarProduto(codigo)
        # interrompe o registro se algum produto não existir
        if not produto:
            flash(f"Produto com código {codigo} não encontrado", "error")
            return redirect(url_for('dashboard'))
        # adiciona à lista o identificador, o preço de custo e a quantidade
        cadastrar_compra.append((produto["id_prod"], produto["valor_custo"], int(quantidade)))
    # cria a compra e solicita sua gravação no banco de dados
    insertCompra(Compra(cadastrar_compra))
    flash("Compra registrada com sucesso", "success")
    return redirect(url_for('dashboard'))

# registra uma conta com descrição, valor e data de vencimento
@app.route('/registrar-conta', methods=['POST'])
@login_required
def registrar_conta():
    # recupera os dados enviados pelo formulário
    descricao = request.form.get('descricao')
    valor = request.form.get('valor')
    vencimento = request.form.get('vencimento')
    try:
        # valida e converte a data para um objeto date
        vencimento = validar_data(vencimento)
    # informa quando a data não estiver no formato esperado
    except ValueError as e:
        return str(e), 400
    try:
        # converte o valor da conta para decimal, aceitando vírgula
        valor = Decimal(valor.replace(',', '.'))
    # trata valores ausentes ou inválidos
    except (TypeError, ValueError, InvalidOperation):
        flash("Valor inválido", "error")
        return redirect(url_for('dashboard'))
    # verifica se os campos obrigatórios foram preenchidos
    if not descricao or valor is None or vencimento is None:
        flash("Preencha todos os campos", "error")
        return redirect(url_for('dashboard'))
    # impede valores negativos para a conta
    if valor < 0:
        flash("Valor não pode ser negativo", "error")
        return redirect(url_for('dashboard'))
    # cria o objeto conta com os dados validados
    cadastrar_conta = Conta(descricao, Decimal(valor), vencimento)
    # grava as informações da conta no banco de dados
    insertConta(*cadastrar_conta.getInformacoes())
    flash("Conta registrada com sucesso", "success")
    return redirect(url_for('dashboard'))

# registra o saldo diário enviado pelo cliente em formato json
@app.route('/registrar-saldo', methods=['POST'])
@login_required
def registrar_saldo():
    # interpreta o corpo da requisição como json
    dados = request.get_json(silent=True)
    if not dados:
        return {"erro": "JSON inválido"}, 400
    try:
        # converte o saldo recebido para decimal
        saldo = Decimal(dados.get('saldo'))
    # retorna erro quando o saldo não pode ser convertido
    except (TypeError, ValueError, InvalidOperation):
        return {"erro": "saldo inválido"}, 400
    # registra o saldo associado à data atual
    insertSaldoDiario(saldo,date.today().strftime("%Y-%m-%d"))
    return {"sucesso": "Saldo registrado com sucesso"}, 200

# rota de logout
@app.route('/logout')
def logout():
    session.clear()  # limpa os dados da sessão
    return redirect(url_for('login'))
