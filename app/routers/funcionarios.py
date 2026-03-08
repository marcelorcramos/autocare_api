from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.db_models import Funcionario as FuncionarioDB
from app.models import Funcionario  # Pydantic (validação de entrada)
from typing import Optional
import re

# Criar router específico para funcionarios
router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])

@router.post("/")
def criar_funcionario(funcionario: Funcionario, db: Session = Depends(get_db)):
    """Criar novo Funcionário"""
    existente = db.query(FuncionarioDB).filter(FuncionarioDB.nif == funcionario.nif).first()
    if existente:
        raise HTTPException(status_code=400, detail="Já existe funcionário com este NIF!")

    novo = FuncionarioDB(
        nome=funcionario.nome,
        telefone=funcionario.telefone,
        nif=funcionario.nif,
        morada=funcionario.morada,
        nivel=funcionario.nivel,
        salario=funcionario.salario,
        area=funcionario.area,
        data_nascimento=funcionario.data_nascimento
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "mensagem": "Funcionário criado com sucesso!",
        "funcionario": {
            "id": novo.id,
            "nome": novo.nome,
            "telefone": novo.telefone,
            "nif": novo.nif,
            "morada": novo.morada,
            "nivel": novo.nivel,
            "salario": novo.salario,
            "area": novo.area,
            "data_nascimento": str(novo.data_nascimento)
        },
        "total_funcionarios": db.query(FuncionarioDB).count()
    }

@router.get("/")
def listar_funcionarios(db: Session = Depends(get_db)):
    """Listar todos os Funcionários"""
    funcionarios = db.query(FuncionarioDB).all()
    return {
        "total": len(funcionarios),
        "funcionarios": [
            {
                "id": f.id,
                "nome": f.nome,
                "telefone": f.telefone,
                "nif": f.nif,
                "morada": f.morada,
                "nivel": f.nivel,
                "salario": f.salario,
                "area": f.area,
                "data_nascimento": str(f.data_nascimento)
            }
            for f in funcionarios
        ]
    }

@router.get("/busca/")
def buscar_funcionarios(
    nome: Optional[str] = None,
    nif: Optional[str] = None,
    area: Optional[str] = None,
    nivel: Optional[str] = None,
    ordenar_por: str = "id",
    ordem: str = "asc",
    db: Session = Depends(get_db)
):
    """Busca avançada por funcionários"""
    query = db.query(FuncionarioDB)

    if nome:
        query = query.filter(FuncionarioDB.nome.ilike(f"%{nome}%"))
    if nif:
        nif_limpo = re.sub(r'\D', '', nif)
        query = query.filter(FuncionarioDB.nif.contains(nif_limpo))
    if area:
        query = query.filter(FuncionarioDB.area.ilike(f"%{area}%"))
    if nivel:
        query = query.filter(FuncionarioDB.nivel.ilike(f"%{nivel}%"))

    coluna = getattr(FuncionarioDB, ordenar_por, FuncionarioDB.id)
    if ordem.lower() == "desc":
        query = query.order_by(coluna.desc())
    else:
        query = query.order_by(coluna.asc())

    resultados = query.all()

    return {
        "total": len(resultados),
        "filtros": {"nome": nome, "nif": nif, "area": area, "nivel": nivel},
        "ordenacao": {"por": ordenar_por, "ordem": ordem},
        "funcionarios": [
            {
                "id": f.id,
                "nome": f.nome,
                "telefone": f.telefone,
                "nif": f.nif,
                "morada": f.morada,
                "nivel": f.nivel,
                "salario": f.salario,
                "area": f.area,
                "data_nascimento": str(f.data_nascimento)
            }
            for f in resultados
        ]
    }

@router.get("/{funcionario_id}")
def buscar_funcionario(funcionario_id: int, db: Session = Depends(get_db)):
    """Buscar funcionario pelo ID"""
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == funcionario_id).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail=f"Funcionário ID {funcionario_id} não encontrado!")

    return {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "telefone": funcionario.telefone,
        "nif": funcionario.nif,
        "morada": funcionario.morada,
        "nivel": funcionario.nivel,
        "salario": funcionario.salario,
        "area": funcionario.area,
        "data_nascimento": str(funcionario.data_nascimento)
    }