# app/models.py
from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):
    nome: str
    email: str
    telefone: str

class Veiculo(BaseModel):
    placa: str
    marca: str
    modelo: str
    ano: int
    cor: Optional[str] = None
    cliente_id: int  # ID do dono do veículo