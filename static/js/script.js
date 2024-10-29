document.getElementById("form-cadastro").addEventListener("submit", async function (event) {
    event.preventDefault(); // Previne o comportamento padrão do formulário

    const formData = new FormData(this); // Pega os dados do formulário
    const data = Object.fromEntries(formData.entries()); // Converte os dados para um objeto JavaScript
    console.log(data)

    try {
        const response = await fetch('http://localhost:5000/api/cadastro', { // Se o servidor do Flask estiver rodando na porta 5000
            method: 'POST', // Envia um JSON em HTTP POST para o backend
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data), // Converte os dados do formulário em JSON
        });

        const responseData = await response.json(); // Transforma a resposta do backend em JSON

        // Aqui você pode usar o "responseData" retornado do backend
        console.log(responseData); // Exemplo de uso
    } catch (error) {
        console.error('Erro ao enviar os dados:', error); // Lida com erros de rede ou resposta
    }
});