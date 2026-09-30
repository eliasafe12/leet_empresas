# GERADO POR IA
# GERADO POR IA
# GERADO POR IA
# GERADO POR IA
# GERADO POR IA

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    # Redireciona a rota inicial para a tela de login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        # Lógica de validação do login futuramente
        return "Login efetuado com sucesso!"
        
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        nome_empresa = request.form.get('nome_empresa')
        senha = request.form.get('senha')
        
        # Futuramente: salvar nome, nome_empresa e senha no banco de dados
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')


if __name__ == '__main__':
    app.run(debug=True)
    