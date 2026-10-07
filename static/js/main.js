function registrarSaldo(saldo) {
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
        if (response.ok) {
            alert("Saldo salvo com sucesso!");
            window.location.reload(); // Recarrega a página atual para atualizar os dados
        } else {
            return response.json().then(data => {
                alert("Erro ao salvar saldo: " + (data.erro || "Erro desconhecido"));
            });
        }
    })
    .catch(error => {
        console.error("Erro na requisição:", error);
        alert("Erro de conexão ao salvar Saldo.");
    });
}
// Função para editar o preço do produto
function editarPreco(codigoProduto) {
    const tipoPreco = prompt('Introduza qual o tipo de preço (Custo/Venda):');
    if (tipoPreco === null) return;
    const tipo = tipoPreco.trim().toLowerCase();
    if (tipo !== 'custo' && tipo !== 'venda') {
        alert("Digite 'Custo' ou 'Venda'.");
        return;
    }

    const novoPreco = prompt(`Introduza o novo preço para o produto (${codigoProduto}):`);
 
    if (novoPreco !== null && novoPreco.trim() !== "") {
        const valorFormatado = parseFloat(novoPreco.replace(',', '.'));
        
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
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Erro ao atualizar o preço do produto.");
            }
        })
        .catch(error => {
            console.error("Erro:", error);
            alert("Falha na comunicação com o servidor.");
        });
    }
}
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
            if (response.ok) {
                window.location.reload();
            } else {
                alert("Erro ao remover o produto.");
            }
        })
        .catch(error => {
            console.error("Erro:", error);
            alert("Falha na comunicação com o servidor.");
        });
    }
}
function toggleNotifications(event) {
    event.stopPropagation();
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.classList.toggle('active');
}

document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('notificationDropdown');
    const wrapper = document.querySelector('.notification-wrapper');
    if (dropdown && !wrapper.contains(event.target)) {
        dropdown.classList.remove('active');
    }
});

function atualizarBadgeNotificacoes() {
    const list = document.getElementById('notificationList');
    const items = list.querySelectorAll('li:not(.no-notifications)');
    const badge = document.getElementById('notificationBadge');

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

function removerNotificacao(button) {
    const li = button.closest('li');
    if (li) {
        li.remove();
        atualizarBadgeNotificacoes();
    }
}

function marcarTodasLidas() {
    const list = document.getElementById('notificationList');
    list.innerHTML = '<li class="no-notifications" style="justify-content: center; color: #888;">Nenhuma notificação no momento.</li>';
    atualizarBadgeNotificacoes();
}

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].classList.remove("active");
    }
    tablinks = document.getElementsByClassName("tab-btn");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }
    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
}


let streamCam = null;

async function iniciarCamera() {
    try {
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

function capturarFoto() {
    const video = document.getElementById('video-preview');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 300;
    canvas.height = video.videoHeight || 200;
    
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    const fotoDataUrl = canvas.toDataURL('image/png');
    document.getElementById('foto_base64').value = fotoDataUrl;
    
    const photoPreview = document.getElementById('photo-preview');
    photoPreview.src = fotoDataUrl;
    photoPreview.style.display = 'block';
    video.style.display = 'none';
    
    if (streamCam) {
        streamCam.getTracks().forEach(track => track.stop());
    }
    
    document.getElementById('btn-capturar').style.display = 'none';
    document.getElementById('btn-camera').style.display = 'block';
    document.getElementById('btn-camera').innerText = 'Tirar Outra Foto';
}
function criarCamposVenda() {
    const numero = parseInt(
        document.getElementById("numero-produtos-venda").value
    );

    const container = document.getElementById("produtos-venda");

    container.innerHTML = "";

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
function criarCamposCompra() {
    const numero = parseInt(
        document.getElementById("numero-produtos-compra").value
    );

    const container = document.getElementById("produtos-compra");

    container.innerHTML = "";

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