from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    """
    Modelo para requisições de chat.
    """
    message: str = Field(..., description="Mensagem do usuário", min_length=1, max_length=2000)
    conversation_id: Optional[str] = Field(None, description="ID da conversa (opcional para nova conversa)")
    user_id: Optional[str] = Field(None, description="ID do usuário (opcional)")
    context: Optional[str] = Field(None, description="Contexto adicional (opcional)")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Como posso lidar com o stress no trabalho?",
                "conversation_id": "conv_123456",
                "user_id": "user_789"
            }
        }

class ChatResponse(BaseModel):
    """
    Modelo para respostas de chat.
    """
    message: str = Field(..., description="Resposta do assistente")
    conversation_id: str = Field(..., description="ID da conversa")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da resposta")
    metadata: Optional[dict] = Field(None, description="Metadados adicionais")
    
    class Config:
        schema_extra = {
            "example": {
                "message": "Para lidar com o stress no trabalho, recomendo algumas estratégias...",
                "conversation_id": "conv_123456",
                "timestamp": "2025-07-28T10:30:00",
                "metadata": {
                    "response_time_ms": 1250,
                    "model_used": "gemini"
                }
            }
        }

class Message(BaseModel):
    """
    Modelo para mensagens individuais em uma conversa.
    """
    id: str = Field(..., description="ID único da mensagem")
    content: str = Field(..., description="Conteúdo da mensagem")
    role: str = Field(..., description="Papel: 'user' ou 'assistant'")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da mensagem")
    conversation_id: str = Field(..., description="ID da conversa")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "msg_abc123",
                "content": "Como posso ser mais empático?",
                "role": "user",
                "timestamp": "2025-07-28T10:29:00",
                "conversation_id": "conv_123456"
            }
        }

class Conversation(BaseModel):
    """
    Modelo para conversas completas.
    """
    id: str = Field(..., description="ID único da conversa")
    user_id: Optional[str] = Field(None, description="ID do usuário")
    title: Optional[str] = Field(None, description="Título da conversa")
    messages: List[Message] = Field(default_factory=list, description="Lista de mensagens")
    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação")
    updated_at: datetime = Field(default_factory=datetime.now, description="Última atualização")
    is_active: bool = Field(True, description="Se a conversa está ativa")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "conv_123456",
                "user_id": "user_789",
                "title": "Discussão sobre ética no trabalho",
                "messages": [],
                "created_at": "2025-07-28T10:00:00",
                "updated_at": "2025-07-28T10:30:00",
                "is_active": True
            }
        }

class EthicalAnalysis(BaseModel):
    """
    Modelo para análise ética de conteúdo.
    """
    is_safe: bool = Field(..., description="Se o conteúdo é seguro")
    risk_level: str = Field(..., description="Nível de risco: low, medium, high")
    detected_issues: List[str] = Field(default_factory=list, description="Problemas detectados")
    sensitive_topics: List[str] = Field(default_factory=list, description="Tópicos sensíveis identificados")
    recommendations: List[str] = Field(default_factory=list, description="Recomendações para melhoria")
    confidence_score: Optional[float] = Field(None, description="Pontuação de confiança da análise (0-1)")
    
    class Config:
        schema_extra = {
            "example": {
                "is_safe": True,
                "risk_level": "low",
                "detected_issues": [],
                "sensitive_topics": ["mental_health"],
                "recommendations": ["Include professional help resources"],
                "confidence_score": 0.95
            }
        }

class HealthCheckResponse(BaseModel):
    """
    Modelo para resposta de verificação de saúde da API.
    """
    status: str = Field(..., description="Status da API")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp da verificação")
    version: str = Field("1.0.0", description="Versão da API")
    services: Optional[dict] = Field(None, description="Status dos serviços")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-07-28T10:30:00",
                "version": "1.0.0",
                "services": {
                    "llm_service": "operational",
                    "rag_service": "operational",
                    "guardrails": "operational"
                }
            }
        }
