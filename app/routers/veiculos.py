from fastapi import APIRouter
from app.models import Veiculo
from app.database import veiculos_db, clientes_db

# Criar router específico para veículos
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