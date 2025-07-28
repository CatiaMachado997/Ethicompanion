#!/usr/bin/env python3
"""
Simple FastAPI server for EthicCompanion - Development Version
This version works without all the dependencies for initial testing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Simple models for development
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    conversation_id: str
    timestamp: datetime

# Create FastAPI app
app = FastAPI(
    title="Ethicompanion API",
    description="API para o assistente ético Ethicompanion",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Ethicompanion API está funcionando!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal para interação com o chatbot ético.
    Versão de desenvolvimento com resposta simples.
    """
    # Simple response for development
    response_message = f"""
    Obrigado pela sua pergunta: "{request.message}"
    
    Como assistente ético, encorajo-o a:
    
    1. **Refletir** sobre os aspectos éticos da situação
    2. **Considerar** o impacto das suas ações nos outros
    3. **Buscar** perspectivas diversas antes de tomar decisões
    4. **Praticar** a empatia e compreensão
    
    Esta é uma resposta de desenvolvimento. Para funcionalidades completas, 
    configure as chaves de API dos modelos de linguagem.
    
    Como posso ajudá-lo a explorar esta questão de forma mais profunda?
    """
    
    conversation_id = request.conversation_id or f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    return ChatResponse(
        message=response_message.strip(),
        conversation_id=conversation_id,
        timestamp=datetime.now()
    )

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando EthicCompanion API...")
    print("📍 API disponível em: http://localhost:8000")
    print("📚 Documentação em: http://localhost:8000/docs")
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=True)
