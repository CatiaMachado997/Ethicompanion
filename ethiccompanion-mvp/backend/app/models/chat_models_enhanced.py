from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import base64
from datetime import datetime
import uuid

class StressLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"

class LLMProvider(str, Enum):
    GEMINI = "gemini"
    CLAUDE = "claude"
    GEMMA_3N = "gemma_3n"
    AUTO = "auto"

class ErrorCode(str, Enum):
    VALIDATION_ERROR = "validation_error"
    LLM_UNAVAILABLE = "llm_unavailable"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    CONTENT_FILTERED = "content_filtered"
    INTERNAL_ERROR = "internal_error"

class EthicalRequest(BaseModel):
    """Enhanced request model for ethical guidance"""
    user_query: str = Field(
        ..., 
        min_length=1, 
        max_length=2000, 
        description="User's ethical question or concern"
    )
    conversation_id: Optional[str] = Field(
        None, 
        description="Conversation ID for context continuity"
    )
    preferred_llm: LLMProvider = Field(
        LLMProvider.AUTO, 
        description="Preferred LLM provider"
    )
    image_data: Optional[str] = Field(
        None, 
        description="Base64 encoded image data"
    )
    context: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        description="Additional context"
    )
    user_stress_level: StressLevel = Field(
        StressLevel.MODERATE, 
        description="Current stress level"
    )
    max_tokens: Optional[int] = Field(
        1000, 
        ge=100, 
        le=4000, 
        description="Maximum tokens for response"
    )
    temperature: Optional[float] = Field(
        0.7, 
        ge=0.0, 
        le=1.0, 
        description="LLM temperature setting"
    )
    
    @validator('image_data')
    def validate_image_data(cls, v):
        if v:
            try:
                base64.b64decode(v)
            except Exception:
                raise ValueError('Invalid base64 image data')
        return v
    
    @validator('conversation_id')
    def validate_conversation_id(cls, v):
        if v and not v.startswith('conv_'):
            return f"conv_{v}"
        return v or f"conv_{uuid.uuid4().hex[:8]}"

class EthicalSource(BaseModel):
    """Source citation for ethical guidance"""
    title: str = Field(..., description="Source document title")
    content_snippet: str = Field(..., description="Relevant content excerpt")
    relevance_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Relevance score"
    )
    document_type: str = Field("knowledge_base", description="Type of source")

class LLMMetadata(BaseModel):
    """Metadata about LLM processing"""
    provider_used: LLMProvider = Field(..., description="LLM provider used")
    model_name: str = Field(..., description="Specific model used")
    processing_time_ms: int = Field(..., description="Processing time in milliseconds")
    token_count: int = Field(..., description="Tokens used")
    confidence_score: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Confidence in response"
    )
    fallback_used: bool = Field(False, description="Whether fallback was used")

class EthicalResponse(BaseModel):
    """Enhanced response model for ethical guidance"""
    ethical_advice: str = Field(..., description="Main ethical guidance")
    reasoning: str = Field(..., description="Explanation of the advice")
    sources: List[EthicalSource] = Field(
        default_factory=list, 
        description="Supporting sources"
    )
    suggested_actions: List[str] = Field(
        default_factory=list, 
        description="Concrete action suggestions"
    )
    peace_techniques: List[str] = Field(
        default_factory=list, 
        description="Mindfulness techniques"
    )
    conversation_id: str = Field(..., description="Conversation identifier")
    response_id: str = Field(
        default_factory=lambda: f"resp_{uuid.uuid4().hex[:8]}", 
        description="Unique response ID"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, 
        description="Response timestamp"
    )
    llm_metadata: LLMMetadata = Field(..., description="LLM processing metadata")
    content_safety: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Content safety assessment"
    )

class ErrorResponse(BaseModel):
    """Standardized error response"""
    error_code: ErrorCode = Field(..., description="Error classification")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(
        None, 
        description="Additional error details"
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, 
        description="Error timestamp"
    )
    conversation_id: Optional[str] = Field(
        None, 
        description="Associated conversation ID"
    )
    suggestions: List[str] = Field(
        default_factory=list, 
        description="Suggested solutions"
    )

class HealthCheckResponse(BaseModel):
    """Enhanced health check response model"""
    status: str = Field("healthy", description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field("1.0.0", description="API version")
    services: Dict[str, str] = Field(
        default_factory=dict, 
        description="Service statuses"
    )
    llm_providers: Dict[str, bool] = Field(
        default_factory=dict, 
        description="LLM provider availability"
    )

# Legacy models for backward compatibility
class ChatRequest(BaseModel):
    """Legacy model for backward compatibility"""
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
    """Legacy model for backward compatibility"""
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
