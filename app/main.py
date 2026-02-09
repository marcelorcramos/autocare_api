from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

#Criar app FastAPI
app = FastAPI(title="AutoCare API", version="1.0.0")

#Modelo de dados (Poderia estar no Schemas)
class Cliente(BaseModel):
    nome : str
    email : str
    telefone : str

clientes_db = []

#Endpoints
@app.get("/")
def home():
    return {"menssagem" : "Bem-vindo ao AutoCare API!" , "status": "online"}

@app.get("/health")
def health():
    return {"status" : "saudável", "clientes_cadastrados" : len(clientes_db)}

#Criar Cliente (Post)
@app.post("/clientes/")
def criar_cliente(cliente: Cliente):
    """Criar novo Cliente"""
    #Adiciona ID automático
    cliente_dict = cliente.dict()
    cliente_dict["id"] = len(clientes_db) + 1

    #Salva na "base de dados"
    clientes_db.append(cliente_dict)

    return {
        "mensagem" : "Cliente criado com sucesso!",
        "cliente" : cliente_dict,
        "total_clientes" : len(clientes_db)
    }

#Listar Clientes (GET)
@app.get("/clientes/")
def listar_clientes():
    """Listar todos os Clientes Criados"""
    return{
        "total" : len(clientes_db),
        "clientes" : clientes_db
    }

#Busca de Clientes por ID (Get com parametro)
@app.get("/clientes/{cliente_id}")
def buscar_cliente(cliente_id: int):
    """Busca de cliente pelo ID"""
    #Converte ID para índice (ID 1 = índice 0)
    if cliente_id < 1 or cliente_id > len(clientes_db):
        return {"erro" : f"Cliente ID {cliente_id} não encontrado"}

    return clientes_db[cliente_id - 1]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


