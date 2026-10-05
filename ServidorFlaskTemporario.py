#Ia

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# Necessário para utilizar o 'session' com segurança no Flask
app.secret_key = 'chave_secreta_leet_empresas'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Exemplo: Guarda o utilizador na sessão se necessário
        session['usuario'] = "Elias"
        session['empresa'] = "Minha Empresa"
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    nome_empresa = session.get('empresa', 'Minha Empresa')
    nome_usuario = session.get('usuario', 'Elias')
    
    return render_template(
        'paginaPrincipal.html',
        nome_empresa=nome_empresa,
        nome_usuario=nome_usuario,
        total_produtos=0,
        saldo_dia=0.0,
        total_vendas_hoje=0,
        total_compras_hoje=0,
        produtos=[],
        notificacoes=[]
    )

# ROTAS DAS AÇÕES DOS FORMULÁRIOS
@app.route('/cadastrar-produto', methods=['POST'])
def cadastrar_produto():
    # Adicione aqui a lógica para salvar produtos
    return redirect(url_for('dashboard'))

@app.route('/repor-estoque', methods=['POST'])
def repor_estoque():
    # Adicione aqui a lógica para repor estoque
    return redirect(url_for('dashboard'))

@app.route('/registrar-venda', methods=['POST'])
def registrar_venda():
    # Adicione aqui a lógica para registrar vendas
    return redirect(url_for('dashboard'))

@app.route('/registrar-compra', methods=['POST'])
def registrar_compra():
    # Adicione aqui a lógica para registrar compras
    return redirect(url_for('dashboard'))

@app.route('/registrar-conta', methods=['POST'])
def registrar_conta():
    # Adicione aqui a lógica para registrar contas a pagar
    return redirect(url_for('dashboard'))

# ROTA DE LOGOUT
@app.route('/logout')
def logout():
    session.clear()  # Limpa os dados da sessão
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)