from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from app.api import chat
    from app.api import chat_enhanced  # Import the enhanced endpoints
except ImportError:
    from api import chat
    try:
        from api import chat_enhanced
    except ImportError:
        chat_enhanced = None

app = FastAPI(
    title="Ethicompanion API",
    description="API para o assistente ético Ethicompanion - Enhanced with multi-LLM support",
    version="2.0.0"
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

# Include enhanced endpoints if available
if chat_enhanced:
    app.include_router(chat_enhanced.router, prefix="/api/v2", tags=["enhanced-chat"])

@app.get("/")
async def root():
    return {
        "message": "Ethicompanion API está funcionando!",
        "version": "2.0.0",
        "features": {
            "multi_llm_support": True,
            "enhanced_validation": True,
            "ethical_guardrails": True,
            "rag_pipeline": True
        },
        "endpoints": {
            "legacy_chat": "/api/v1/chat",
            "enhanced_chat": "/api/v2/ask_ethical" if chat_enhanced else "Not available",
            "health": "/api/v2/health" if chat_enhanced else "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
