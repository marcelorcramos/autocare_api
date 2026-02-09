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
    

