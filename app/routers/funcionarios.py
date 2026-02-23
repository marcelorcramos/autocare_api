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

@router.get("/")
def listar_funcionarios():
    """Listar todos os Funcionários"""
    return{
        "total": len(funcionarios_db),
        "funcionarios": funcionarios_db
    }


@router.get("/{funcionario_id}")
def buscar_funcionario(funcionario_id: int):
    """Buscar funcionario pelo ID"""
    for funcionario in funcionarios_db:
        if funcionario["id"] == funcionario_id:
            return funcionario
        
    return {"erro":f"Funcionário ID {funcionario_id} não encontrado!"}

@router.get("/funcionarios/busca/")
def buscar_clientes(
    nome: Optional[str] = None,
    nif: Optional[str] = None,
    area: Optional[str] = None,
    nivel: Optional[str] = None,
    ordenar_por: str =  "id",
    ordem: str= "asc"
):
    """Busca avançada por funcionários"""
    resultados = funcionarios_db.copy()

    if nome:
        resultados = [f for f in resultados if nome.lower() in c["nome"].lower()]

    if nif:
        nif_limpo = re.sub(r'\D','', nif)
        resultados = [f for f in resultados if nif_limpo in c["nif"]]

    reverse = (ordem.lower() == "desc")
    resultados.sort(key=lambda x: x.get(ordenar_por,""),reverse = reverse)

    return{
        "total": len(resultados),
        "filtros":{"nome":nome, "nif": nif},
        "ordenacao": {"por": ordenar_por,"ordem": ordem},
        "funcionarios": resultados
    }