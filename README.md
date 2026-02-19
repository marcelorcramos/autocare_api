# 🚗 **AutoCare API**

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📋 **Sobre o Projeto**

**AutoCare API** é uma API RESTful em desenvolvimento para gestão de oficinas mecânicas e concessionárias. Com o principal objetivo de aprender e desenvolver novas skills. O projeto está em constante evolução, com novos endpoints e funcionalidades sendo adicionados regularmente.

### 🎯 **Objetivo**
Fornecer uma solução completa para gerenciamento de:
- Clientes e seus veículos
- Agendamentos de serviços
- Gestão de oficina
- Futuramente: faturamento, estoque e relatórios

---

## 🚀 **Tecnologias Utilizadas**

- **FastAPI** - Framework web moderno e rápido
- **Python 3.12+** - Linguagem de programação
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI
- **Swagger UI** - Documentação interativa automática

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
pip install fastapi uvicorn

# Execute a API
uvicorn app.main:app --reload
```

### **Acesse a Documentação**
Após executar, abra no navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📌 **Funcionalidades Atuais**

O projeto está em desenvolvimento ativo. Atualmente implementamos:

✅ **CRUD completo de Clientes**  
✅ **CRUD completo de Veículos**  
✅ **Validações de dados** (NIF, telefone, placa portuguesa)  
✅ **Busca avançada com filtros**  
✅ **Relacionamento Cliente ↔ Veículos**

---

## 🗺️ **Roadmap (Em Evolução)**

### 🔜 **Próximas Implementações**
- [ ] Agendamentos de serviços
- [ ] Catálogo de serviços
- [ ] Dashboard com estatísticas
- [ ] Relatórios gerenciais
- [ ] Validators (email, ...)

### 🔮 **Futuro**
- [ ] Autenticação JWT
- [ ] Banco de dados PostgreSQL
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

**Autor**: Marcelo Ramos | 
**Email**: marcelorcramos@gmail.com

---

## ⚠️ **Nota Importante**

> Este README será atualizado conforme o projeto evolui.  
> Para documentação detalhada e atualizada dos endpoints, consulte a **documentação interativa** em `/docs` após executar a API.

---

**🚗 Em constante evolução...**
