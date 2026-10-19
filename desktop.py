import threading
import time
import webview

from app import app


def iniciar_flask(): # inicia server flask
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":
    servidor = threading.Thread(
        target=iniciar_flask, # chama a função iniciar_flask
        daemon=True
    )

    servidor.start()

    time.sleep(1)

    webview.create_window( # cria a janela com o server
        "Leet Empresas",
        "http://127.0.0.1:5000",
        width=1280,
        height=800,
        resizable=True
    )

    webview.start()