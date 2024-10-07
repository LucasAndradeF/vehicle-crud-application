document.addEventListener("DOMContentLoaded", () => {
  // Função para obter o valor de um parâmetro da URL
  function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  // Obter o ID do veículo da URL
  const id = getQueryParam("id");
  const formAlterar = document.getElementById("form-alterar");
  const formBusca = document.getElementById("form-busca");

  // Verificar se o ID está presente na URL
  if (id) {
    // Buscar as informações do veículo na API
    fetch(`http://127.0.0.1:5000/veiculos/${id}`)
      .then((response) => {
        if (!response.ok) throw new Error("Erro ao buscar veículo.");
        return response.json();
      })
      .then((veiculo) => {
        // Preencher os campos do formulário com os dados do veículo
        document.getElementById("marca").value = veiculo.marca || "";
        document.getElementById("modelo").value = veiculo.modelo || "";
        document.getElementById("ano").value = veiculo.ano || "";
        document.getElementById("preco").value = veiculo.preco.toFixed(2) || "";
      })
      .catch((error) => {
        console.error("Erro ao carregar os dados do veículo:", error);
        alert("Erro ao carregar os dados do veículo. Veículo não encontrado");
      });
  }

  // Adicionar o evento de submit ao formulário de alteração
  if (formAlterar) {
    formAlterar.addEventListener("submit", async (event) => {
      event.preventDefault(); // Impede o envio padrão do formulário

      const marca = document.getElementById("marca").value;
      const modelo = document.getElementById("modelo").value;
      const ano = document.getElementById("ano").value;
      const preco = document.getElementById("preco").value;

      const veiculoAtualizado = {
        marca,
        modelo,
        ano: parseInt(ano),
        preco: parseFloat(preco),
      };

      try {
        const response = await fetch(`http://127.0.0.1:5000/veiculos/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(veiculoAtualizado),
        });

        if (response.ok) {
          alert("Veículo atualizado com sucesso!");
          window.location.href = "dashboard.html"; // Redireciona após sucesso
        } else {
          alert("Erro ao atualizar o veículo.");
          console.error("Erro na resposta:", await response.text());
        }
      } catch (error) {
        console.error("Erro ao atualizar o veículo:", error);
        alert("Erro ao salvar as alterações.");
      }
    });
  } else {
    console.error("Formulário de alteração não encontrado.");
  }

  // Adicionar o evento de submit ao formulário de busca
  if (formBusca) {
    formBusca.addEventListener("submit", function (event) {
      event.preventDefault(); // Impede o envio padrão do formulário

      // Pega o ID do veículo digitado
      const id = document.getElementById("id").value;

      // Redireciona para a página de alteração com o ID na URL
      window.location.href = `dados-veiculos.html?id=${id}`;
    });
  }
});

// Função para listar veículos na tabela
function listarVeiculos() {
  fetch("http://127.0.0.1:5000/veiculos")
    .then((response) => {
      console.log("Resposta da API:", response); // Exibe a resposta completa no console
      return response.json();
    })
    .then((veiculos) => {
      // Seleciona o tbody da tabela onde os dados serão inseridos
      const listarVeiculos = document.querySelector("#tabela-veiculos");
      if (!listarVeiculos) return;
      // Limpa o tbody antes de adicionar novos dados (opcional)
      listarVeiculos.innerHTML = "";

      veiculos.forEach((veiculo) => {
        // Cria uma nova linha para cada veículo
        const itemVeiculos = document.createElement("tr");

        // Cria células para cada propriedade do veículo
        itemVeiculos.innerHTML = `
                  <td>${veiculo.id}</td>
                  <td>${veiculo.marca}</td>
                  <td>${veiculo.modelo}</td>
                  <td>${veiculo.ano}</td>
                  <td>R$ ${veiculo.preco.toFixed(2)}</td>
                  <td><button class="button is-warning" onclick="editarVeiculo(${
                    veiculo.id
                  })">Alterar</button></td>
                  <td><button class="button is-danger" onclick="deleteItem(${
                    veiculo.id
                  })">Excluir</button></td>
              `;

        // Adiciona a nova linha ao tbody
        listarVeiculos.appendChild(itemVeiculos);
      });
    })
    .catch((error) => {
      console.error("Erro na requisição:", error);
      alert("Falha ao se conectar com a API.");
    });
}

// Função para deletar um veículo
async function deleteItem(id) {
  const resposta = confirm("Tem certeza que deseja excluir esse veículo?");
  if (resposta) {
    try {
      const response = await fetch(`http://127.0.0.1:5000/veiculos/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        console.log(`Veículo ${id} deletado com sucesso`);
        // Atualiza a lista após a exclusão
        listarVeiculos();
      } else {
        console.error("Erro ao deletar o veículo:", response.statusText);
      }
    } catch (error) {
      console.error("Erro na requisição de exclusão:", error);
    }
    alert("Veículo excluído com sucesso!");
  } else {
    alert("Ação cancelada");
  }
}

function editarVeiculo(id) {
  window.location.href = `dados-veiculos.html?id=${id}`;
}

// Chamada inicial para listar veículos na tabela
listarVeiculos();
