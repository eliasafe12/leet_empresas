// envia o saldo do dia para o servidor e recarrega a página quando ele é salvo
function registrarSaldo(saldo) {
    // envia o saldo em json junto com o token csrf lido da página
    fetch('/registrar-saldo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({
            saldo: parseFloat(saldo)
        })
    })
    .then(response => {
        // confirma o salvamento e atualiza a página quando o servidor responde com sucesso
        if (response.ok) {
            alert("Saldo salvo com sucesso!");
            window.location.reload(); // Recarrega a página atual para atualizar os dados
        } else {
            // mostra a mensagem de erro enviada pelo servidor
            return response.json().then(data => {
                alert("Erro ao salvar saldo: " + (data.erro || "Erro desconhecido"));
            });
        }
    })
    // informa falhas de comunicação com o servidor
    .catch(error => {
        console.error("Erro na requisição:", error);
        alert("Erro de conexão ao salvar Saldo.");
    });
}
// Função para editar o preço do produto
function editarPreco(codigoProduto) {
    // pergunta qual dos preços será alterado
    const tipoPreco = prompt('Introduza qual o tipo de preço (Custo/Venda):');
    if (tipoPreco === null) return;
    // padroniza a resposta para letras minúsculas
    const tipo = tipoPreco.trim().toLowerCase();
    // aceita somente os tipos custo e venda
    if (tipo !== 'custo' && tipo !== 'venda') {
        alert("Digite 'Custo' ou 'Venda'.");
        return;
    }

    // pergunta o novo valor do preço
    const novoPreco = prompt(`Introduza o novo preço para o produto (${codigoProduto}):`);
 
    if (novoPreco !== null && novoPreco.trim() !== "") {
        // troca a vírgula por ponto e converte o texto em número
        const valorFormatado = parseFloat(novoPreco.replace(',', '.'));
        
        // impede valores que não sejam números ou que sejam negativos
        if (isNaN(valorFormatado) || valorFormatado < 0) {
            alert("Por favor, introduza um valor numérico válido.");
            return;
        }

        // Envio do formulário para a rota de edição de preço
        fetch('/editar-preco', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({
                codigo: codigoProduto,
                novo_preco: valorFormatado,
                tipo_preco: tipo // Envia o tipo de preço em minúsculas
            })
        })
        .then(response => {
            // recarrega a página para mostrar o novo preço quando a atualização funciona
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Erro ao atualizar o preço do produto.");
            }
        })
        // informa falhas de comunicação com o servidor
        .catch(error => {
            console.error("Erro:", error);
            alert("Falha na comunicação com o servidor.");
        });
    }
}
// pede confirmação e remove um item, que pode ser produto, venda, compra ou conta
function removerItem(codigoItem, tipo) {
    if (confirm(`Tem certeza que deseja remover o item com código ${codigoItem}?`)) {
        // Envio do formulário para a rota de remoção de item
        fetch('/remover-item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            },
            body: JSON.stringify({
                codigo: codigoItem,
                tipo: tipo // Envia o tipo de item (produto, venda, compra, conta)
            })
        })
        .then(response => {
            // recarrega a página para retirar da lista o item removido
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Erro ao remover o produto.");
            }
        })
        // informa falhas de comunicação com o servidor
        .catch(error => {
            console.error("Erro:", error);
            alert("Falha na comunicação com o servidor.");
        });
    }
}
// abre ou fecha a lista de notificações
function toggleNotifications(event) {
    // impede que o clique feche a lista logo depois de abri-la
    event.stopPropagation();
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.classList.toggle('active');
}

// fecha a lista de notificações quando o clique acontece fora dela
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('notificationDropdown');
    const wrapper = document.querySelector('.notification-wrapper');
    if (dropdown && !wrapper.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});

// atualiza o número exibido no ícone de notificações
function atualizarBadgeNotificacoes() {
    const list = document.getElementById('notificationList');
    // conta as notificações que ainda estão na lista
    const items = list.querySelectorAll('li:not(.no-notifications)');
    const badge = document.getElementById('notificationBadge');

    // mostra o número de notificações quando existem e esconde o ícone quando a lista está vazia
    if (items.length > 0) {
        if (badge) {
            badge.innerText = items.length;
            badge.style.display = 'flex';
        }
    } else {
        if (badge) {
            badge.style.display = 'none';
        }
        list.innerHTML = '<li class="no-notifications" style="justify-content: center; color: #888;">Nenhuma notificação no momento.</li>';
    }
}

