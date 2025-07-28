from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from app.api import chat
except ImportError:
    from api import chat

app = FastAPI(
    title="Ethicompanion API",
    description="API para o assistente ético Ethicompanion",
    version="1.0.0"
)

# Configuração CORS para permitir requisições do frontend Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Ethicompanion API está funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
