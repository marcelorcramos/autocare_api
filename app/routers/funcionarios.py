from fastapi import APIRouter
from app.models import Funcionario
from app.database import funcionarios_db
from typing import Optional
import re

# Criar router específico para clientes
router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])

@router.post("/")
def criar_funcionario(funcionario: Funcionario):
    """Criar novo Funcionário"""
    funcionario_dict = funcionario.dict()
    funcionario_dict["id"] = len(funcionarios_db) + 1
    funcionarios_db.append(funcionario_dict)

    return{
        "mensagem": "Funcionário criado com sucesso!",
        "cliente": funcionario_dict,
        "total_funcionarios": len(funcionarios_db)
    }