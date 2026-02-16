from fastapi import APIRouter
from app.models import Cliente
from app.database import clientes_db
from typing import Optional
import re

# Criar router específico para clientes
router = APIRouter(prefix="/clientes", tags=["Clientes"]) 

@router.post("/")
def criar_cliente(cliente: Cliente):
    """Criar novo Cliente"""
    cliente_dict = cliente.dict()
    cliente_dict["id"] = len(clientes_db) + 1
    clientes_db.append(cliente_dict)

    return {
        "mensagem": "Cliente criado com sucesso!",
        "cliente": cliente_dict,
        "total_clientes": len(clientes_db)
    }

@router.get("/")
def listar_clientes():
    """Listar todos os Clientes"""
    return {
        "total": len(clientes_db),
        "clientes": clientes_db
    }

@router.get("/{cliente_id}")
def buscar_cliente(cliente_id: int):
    """Buscar cliente pelo ID"""
    #For para evitar possíveis clientes excluídos
    for cliente in clientes_db:
        if cliente["id"] == cliente_id:
            return cliente
    #Tratamento erro    
    return {"erro" : f"Cliente ID {cliente_id} não encontrado!"}

@router.get("/clientes/busca/")
def buscar_clientes(
    nome: Optional[str] = None,
    email: Optional[str] = None,
    nif: Optional[str] = None,
    ordenar_por: str = "id",
    ordem: str = "asc"
):
    """Busca avançada de clientes"""
    resultados = clientes_db.copy()

    #Filtros
    if nome:
        resultados = [c for c in resultados if nome.lower() in c["nome"].lower()]

    if email:
        resultados = [c for c in resultados if email.lower() in c["email"].lower()]
    
    if nif:
        nif_limpo = re.sub(r'\D', '', nif)
        resultados = [c for c in resultados if nif_limpo in c["nif"]]
  
    #Ordenação
    reverse = (ordem.lower() == "desc")
    resultados.sort(key=lambda x: x.get(ordenar_por, ""), reverse=reverse)

    return{
        "total": len(resultados),
        "filtros": {"nome": nome, "email": email, "nif": nif},
        "ordenacao": {"por": ordenar_por, "ordem": ordem},
        "clientes": resultados
    }


@router.put("/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente_atualizado: Cliente):
    """Atualizar cliente existente"""
    for indice, cliente in enumerate(clientes_db):
        if cliente["id"] == cliente_id:
            cliente_dict = cliente_atualizado.dict()
            cliente_dict["id"] = cliente_id
            clientes_db[indice] = cliente_dict

            return{
                "mensagem" : f"Cliente ID {cliente_id} atualizado!",
                "cliente" : cliente_dict
            }

    return {
        "erro" : f"Cliente ID {cliente_id} não encontrado!"
    }

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int):
    """Remover cliente"""
    for indice, cliente in enumerate(clientes_db):
        if cliente["id"] == cliente_id:
            cliente_removido = clientes_db.pop(indice)

            return {
                "mensagem": f"Cliente ID {cliente_id} removido!",
                "cliente_removido": cliente_removido,
                "total_clientes": len(clientes_db)
            }
            
    return {"erro": f"Cliente ID {cliente_id} não encontrado"}


