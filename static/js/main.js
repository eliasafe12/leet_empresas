// Função para editar o preço do produto
function editarPreco(codigoProduto) {
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
            },
            body: JSON.stringify({
                codigo: codigoProduto,
                preco: valorFormatado
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