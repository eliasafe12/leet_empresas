# arquivo que abre o aplicativo em uma janela de desktop
# importa recursos para executar o servidor em paralelo à janela
import threading
# importa recursos para aguardar o servidor iniciar
import time
import socket
import urllib.request
# importa a biblioteca que cria a janela do aplicativo
import webview

# importa a aplicação flask criada no arquivo app
from app import app


def obter_porta_livre():
    # solicita ao sistema operacional uma porta local disponível
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


# escolhe uma porta livre antes de iniciar o servidor
PORTA = obter_porta_livre()


def iniciar_flask(): # inicia server flask
    # executa o servidor apenas na máquina local, sem modo de depuração e sem reiniciar sozinho
    app.run(
        host="127.0.0.1",
        port=PORTA,
        debug=False,
        use_reloader=False
    )


# executa somente quando o arquivo é aberto diretamente
if __name__ == "__main__":
    # cria a thread que roda o servidor flask
    servidor = threading.Thread(
        target=iniciar_flask, # chama a função iniciar_flask
        # encerra o servidor junto com o programa principal
        daemon=True
    )

    # inicia o servidor em segundo plano
    servidor.start()

    # aguarda a resposta do servidor antes de abrir a janela, com limite de tempo
    endereco = f"http://127.0.0.1:{PORTA}"
    for tentativa in range(50):
        try:
            with urllib.request.urlopen(endereco, timeout=0.5):
                break
        except Exception:
            time.sleep(0.2)
    else:
        raise RuntimeError("O servidor local não iniciou corretamente")

    # define o título, o endereço, o tamanho e permite redimensionar a janela
    webview.create_window( # cria a janela com o server
        "Leet Empresas",
        endereco,
        width=1280,
        height=800,
        resizable=True
    )

    # abre a janela e mantém o aplicativo em execução até ela ser fechada
    webview.start()