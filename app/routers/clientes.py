from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import Cliente as ClienteDB
from app.models import Cliente  # Pydantic (validação de entrada)
from typing import Optional
import re

# Criar router específico para clientes
router = APIRouter(prefix="/clientes", tags=["Clientes"]) 

@router.post("/")
def criar_cliente(cliente: Cliente, db: Session = Depends(get_db)):
    """Criar novo Cliente"""
    # Verifica se já existe cliente com mesmo NIF ou email
    existente = db.query(ClienteDB).filter(
        (ClienteDB.nif == cliente.nif) | (ClienteDB.email == cliente.email)
    ).first()
    if existente:
        raise HTTPException(status_code=400, detail="Já existe cliente com este NIF ou email!")

    novo_cliente = ClienteDB(
        nome=cliente.nome,
        email=cliente.email,
        telefone=cliente.telefone,
        nif=cliente.nif,
        data_nascimento=cliente.data_nascimento
    )
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)

    return {
        "mensagem": "Cliente criado com sucesso!",
        "cliente": {
            "id": novo_cliente.id,
            "nome": novo_cliente.nome,
            "email": novo_cliente.email,
            "telefone": novo_cliente.telefone,
            "nif": novo_cliente.nif,
            "data_nascimento": str(novo_cliente.data_nascimento)
        }
    }

@router.get("/")
def listar_clientes(db: Session = Depends(get_db)):
    """Listar todos os Clientes"""
    clientes = db.query(ClienteDB).all()
    return {
        "total": len(clientes),
        "clientes": [
            {
                "id": c.id,
                "nome": c.nome,
                "email": c.email,
                "telefone": c.telefone,
                "nif": c.nif,
                "data_nascimento": str(c.data_nascimento)
            }
            for c in clientes
        ]
    }

@router.get("/busca/")
def buscar_clientes(
    nome: Optional[str] = None,
    email: Optional[str] = None,
    nif: Optional[str] = None,
    ordenar_por: str = "id",
    ordem: str = "asc",
    db: Session = Depends(get_db)
):
    """Busca avançada de clientes"""
    query = db.query(ClienteDB)

    if nome:
        query = query.filter(ClienteDB.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(ClienteDB.email.ilike(f"%{email}%"))
    if nif:
        nif_limpo = re.sub(r'\D', '', nif)
        query = query.filter(ClienteDB.nif.contains(nif_limpo))

    coluna = getattr(ClienteDB, ordenar_por, ClienteDB.id)
    if ordem.lower() == "desc":
        query = query.order_by(coluna.desc())
    else:
        query = query.order_by(coluna.asc())

    resultados = query.all()

    return {
        "total": len(resultados),
        "filtros": {"nome": nome, "email": email, "nif": nif},
        "ordenacao": {"por": ordenar_por, "ordem": ordem},
        "clientes": [
            {
                "id": c.id,
                "nome": c.nome,
                "email": c.email,
                "telefone": c.telefone,
                "nif": c.nif,
                "data_nascimento": str(c.data_nascimento)
            }
            for c in resultados
        ]
    }

@router.get("/{cliente_id}")
def buscar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Buscar cliente pelo ID"""
    cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado!")

    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "email": cliente.email,
        "telefone": cliente.telefone,
        "nif": cliente.nif,
        "data_nascimento": str(cliente.data_nascimento)
    }

@router.put("/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente_atualizado: Cliente, db: Session = Depends(get_db)):
    """Atualizar cliente existente"""
    cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado!")

    cliente.nome = cliente_atualizado.nome
    cliente.email = cliente_atualizado.email
    cliente.telefone = cliente_atualizado.telefone
    cliente.nif = cliente_atualizado.nif
    cliente.data_nascimento = cliente_atualizado.data_nascimento
    db.commit()
    db.refresh(cliente)

    return {
        "mensagem": f"Cliente ID {cliente_id} atualizado!",
        "cliente": {
            "id": cliente.id,
            "nome": cliente.nome,
            "email": cliente.email,
            "telefone": cliente.telefone,
            "nif": cliente.nif,
            "data_nascimento": str(cliente.data_nascimento)
        }
    }

@router.delete("/{cliente_id}")
def deletar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Remover cliente"""
    cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail=f"Cliente ID {cliente_id} não encontrado!")

    nome_removido = cliente.nome
    db.delete(cliente)
    db.commit()
    total = db.query(ClienteDB).count()

    return {
        "mensagem": f"Cliente ID {cliente_id} removido!",
        "cliente_removido": nome_removido,
        "total_clientes": total
    }


