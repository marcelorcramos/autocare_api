from fastapi import FastAPI
from app.database import clientes_db, veiculos_db, funcionarios_db, engine
from app.db_models import Base  # importa os modelos para criar as tabelas

from app.routers import clientes_router, veiculos_router, funcionarios_router

# Cria todas as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoCare API", version="1.0.0")

app.include_router(clientes_router)
app.include_router(veiculos_router) 
app.include_router(funcionarios_router)

# Rotas públicas
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo ao AutoCare API!", "status": "online"}

@app.get("/health")
def health():
    return {
        "status": "saudável", 
        "clientes_cadastrados": len(clientes_db),
        "veiculos_cadastrados": len(veiculos_db),
        "funcionarios_cadastrados": len(funcionarios_db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)