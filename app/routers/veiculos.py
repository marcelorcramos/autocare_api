from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import Veiculo as VeiculoDB, Cliente as ClienteDB
from app.models import Veiculo  # Pydantic (validação de entrada)
from typing import Optional
import re

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

@router.post("/")
def criar_veiculo(veiculo: Veiculo, db: Session = Depends(get_db)):
    """Criar novo veículo"""
    # Verifica se o cliente existe
    cliente = db.query(ClienteDB).filter(ClienteDB.id == veiculo.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {veiculo.cliente_id} não encontrado")

    # Verifica se placa já existe
    existente = db.query(VeiculoDB).filter(VeiculoDB.placa == veiculo.placa).first()
    if existente:
        raise HTTPException(status_code=400, detail=f"Já existe veículo com a placa {veiculo.placa}")

    novo = VeiculoDB(
        placa=veiculo.placa,
        marca=veiculo.marca,
        modelo=veiculo.modelo,
        ano=veiculo.ano,
        cor=veiculo.cor,
        cliente_id=veiculo.cliente_id
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "mensagem": "Veículo criado com sucesso!",
        "veiculo": {
            "id": novo.id,
            "placa": novo.placa,
            "marca": novo.marca,
            "modelo": novo.modelo,
            "ano": novo.ano,
            "cor": novo.cor,
            "cliente_id": novo.cliente_id
        }
    }

@router.get("/")
def listar_veiculos(db: Session = Depends(get_db)):
    """Listar todos os veículos"""
    veiculos = db.query(VeiculoDB).all()
    return {
        "total": len(veiculos),
        "veiculos": [
            {
                "id": v.id,
                "placa": v.placa,
                "marca": v.marca,
                "modelo": v.modelo,
                "ano": v.ano,
                "cor": v.cor,
                "cliente_id": v.cliente_id
            }
            for v in veiculos
        ]
    }

@router.get("/busca/")
def buscar_veiculos(
    placa: Optional[str] = None,
    marca: Optional[str] = None,
    modelo: Optional[str] = None,
    ordenar_por: str = "id",
    ordem: str = "asc",
    db: Session = Depends(get_db)
):
    """Busca avançada de veículos"""
    query = db.query(VeiculoDB)

    if placa:
        query = query.filter(VeiculoDB.placa.ilike(f"%{placa}%"))
    if marca:
        query = query.filter(VeiculoDB.marca.ilike(f"%{marca}%"))
    if modelo:
        query = query.filter(VeiculoDB.modelo.ilike(f"%{modelo}%"))

    coluna = getattr(VeiculoDB, ordenar_por, VeiculoDB.id)
    if ordem.lower() == "desc":
        query = query.order_by(coluna.desc())
    else:
        query = query.order_by(coluna.asc())

    resultados = query.all()

    return {
        "total": len(resultados),
        "filtros": {"placa": placa, "marca": marca, "modelo": modelo},
        "ordenacao": {"por": ordenar_por, "ordem": ordem},
        "veiculos": [
            {
                "id": v.id,
                "placa": v.placa,
                "marca": v.marca,
                "modelo": v.modelo,
                "ano": v.ano,
                "cor": v.cor,
                "cliente_id": v.cliente_id
            }
            for v in resultados
        ]
    }

@router.get("/{veiculo_id}")
def buscar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """Buscar veículo por ID"""
    veiculo = db.query(VeiculoDB).filter(VeiculoDB.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail=f"Veículo ID {veiculo_id} não encontrado")

    return {
        "id": veiculo.id,
        "placa": veiculo.placa,
        "marca": veiculo.marca,
        "modelo": veiculo.modelo,
        "ano": veiculo.ano,
        "cor": veiculo.cor,
        "cliente_id": veiculo.cliente_id
    }

@router.delete("/{veiculo_id}")
def deletar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    """Remover veículo existente"""
    veiculo = db.query(VeiculoDB).filter(VeiculoDB.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail=f"Veículo ID {veiculo_id} não encontrado")

    placa_removida = veiculo.placa
    db.delete(veiculo)
    db.commit()
    total = db.query(VeiculoDB).count()

    return {
        "mensagem": f"Veículo ID {veiculo_id} removido com sucesso!",
        "veiculo_removido": placa_removida,
        "total_veiculos": total
    }

@router.put("/{veiculo_id}")
def atualizar_veiculo(veiculo_id: int, veiculo_atualizado: Veiculo, db: Session = Depends(get_db)):
    """Atualizar Informações do veículo"""
    veiculo = db.query(VeiculoDB).filter(VeiculoDB.id == veiculo_id).first()
    if not veiculo:
        raise HTTPException(status_code=404, detail=f"Veículo ID {veiculo_id} não encontrado!")

    # Verifica se o novo cliente_id existe
    cliente = db.query(ClienteDB).filter(ClienteDB.id == veiculo_atualizado.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {veiculo_atualizado.cliente_id} não encontrado")

    veiculo.placa = veiculo_atualizado.placa
    veiculo.marca = veiculo_atualizado.marca
    veiculo.modelo = veiculo_atualizado.modelo
    veiculo.ano = veiculo_atualizado.ano
    veiculo.cor = veiculo_atualizado.cor
    veiculo.cliente_id = veiculo_atualizado.cliente_id
    db.commit()
    db.refresh(veiculo)

    return {
        "mensagem": f"Veículo ID {veiculo_id} atualizado!",
        "veiculo": {
            "id": veiculo.id,
            "placa": veiculo.placa,
            "marca": veiculo.marca,
            "modelo": veiculo.modelo,
            "ano": veiculo.ano,
            "cor": veiculo.cor,
            "cliente_id": veiculo.cliente_id
        }
    }

@router.get("/clientes/{cliente_id}/veiculos")
def veiculos_do_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Listar todos os veículos de um cliente"""
    cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado!")

    veiculos = db.query(VeiculoDB).filter(VeiculoDB.cliente_id == cliente_id).all()

    return {
        "cliente_id": cliente_id,
        "cliente_nome": cliente.nome,
        "total_veiculos": len(veiculos),
        "veiculos": [
            {
                "id": v.id,
                "placa": v.placa,
                "marca": v.marca,
                "modelo": v.modelo,
                "ano": v.ano,
                "cor": v.cor,
                "cliente_id": v.cliente_id
            }
            for v in veiculos
        ]
    }


