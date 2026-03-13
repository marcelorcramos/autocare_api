const API_ENDPOINTS = {
  clientes: "/clientes/",
  funcionarios: "/funcionarios/",
  veiculos: "/veiculos/"
};

const TABLE_CONFIG = {
  clientes: {
    tbodyId: "tbody-clientes",
    statusId: "status-clientes",
    listKey: "clientes",
    columns: ["id", "nome", "email", "telefone"]
  },
  funcionarios: {
    tbodyId: "tbody-funcionarios",
    statusId: "status-funcionarios",
    listKey: "funcionarios",
    columns: ["id", "nome", "area", "nivel"]
  },
  veiculos: {
    tbodyId: "tbody-veiculos",
    statusId: "status-veiculos",
    listKey: "veiculos",
    columns: ["id", "placa", "marca", "modelo"]
  }
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function setStatus(resource, message, mode = "success") {
  const status = document.getElementById(TABLE_CONFIG[resource].statusId);
  status.textContent = message;
  status.className = `status ${mode}`;
}

function renderTable(resource, items) {
  const { tbodyId, columns } = TABLE_CONFIG[resource];
  const tbody = document.getElementById(tbodyId);

  if (!Array.isArray(items) || items.length === 0) {
    tbody.innerHTML = '<tr><td colspan="4" class="empty">Nenhum registro encontrado.</td></tr>';
    return;
  }

  const rows = items
    .map((item) => {
      const cells = columns
        .map((column) => `<td>${escapeHtml(item[column])}</td>`)
        .join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  tbody.innerHTML = rows;
}

async function carregarRecurso(resource) {
  const endpoint = API_ENDPOINTS[resource];
  const { listKey } = TABLE_CONFIG[resource];

  setStatus(resource, "Carregando...", "loading");

  try {
    const response = await fetch(endpoint, {
      method: "GET",
      headers: {
        Accept: "application/json"
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    const items = payload[listKey] ?? [];

    renderTable(resource, items);
    setStatus(resource, `${items.length} registro(s) carregado(s).`, "success");
  } catch (error) {
    console.error(`Erro ao buscar ${resource}:`, error);
    setStatus(resource, "Falha ao conectar com a API.", "error");
  }
}

function bindButtons() {
  const buttons = document.querySelectorAll("button[data-resource]");

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      const resource = button.getAttribute("data-resource");
      carregarRecurso(resource);
    });
  });

  document.getElementById("load-all").addEventListener("click", async () => {
    await Promise.all([
      carregarRecurso("clientes"),
      carregarRecurso("funcionarios"),
      carregarRecurso("veiculos")
    ]);
  });
}

function init() {
  const apiBaseElement = document.getElementById("api-base-value");
  apiBaseElement.textContent = window.location.origin;
  bindButtons();
  bindBuscaCliente();
}

function bindBuscaCliente() {
  const btnBuscar = document.getElementById("btn-buscar-cliente");
  const inputId = document.getElementById("cliente-id-input");

  btnBuscar.addEventListener("click", () => {
    const id = inputId.value.trim();
    if (!id) {
      setStatusBusca("Por favor, digite um ID válido", "error");
      return;
    }
    buscarClientePorId(id);
  });

  // Permitir buscar ao pressionar Enter no input
  inputId.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      btnBuscar.click();
    }
  });
}

async function buscarClientePorId(id) {
  const endpoint = `/clientes/${id}`;

  setStatusBusca("Buscando cliente...", "loading");

  try {
    const response = await fetch(endpoint, {
      method: "GET",
      headers: {
        Accept: "application/json"
      }
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error("Cliente não encontrado!");
      }
      throw new Error(`HTTP ${response.status}`);
    }

    const cliente = await response.json();
    renderClienteCard(cliente);
    setStatusBusca("Cliente encontrado!", "success");
  } catch (error) {
    console.error(`Erro ao buscar cliente:`, error);
    setStatusBusca(
      error.message === "Cliente não encontrado!"
        ? "Cliente não encontrado. Tente outro ID."
        : "Falha ao conectar com a API.",
      "error"
    );
    
    const container = document.getElementById("resultado-cliente");
    container.innerHTML = "";
    container.classList.remove("empty");
  }
}

function renderClienteCard(cliente) {
  const container = document.getElementById("resultado-cliente");

  const card = `
    <div class="cliente-card">
      <h3>${escapeHtml(cliente.nome)}</h3>
      <div class="cliente-field">
        <span class="cliente-field-label">ID:</span>
        <span class="cliente-field-value">${cliente.id}</span>
      </div>
      <div class="cliente-field">
        <span class="cliente-field-label">Email:</span>
        <span class="cliente-field-value">${escapeHtml(cliente.email)}</span>
      </div>
      <div class="cliente-field">
        <span class="cliente-field-label">Telefone:</span>
        <span class="cliente-field-value">${escapeHtml(cliente.telefone)}</span>
      </div>
      <div class="cliente-field">
        <span class="cliente-field-label">NIF:</span>
        <span class="cliente-field-value">${escapeHtml(cliente.nif)}</span>
      </div>
      <div class="cliente-field">
        <span class="cliente-field-label">Data de Nascimento:</span>
        <span class="cliente-field-value">${escapeHtml(cliente.data_nascimento)}</span>
      </div>
    </div>
  `;

  container.innerHTML = card;
  container.classList.remove("empty");
}

function setStatusBusca(message, mode = "success") {
  const status = document.getElementById("status-busca-cliente");
  status.textContent = message;
  status.className = `status ${mode}`;
}

document.addEventListener("DOMContentLoaded", init);
