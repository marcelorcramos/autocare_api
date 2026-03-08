"""Configuração do banco de dados SQLite com SQLAlchemy"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL do banco de dados SQLite (arquivo local)
DATABASE_URL = "sqlite:///./autocare.db"

# Engine — conexão com o banco
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necessário para SQLite
    echo=True  # mostra os comandos SQL no terminal (útil para aprender)
)

# SessionLocal — fábrica de sessões (cada request usa uma sessão)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base — classe base para todos os modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependency do FastAPI: cria uma sessão do banco por request.
    Uso nos routers:
        from app.database import get_db
        def meu_endpoint(db: Session = Depends(get_db)):
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Compatibilidade temporária ──────────────────────────────────────
# Mantém as listas em memória para os endpoints atuais continuarem
# funcionando enquanto não são migrados para usar o SQLAlchemy.
clientes_db: list = []
veiculos_db: list = []
funcionarios_db: list = []