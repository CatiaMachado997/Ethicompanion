from fastapi import APIRouter, HTTPException
try:
    from app.models.chat_models import ChatRequest, ChatResponse
    from app.services.llm_service import LLMService
    from app.services.rag_service import RAGService
    from app.services.ethical_guardrails import EthicalGuardrails
except ImportError:
    from models.chat_models import ChatRequest, ChatResponse
    from services.llm_service import LLMService
    from services.rag_service import RAGService
    from services.ethical_guardrails import EthicalGuardrails

router = APIRouter()

# Inicializar serviços
llm_service = LLMService()
rag_service = RAGService()
ethical_guardrails = EthicalGuardrails()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal para interação com o chatbot ético.
    """
    try:
        # 1. Verificar guardrails éticos na mensagem de entrada
        is_safe_input = await ethical_guardrails.check_input(request.message)
        if not is_safe_input:
            return ChatResponse(
                message="Desculpe, não posso responder a essa pergunta. Vamos focar em tópicos construtivos?",
                conversation_id=request.conversation_id
            )
        
        # 2. Obter contexto relevante através do RAG
        context = await rag_service.get_relevant_context(request.message)
        
        # 3. Gerar resposta com o LLM
        response = await llm_service.generate_response(
            user_message=request.message,
            context=context,
            conversation_id=request.conversation_id
        )
        
        # 4. Verificar guardrails éticos na resposta
        is_safe_output = await ethical_guardrails.check_output(response)
        if not is_safe_output:
            response = "Peço desculpa, mas preciso reformular a resposta. Como posso ajudá-lo de forma mais construtiva?"
        
        return ChatResponse(
            message=response,
            conversation_id=request.conversation_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    """
    Obter histórico de conversa.
    """
    # TODO: Implementar lógica de recuperação do histórico
    return {"conversation_id": conversation_id, "messages": []}

@router.delete("/chat/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """
    Deletar uma conversa.
    """
    # TODO: Implementar lógica de deleção
    return {"message": "Conversa deletada com sucesso"}
