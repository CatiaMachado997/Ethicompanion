from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
import logging
import time
from typing import Optional
import asyncio

try:
    from ..models.chat_models_enhanced import (
        EthicalRequest,
        EthicalResponse, 
        ErrorResponse,
        ErrorCode,
        LLMProvider,
        LLMMetadata,
        EthicalSource
    )
    from ..services.llm_service_enhanced import LLMOrchestrator
    from ..services.rag_service_enhanced import EthicalRAGService
    from ..services.ethical_guardrails_enhanced import EthicalGuardrailsService
except ImportError:
    # Fallback imports for module resolution issues
    from models.chat_models_enhanced import (
        EthicalRequest,
        EthicalResponse, 
        ErrorResponse,
        ErrorCode,
        LLMProvider,
        LLMMetadata,
        EthicalSource
    )
    from services.llm_service_enhanced import LLMOrchestrator
    from services.rag_service_enhanced import EthicalRAGService
    from services.ethical_guardrails_enhanced import EthicalGuardrailsService

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
llm_orchestrator = LLMOrchestrator()
rag_service = EthicalRAGService()
guardrails_service = EthicalGuardrailsService()

@router.post("/ask_ethical", response_model=EthicalResponse)
async def ask_ethical_guidance(
    request: EthicalRequest,
    background_tasks: BackgroundTasks
) -> EthicalResponse:
    """
    Enhanced ethical guidance endpoint with comprehensive validation,
    multi-LLM support, and proper error handling.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Received ethical guidance request: {request.conversation_id}")
        
        # Step 1: Content moderation and guardrails
        moderation_result = await guardrails_service.moderate_content(request.user_query)
        if not moderation_result.is_safe:
            raise HTTPException(
                status_code=400,
                detail=ErrorResponse(
                    error_code=ErrorCode.CONTENT_FILTERED,
                    message="Content violates ethical guidelines",
                    details={"moderation_flags": moderation_result.flags},
                    conversation_id=request.conversation_id,
                    suggestions=[
                        "Please rephrase your question focusing on information management",
                        "Consider asking about stress reduction techniques",
                        "Try asking about constructive ways to handle difficult situations"
                    ]
                ).dict()
            )
        
        # Step 2: RAG - Retrieve relevant context
        relevant_context = await rag_service.get_relevant_context(
            query=request.user_query,
            k=5  # Retrieve top 5 relevant documents
        )
        
        # Step 3: LLM Processing with automatic provider selection
        llm_response = await llm_orchestrator.get_ethical_guidance(
            query=request.user_query,
            context={
                "relevant_docs": relevant_context,
                "user_stress_level": request.user_stress_level.value,
                "conversation_history": request.context.get("history", []),
                "image_data": request.image_data
            },
            preferred_model=request.preferred_llm.value,
            max_tokens=request.max_tokens,
            temperature=request.temperature
        )
        
        # Step 4: Generate structured sources
        sources = []
        for doc in relevant_context[:3]:  # Top 3 most relevant
            sources.append(EthicalSource(
                title=doc.get("metadata", {}).get("source", "Knowledge Base"),
                content_snippet=doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"],
                relevance_score=doc.get("relevance_score", 0.0),
                document_type="ethical_knowledge"
            ))
        
        # Step 5: Generate peace techniques based on stress level
        peace_techniques = await _generate_peace_techniques(
            stress_level=request.user_stress_level,
            context=request.context
        )
        
        # Step 6: Generate suggested actions
        suggested_actions = await _generate_suggested_actions(
            query=request.user_query,
            advice=llm_response.content
        )
        
        # Step 7: Content safety assessment
        content_safety = {
            "safety_score": moderation_result.confidence,
            "ethical_assessment": "approved",
            "sensitive_topics": moderation_result.flags
        }
        
        # Step 8: Create metadata
        processing_time = int((time.time() - start_time) * 1000)
        metadata = LLMMetadata(
            provider_used=LLMProvider(llm_response.model_used.lower()),
            model_name=llm_response.model_used,
            processing_time_ms=processing_time,
            token_count=llm_response.token_count,
            confidence_score=llm_response.confidence,
            fallback_used=getattr(llm_response, 'fallback_used', False)
        )
        
        # Step 9: Build response
        response = EthicalResponse(
            ethical_advice=llm_response.content,
            reasoning=llm_response.reasoning,
            sources=sources,
            suggested_actions=suggested_actions,
            peace_techniques=peace_techniques,
            conversation_id=request.conversation_id,
            llm_metadata=metadata,
            content_safety=content_safety
        )
        
        # Step 10: Background logging
        background_tasks.add_task(
            _log_interaction,
            request=request,
            response=response,
            processing_time=processing_time
        )
        
        logger.info(f"Successfully processed request {request.conversation_id} in {processing_time}ms")
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error processing ethical guidance request: {str(e)}")
        processing_time = int((time.time() - start_time) * 1000)
        
        error_response = ErrorResponse(
            error_code=ErrorCode.INTERNAL_ERROR,
            message="An unexpected error occurred while processing your request",
            details={"error": str(e), "processing_time_ms": processing_time},
            conversation_id=request.conversation_id,
            suggestions=[
                "Please try again in a moment",
                "Consider simplifying your question",
                "Check your internet connection"
            ]
        )
        
        raise HTTPException(status_code=500, detail=error_response.dict())

async def _generate_peace_techniques(stress_level, context) -> list:
    """Generate personalized peace techniques based on stress level"""
    techniques_map = {
        "low": [
            "Take 3 deep breaths and notice your surroundings",
            "Practice a 2-minute mindfulness exercise",
            "Write down one thing you're grateful for"
        ],
        "moderate": [
            "Try the 4-7-8 breathing technique",
            "Take a 5-minute walk outside",
            "Practice progressive muscle relaxation",
            "Listen to calming music for 10 minutes"
        ],
        "high": [
            "Use the 5-4-3-2-1 grounding technique",
            "Practice box breathing (4-4-4-4 pattern)",
            "Take a longer break from your current activity",
            "Call a trusted friend or counselor"
        ],
        "critical": [
            "Focus on your immediate safety and basic needs",
            "Contact a mental health professional",
            "Use crisis helpline resources",
            "Practice emergency grounding techniques"
        ]
    }
    
    return techniques_map.get(stress_level.value, techniques_map["moderate"])

async def _generate_suggested_actions(query: str, advice: str) -> list:
    """Generate concrete action suggestions based on the query and advice"""
    # This could be enhanced with more sophisticated NLP analysis
    generic_actions = [
        "Start with small, manageable steps",
        "Set aside time for reflection and planning",
        "Consider discussing this with trusted friends or mentors",
        "Document your progress and learnings"
    ]
    
    # Could add query-specific action generation here
    return generic_actions[:3]  # Return top 3 actions

async def _log_interaction(request: EthicalRequest, response: EthicalResponse, processing_time: int):
    """Background task to log interactions for analytics and improvement"""
    log_data = {
        "conversation_id": request.conversation_id,
        "query_length": len(request.user_query),
        "stress_level": request.user_stress_level.value,
        "preferred_llm": request.preferred_llm.value,
        "processing_time_ms": processing_time,
        "sources_count": len(response.sources),
        "llm_provider_used": response.llm_metadata.provider_used.value,
        "confidence_score": response.llm_metadata.confidence_score
    }
    
    logger.info(f"Interaction logged: {log_data}")
    # In production, you might store this in a database or analytics service

@router.get("/health", response_model=dict)
async def health_check():
    """Enhanced health check endpoint"""
    try:
        # Check LLM services
        llm_status = await llm_orchestrator.check_health()
        
        # Check RAG service
        rag_status = await rag_service.check_health()
        
        # Check guardrails service
        guardrails_status = await guardrails_service.check_health()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "1.0.0",
            "services": {
                "llm_orchestrator": "operational" if llm_status else "degraded",
                "rag_service": "operational" if rag_status else "degraded", 
                "guardrails": "operational" if guardrails_status else "degraded"
            },
            "llm_providers": llm_status if isinstance(llm_status, dict) else {}
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "timestamp": time.time(),
            "error": str(e)
        }
