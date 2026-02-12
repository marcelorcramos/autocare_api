from fastapi import FastAPI
from app.database import clientes_db, veiculos_db

from app.routers import clientes_router, veiculos_router

app = FastAPI(title="AutoCare API", version="1.0.0")

app.include_router(clientes_router)
app.include_router(veiculos_router) 

# Rotas públicas
@app.get("/")
def home():
    return {"mensagem": "Bem-vindo ao AutoCare API!", "status": "online"}

@app.get("/health")
def health():
    return {
        "status": "saudável", 
        "clientes_cadastrados": len(clientes_db),
        "veiculos_cadastrados": len(veiculos_db)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)