from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    # Redireciona a rota inicial para a tela de login
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Aqui no futuro validaremos com as classes de models (POO)
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        print(f"Tentativa de login -> Usuário: {usuario}, Senha: {senha}")
        
        # Após o login, futuramente redirecionamos para a interface do usuário
        return f"Login recebido com sucesso para o usuário: {usuario}"

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)