from fastapi import APIRouter
from app.models import Cliente
from app.database import clientes_db

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
    for cliente in clientes_db:
        if cliente["id"] == cliente_id:
            return cliente
    #Tratamento erro    
    return {"erro" : f"Cliente ID {cliente_id} não encontrado!"}

@router.put("/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente_atualizado: Cliente):
    """Atualizar cliente existente"""
    if cliente_id < 1 or cliente_id > len(clientes_db):
        return {"erro": f"Cliente ID {cliente_id} não encontrado"}
    
    cliente_dict = cliente_atualizado.dict()
    cliente_dict["id"] = cliente_id
    clientes_db[cliente_id - 1] = cliente_dict
    
    return {
        "mensagem": f"Cliente ID {cliente_id} atualizado!",
        "cliente": cliente_dict
    }

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int):
    """Remover cliente"""
    if cliente_id < 1 or cliente_id > len(clientes_db):
        return {"erro": f"Cliente ID {cliente_id} não encontrado"}
    
    cliente_removido = clientes_db.pop(cliente_id - 1)
    
    return {
        "mensagem": f"Cliente ID {cliente_id} removido!",
        "cliente_removido": cliente_removido,
        "total_clientes": len(clientes_db)
    }