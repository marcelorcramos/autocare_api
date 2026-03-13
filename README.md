# 🚗 **AutoCare API**

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📋 **Sobre o Projeto**

**AutoCare API** é uma API RESTful em desenvolvimento para gestão de oficinas mecânicas e concessionárias. Com o principal objetivo de aprender e desenvolver novas skills. O projeto está em constante evolução, com novos endpoints e funcionalidades sendo adicionados regularmente.

### 🎯 **Objetivo**
Fornecer uma solução completa para gerenciamento de:
- Clientes e seus veículos
- Funcionários da oficina
- Agendamentos de serviços
- Gestão de oficina
- Futuramente: faturamento, estoque e relatórios

---

## 🚀 **Tecnologias Utilizadas**

- **FastAPI** - Framework web moderno e rápido
- **Python 3.12+** - Linguagem de programação
- **SQLAlchemy 2.0** - ORM para mapeamento objeto-relacional
- **SQLite** - Banco de dados relacional (ficheiro local `autocare.db`)
- **Pydantic v2** - Validação de dados de entrada/saída
- **Uvicorn** - Servidor ASGI
- **Swagger UI** - Documentação interativa automática

---

## 📁 **Estrutura do Projeto**

```
autocare_api/
├── app/
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada da API (FastAPI app)
│   ├── database.py          # Configuração SQLAlchemy (engine, sessão, Base)
│   ├── db_models.py         # Modelos ORM — tabelas no banco de dados
│   ├── models.py            # Modelos Pydantic — validação de dados
│   ├── requirements.txt     # Dependências do projeto
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── clientes.py      # Endpoints CRUD de Clientes
│   │   ├── funcionarios.py  # Endpoints CRUD de Funcionários
│   │   └── veiculos.py      # Endpoints CRUD de Veículos
│   └── schemas/
│       ├── __init__.py
│       ├── cliente.py        # Schemas Create/Response de Cliente
│       ├── funcionario.py    # Schemas Create/Response de Funcionário
│       └── veiculo.py        # Schemas Create/Response de Veículo
├── seed_db.py               # Script para popular o banco com dados de exemplo
├── LICENSE
└── README.md
```

---

## ⚙️ **Como Executar**

### **Pré-requisitos**
- Python 3.12 ou superior
- pip (gerenciador de pacotes)

### **Instalação Rápida**

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/autocare-api.git
cd autocare-api

# Crie e ative ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # No Mac/Linux
# venv\Scripts\activate   # No Windows

# Instale as dependências
pip install -r app/requirements.txt

# (Opcional) Popular o banco com dados de exemplo
python seed_db.py

# Execute a API
uvicorn app.main:app --reload
```

### **Acesse a Documentação**
Após executar, abra no navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Frontend Demo**: http://localhost:8000/frontend

---

## 📌 **Funcionalidades Atuais**

### ✅ **Implementado**

| Recurso | Descrição |
|---------|-----------|
| **CRUD Clientes** | Criar, listar, buscar, atualizar e remover clientes |
| **CRUD Veículos** | Criar, listar, buscar, atualizar e remover veículos |
| **CRUD Funcionários** | Criar, listar, buscar, atualizar e remover funcionários |
| **Banco de dados SQLite** | Persistência de dados com SQLAlchemy ORM |
| **Validações robustas** | NIF (9 dígitos), email, telefone PT, placa PT (AA-00-AA), idade mínima 18 anos |
| **Validações de Funcionários** | Nível (Part Time / Full Time), salário mínimo por nível (460€ / 920€) |
| **Busca avançada** | Filtros por nome, email, NIF, área, nível + ordenação (asc/desc) |
| **Relacionamento Cliente ↔ Veículos** | Um cliente pode ter vários veículos |
| **Veículos por cliente** | Endpoint dedicado para listar veículos de um cliente específico |
| **Schemas separados** | Schemas Pydantic organizados (Create/Response) no pacote `schemas/` |
| **Seed script** | Script para popular o banco com dados de exemplo para testes |
| **Health check** | Endpoint `/health` com contagem de registos no banco |

---

## 🔗 **Endpoints da API**

### 🏠 **Geral**
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/` | Página inicial — status da API |
| `GET` | `/health` | Health check com estatísticas do banco |