// remove da lista a notificação do botão clicado
function removerNotificacao(button) {
    const li = button.closest('li');
    if (li) {
        li.remove();
        atualizarBadgeNotificacoes();
    }
}

// limpa a lista e mostra a mensagem de que não há notificações
function marcarTodasLidas() {
    const list = document.getElementById('notificationList');
    list.innerHTML = '<li class="no-notifications" style="justify-content: center; color: #888;">Nenhuma notificação no momento.</li>';
    atualizarBadgeNotificacoes();
}

// mostra a aba escolhida e esconde as demais
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    // esconde o conteúdo de todas as abas
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    // remove o destaque de todos os botões de aba
    tablinks = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    // mostra a aba escolhida e destaca o botão clicado
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}


// guarda o fluxo da câmera para poder desligá-la depois
let streamCam = null;

// liga a câmera e mostra a imagem ao vivo no lugar da foto
async function iniciarCamera() {
    try {
        // pede permissão para usar a câmera
        streamCam = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.getElementById('video-preview');
        video.srcObject = streamCam;
        video.style.display = 'block';
        document.getElementById('photo-preview').style.display = 'none';
        document.getElementById('btn-camera').style.display = 'none';
        document.getElementById('btn-capturar').style.display = 'block';
    } catch (err) {
        alert('Não foi possível acessar a câmara: ' + err.message);
    }
}

// tira a foto a partir da imagem da câmera, reduz o tamanho e guarda o resultado em base64
function capturarFoto() {
    const video = document.getElementById('video-preview');
    const canvas = document.createElement('canvas');
    // limita a largura da imagem a 800 pixels
    const larguraMax = 800;
    let w = video.videoWidth || 300;
    let h = video.videoHeight || 200;
    if (w > larguraMax) {
        h = Math.round(h * larguraMax / w);
        w = larguraMax;
    }
    canvas.width = w;
    canvas.height = h;

    // desenha o quadro atual do vídeo no canvas
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, w, h);

    // JPEG com qualidade 0.8 pesa uma fração do PNG
    const fotoDataUrl = canvas.toDataURL('image/jpeg', 0.8);
    document.getElementById('foto_base64').value = fotoDataUrl;
    
    const photoPreview = document.getElementById('photo-preview');
    photoPreview.src = fotoDataUrl;
    photoPreview.style.display = 'block';
    video.style.display = 'none';
    
    // desliga a câmera depois de capturar a foto
    if (streamCam) {
        streamCam.getTracks().forEach(track => track.stop());
    }
    
    document.getElementById('btn-capturar').style.display = 'none';
    document.getElementById('btn-camera').style.display = 'block';
    document.getElementById('btn-camera').innerText = 'Tirar Outra Foto';
}
// cria os campos de código e quantidade conforme o número de produtos da venda
function criarCamposVenda() {
    // lê quantos produtos terão campos
    const numero = parseInt(
        document.getElementById("numero-produtos-venda").value
    );

    const container = document.getElementById("produtos-venda");

    // limpa os campos criados anteriormente
    container.innerHTML = "";

    // cria um bloco de campos para cada produto
    for (let i = 0; i < numero; i++) {
        container.innerHTML += `
            <div class="movimentacao">
                <h4>Produto ${i + 1}</h4>

                <label>Código do Produto:</label>
                <input 
                    type="text" 
                    name="codigo[]" 
                    placeholder="Código"
                    required
                >

                <label>Quantidade Vendida:</label>
                <input 
                    type="number" 
                    name="quantidade[]" 
                    placeholder="Quantidade"
                    min="1"
                    required
                >
            </div>
        `;
    }
}
// cria os campos de código e quantidade conforme o número de produtos da compra
function criarCamposCompra() {
    // lê quantos produtos terão campos
    const numero = parseInt(
        document.getElementById("numero-produtos-compra").value
    );

    const container = document.getElementById("produtos-compra");

    // limpa os campos criados anteriormente
    container.innerHTML = "";

    // cria um bloco de campos para cada produto
    for (let i = 0; i < numero; i++) {
        container.innerHTML += `
            <div class="movimentacao">
                <h4>Produto ${i + 1}</h4>

                <label>Código do Produto:</label>
                <input 
                    type="text" 
                    name="codigo[]" 
                    placeholder="Código"
                    required
                >

                <label>Quantidade Comprada:</label>
                <input 
                    type="number" 
                    name="quantidade[]" 
                    placeholder="Quantidade"
                    min="1"
                    required
                >
            </div>
        `;
    }
}