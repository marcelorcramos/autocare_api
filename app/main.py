from fastapi import FastAPI
from app.database import clientes_db  # só para o health check
from app.routers import clientes, veiculos

# Criar app FastAPI
app = FastAPI(title="AutoCare API", version="1.0.0")

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

# Incluir os routers
app.include_router(clientes.router)
app.include_router(veiculos.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