### 👤 **Clientes** (`/clientes`)
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/clientes/` | Criar novo cliente |
| `GET` | `/clientes/` | Listar todos os clientes |
| `GET` | `/clientes/busca/` | Busca avançada (nome, email, NIF, ordenação) |
| `GET` | `/clientes/{id}` | Buscar cliente por ID |
| `PUT` | `/clientes/{id}` | Atualizar cliente |
| `DELETE` | `/clientes/{id}` | Remover cliente |

### 🚗 **Veículos** (`/veiculos`)
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/veiculos/` | Criar novo veículo |
| `GET` | `/veiculos/` | Listar todos os veículos |
| `GET` | `/veiculos/busca/` | Busca avançada (placa, marca, modelo, ordenação) |
| `GET` | `/veiculos/{id}` | Buscar veículo por ID |
| `PUT` | `/veiculos/{id}` | Atualizar veículo |
| `DELETE` | `/veiculos/{id}` | Remover veículo |
| `GET` | `/veiculos/clientes/{id}/veiculos` | Listar veículos de um cliente |

### 👷 **Funcionários** (`/funcionarios`)
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/funcionarios/` | Criar novo funcionário |
| `GET` | `/funcionarios/` | Listar todos os funcionários |
| `GET` | `/funcionarios/busca/` | Busca avançada (nome, NIF, área, nível, ordenação) |
| `GET` | `/funcionarios/{id}` | Buscar funcionário por ID |
| `PUT` | `/funcionarios/{id}` | Atualizar funcionário |
| `DELETE` | `/funcionarios/{id}` | Remover funcionário |

---

## 🛡️ **Validações**

### **Cliente**
- **NIF**: Deve conter exatamente 9 dígitos
- **Email**: Formato válido com `@` e domínio `.com`
- **Telefone**: Entre 9 e 12 dígitos, formatação automática
- **Data de nascimento**: Idade mínima de 18 anos, máxima de 120

### **Funcionário**
- **NIF**: Deve conter exatamente 9 dígitos
- **Telefone**: 9 dígitos (sem indicativo), formatação automática `+351 XXX XXX XXX`
- **Nível**: Apenas `Part Time` ou `Full Time`
- **Salário**: Mínimo de 920€ (Full Time) ou 460€ (Part Time)
- **Data de nascimento**: Idade mínima de 18 anos

### **Veículo**
- **Placa**: Formato português `AA-00-AA` (aceita com ou sem hífens)
- **Cliente ID**: Deve corresponder a um cliente existente

---

## 🗺️ **Roadmap (Em Evolução)**

### 🔜 **Próximas Implementações**
- [ ] Agendamentos de serviços
- [ ] Catálogo de serviços
- [ ] Dashboard com estatísticas
- [ ] Relatórios gerenciais
- [ ] Migração para PostgreSQL

### 🔮 **Futuro**
- [ ] Autenticação JWT
- [ ] Sistema de notificações
- [ ] Gestão de estoque
- [ ] Faturamento

---

## 🧪 **Como Contribuir**

Este é um projeto em evolução. Sugestões e contribuições são bem-vindas!

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

## 📝 **Licença**

Este projeto está sob a licença MIT.

---

## 📞 **Contato**

**Autor**: Marcelo Ramos  
**Email**: marcelorcramos@gmail.com

---

## ⚠️ **Nota Importante**

> Este README será atualizado conforme o projeto evolui.  
> Para documentação detalhada e atualizada dos endpoints, consulte a **documentação interativa** em `/docs` após executar a API.

---

**🚗 Em constante evolução...**
