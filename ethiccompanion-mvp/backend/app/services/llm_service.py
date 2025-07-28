import os
from typing import Optional
import google.generativeai as genai
from anthropic import Anthropic

class LLMService:
    """
    Serviço para integração com LLMs (Gemini e Claude).
    """
    
    def __init__(self):
        # Configurar Gemini
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-pro')
        
        # Configurar Claude
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
    
    async def generate_response(
        self, 
        user_message: str, 
        context: str = "", 
        conversation_id: Optional[str] = None,
        preferred_model: str = "gemini"
    ) -> str:
        """
        Gerar resposta usando o LLM especificado.
        """
        
        # Prompt do sistema para comportamento ético
        system_prompt = """
        Você é o Ethicompanion, um assistente de IA especializado em apoio ético e bem-estar digital.
        Seus objetivos são:
        1. Promover reflexão ética e crescimento pessoal
        2. Ajudar com sobrecarga de informação
        3. Ensinar técnicas de paz interior e mindfulness
        4. Sempre responder de forma construtiva, empática e respeitosa
        5. Não fornecer conselhos médicos, legais ou financeiros específicos
        
        Use o contexto fornecido para enriquecer suas respostas quando relevante.
        """
        
        # Construir prompt completo
        full_prompt = f"{system_prompt}\n\nContexto relevante:\n{context}\n\nPergunta do usuário: {user_message}\n\nResposta:"
        
        try:
            if preferred_model == "gemini" and hasattr(self, 'gemini_model'):
                response = self.gemini_model.generate_content(full_prompt)
                return response.text
            
            elif preferred_model == "claude" and hasattr(self, 'anthropic_client'):
                response = self.anthropic_client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Contexto: {context}\n\nPergunta: {user_message}"
                        }
                    ]
                )
                return response.content[0].text
            
            else:
                # Fallback para resposta padrão se APIs não estiverem configuradas
                return self._generate_fallback_response(user_message)
                
        except Exception as e:
            print(f"Erro ao gerar resposta: {e}")
            return self._generate_fallback_response(user_message)
    
    def _generate_fallback_response(self, user_message: str) -> str:
        """
        Resposta de fallback quando APIs não estão disponíveis.
        """
        return f"""
        Obrigado pela sua pergunta sobre "{user_message}". 
        
        Como assistente ético, encorajo-o a:
        
        1. **Refletir** sobre os aspectos éticos da situação
        2. **Considerar** o impacto das suas ações nos outros
        3. **Buscar** perspectivas diversas antes de tomar decisões
        4. **Praticar** a empatia e compreensão
        
        Para uma experiência mais personalizada, por favor configure as chaves de API dos modelos de linguagem.
        
        Como posso ajudá-lo a explorar esta questão de forma mais profunda?
        """
