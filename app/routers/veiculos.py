from fastapi import APIRouter 
from app.models import Veiculo
from app.database import veiculos_db, clientes_db
from typing import Optional
import re

# MUDE de FastAPI() para APIRouter()
router = APIRouter(prefix="/veiculos", tags=["Veículos"])

@router.post("/")
def criar_veiculo(veiculo: Veiculo):
    """Criar novo veículo"""
    # Verifica se o cliente existe
    cliente_existe = False
    for c in clientes_db:
        if c["id"] == veiculo.cliente_id:
            cliente_existe = True
            break
    
    if not cliente_existe:
        return {"erro": f"Cliente ID {veiculo.cliente_id} não encontrado"}
    
    veiculo_dict = veiculo.dict()
    veiculo_dict["id"] = len(veiculos_db) + 1
    veiculos_db.append(veiculo_dict)
    
    return {
        "mensagem": "Veículo criado com sucesso!",
        "veiculo": veiculo_dict
    }

@router.get("/")
def listar_veiculos():
    """Listar todos os veículos"""
    return {
        "total": len(veiculos_db),
        "veiculos": veiculos_db
    }

@router.get("/veiculos/busca/")
def buscar_veiculos(
    placa: Optional[str] = None,
    marca: Optional[str] = None,
    modelo: Optional[str] = None,
    ordenar_por: str = "id",
    ordem: str = "asc"
):
    """Busca avançada de veículos"""
    resultados = veiculos_db.copy()

    #Filtros
    if placa:
        resultados = [v for v in resultados if placa.lower() in v["placa"].lower()]

    if marca:
        resultados = [v for v in resultados if marca.lower() in v["marca"].lower()]
    
    if modelo:
        resultados = [v for v in resultados if modelo.lower() in v["modelo"].lower()]

    #Ordenação
    reverse = (ordem.lower() == "desc")
    resultados.sort(key=lambda x: x.get(ordenar_por, ""), reverse=reverse)

    return{
        "total": len(resultados),
        "filtros": {"placa": placa, "marca": marca, "modelo": modelo},
        "ordenacao": {"por": ordenar_por, "ordem": ordem},
        "veiculos": resultados
    }

@router.get("/veiculos/{veiculo_id}")
def buscar_veiculo(veiculo_id: int):
    """Buscar veículo por ID"""
    for veiculo in veiculos_db:
        if veiculo["id"] == veiculo_id: 
            return veiculo
        
    return {"erro": f"Veículo ID {veiculo_id} não encontrado"}

@router.delete("/veiculos/{veiculo_id}")
def deletar_veiculo (veiculo_id: int):
    """Remover veículo existente"""
    for indice, veiculo in enumerate(veiculos_db):
        if veiculo["id"] == veiculo_id:
            veiculo_removido = veiculos_db.pop(indice)

            return {
                "mensagem" : f"Veículo ID {veiculo_id} removido com sucesso!",
                "veiculo_removido" : veiculo_removido,
                "total_veiculos": len(veiculos_db)
            }

    return{"erro" : f"Veículo ID {veiculo_id} não encontrado"}

@router.put("/veiculos/{veiculo_id}")
def atualizar_veiculo (veiculo_id : int, veiculo_atualizado: Veiculo):
    """Atualizar Informações do veículo"""
    for indice, veiculo in enumerate(veiculos_db):
        if veiculo["id"] == veiculo_id:
            veiculo_dict = veiculo_atualizado.dict()
            veiculo_dict["id"] = veiculo_id
            veiculos_db[indice] = veiculo_dict

            return {
                "mensagem" : f"Veículo ID {veiculo_id} atualizado!",
                "veiculo" : veiculo_dict
            }

    return{
        "erro" : f"Veículo ID {veiculo_id} não encontrado!"
    }

@router.get("/clientes/{cliente_id}/veiculos")
def veiculos_do_cliente(cliente_id : int):
    """Listar todos os veículos de um cliente"""
    #Verifica se existe o cliente
    cliente_existe = False
    for c in clientes_db:
        if c["id"] == cliente_id:
            cliente_existe = True
            break
    
    if not cliente_existe:
        return {
            "erro" : f"Cliente ID {cliente_id} não encontrado!"
        }
    
    veiculos_cliente = [
        v for v in veiculos_db
        if v ["cliente_id"] == cliente_id
    ]

    return{
        "cliente_id" : cliente_id,
        "total_veiculos" : len(veiculos_cliente),
        "veiculos": veiculos_cliente
    }


