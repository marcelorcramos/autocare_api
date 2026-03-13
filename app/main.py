from pathlib import Path

from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app.db_models import Base, Cliente, Funcionario, Veiculo

from app.routers import clientes_router, veiculos_router, funcionarios_router

# Cria todas as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoCare API", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(clientes_router)
app.include_router(veiculos_router) 
app.include_router(funcionarios_router)

# Rotas públicas
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo ao AutoCare API!", "status": "online"}

@app.get("/health")
def health(db: Session = Depends(get_db)):
    return {
        "status": "saudável", 
        "clientes_cadastrados": db.query(Cliente).count(),
        "veiculos_cadastrados": db.query(Veiculo).count(),
        "funcionarios_cadastrados": db.query(Funcionario).count()
    }


@app.get("/frontend", include_in_schema=False)
def frontend_page():
    return FileResponse(STATIC_DIR / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
