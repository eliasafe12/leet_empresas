# =========================================================
# Servidor Flask Completo para LeetEmpresas
# =========================================================

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de dados temporária (Simulação)
produtos_db = [
    {
        "nome": "Detergente Líquido",
        "codigo": "10101010",
        "quantidade": 50,
        "preco": 5.00,
        "valor_custo": 2.50,
        "foto_url": None
    }
]

# Registos temporários de transações
vendas_db = [
    {"codigo": "10101010", "quantidade": 10, "valor_total": 50.00, "data": "2026-10-05"}
]

compras_db = [
    {"codigo": "10101010", "quantidade": 20, "valor_total": 100.00, "data": "2026-10-05"},
    {"codigo": "10101010", "quantidade": 10, "valor_total": 50.00, "data": "2026-10-05"}
]

# Registos temporários de contas a pagar
contas_db = [
    {"descricao": "Energia Elétrica / Luz", "valor": 250.00, "vencimento": "2026-10-15"}
]

# Avisos do sistema
notificacoes_db = [
    "⚠️ AVISO: Existe uma conta de luz pendente com vencimento próximo!",
    "ℹ️ 1 venda registrada hoje (R$ 50,00).",
    "ℹ️ 2 compras de estoque registradas hoje (R$ 150,00 total)."
]

# ---------------------------------------------------------
# ROTAS PRINCIPAIS DE NAVEGAÇÃO
# ---------------------------------------------------------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    # Cálculo dinâmico dos totais
    total_vendas = sum(v['valor_total'] for v in vendas_db)   # R$ 50.00
    total_compras = sum(c['valor_total'] for c in compras_db) # R$ 150.00
    saldo_dia = total_vendas - total_compras                  # R$ -100.00

    return render_template(
        'paginaPrincipal.html',
        nome_empresa="Minha Empresa",
        nome_usuario="Usuário",
        total_produtos=len(produtos_db),
        produtos=produtos_db,
        vendas=vendas_db,       # <--- Passado para a aba de Vendas
        compras=compras_db,     # <--- Passado para a aba de Compras
        contas=contas_db,       # <--- Passado para a aba de Contas e Dashboard
        saldo_dia=saldo_dia,
        total_vendas_hoje=total_vendas,
        total_compras_hoje=total_compras,
        notificacoes=notificacoes_db
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# ---------------------------------------------------------
# ROTAS DE AÇÕES E FORMULÁRIOS (POSTs)
# ---------------------------------------------------------

@app.route('/cadastrar-produto', methods=['POST'])
def cadastrar_produto():
    nome = request.form.get('nome')
    codigo = request.form.get('codigo', '10101010')
    valor_venda = float(request.form.get('valor_venda', 0))
    valor_custo = float(request.form.get('valor_custo', 0))
    quantidade = int(request.form.get('quantidade', 0))
    foto_base64 = request.form.get('foto_base64')

    produtos_db.append({
        "nome": nome,
        "codigo": codigo,
        "quantidade": quantidade,
        "preco": valor_venda,
        "valor_custo": valor_custo,
        "foto_url": foto_base64 if foto_base64 else None
    })
    
    notificacoes_db.insert(0, f"✅ Produto '{nome}' cadastrado com sucesso!")
    return redirect(url_for('dashboard'))

@app.route('/registrar-venda', methods=['POST'])
def registrar_venda():
    codigo = request.form.get('codigo')
    qtd = int(request.form.get('quantidade', 0))
    
    preco = 5.00
    for p in produtos_db:
        if p['codigo'] == codigo:
            preco = p['preco']
            p['quantidade'] -= qtd
            break
            
    valor_total = preco * qtd
    vendas_db.append({"codigo": codigo, "quantidade": qtd, "valor_total": valor_total, "data": "2026-10-05"})
    notificacoes_db.insert(0, f"💰 Venda efetuada: {qtd}x item ({codigo}) - Total: R$ {valor_total:.2f}")
    
    return redirect(url_for('dashboard'))

@app.route('/registrar-compra', methods=['POST'])
def registrar_compra():
    codigo = request.form.get('codigo')
    qtd = int(request.form.get('quantidade', 0))
    
    custo_unitario = 5.00
    valor_total = custo_unitario * qtd
    
    compras_db.append({"codigo": codigo, "quantidade": qtd, "valor_total": valor_total, "data": "2026-10-05"})
    
    for p in produtos_db:
        if p['codigo'] == codigo:
            p['quantidade'] += qtd
            break
            
    notificacoes_db.insert(0, f"📦 Compra de estoque: {qtd}x item ({codigo}) - Total: R$ {valor_total:.2f}")
    return redirect(url_for('dashboard'))

@app.route('/registrar-conta', methods=['POST'])
def registrar_conta():
    descricao = request.form.get('descricao')
    valor = float(request.form.get('valor', 0))
    vencimento = request.form.get('vencimento')
    
    # Adiciona a conta à base de dados de contas
    contas_db.append({
        "descricao": descricao,
        "valor": valor,
        "vencimento": vencimento
    })
    
    notificacoes_db.insert(0, f"⚠️ Nova conta registrada: {descricao} - R$ {valor:.2f} (Vencimento: {vencimento})")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)