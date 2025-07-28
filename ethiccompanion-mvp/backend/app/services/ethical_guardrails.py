import re
from typing import List, Dict, Optional
import asyncio

class EthicalGuardrails:
    """
    Sistema de guardrails éticos para verificar inputs e outputs.
    Implementação inicial com regras baseadas em palavras-chave.
    """
    
    def __init__(self):
        # Palavras/frases que indicam conteúdo potencialmente problemático
        self.harmful_keywords = [
            # Violência
            "violence", "violência", "matar", "kill", "hurt", "ferir",
            "weapon", "arma", "bomb", "bomba",
            
            # Ódio e discriminação
            "hate", "ódio", "racism", "racismo", "sexism", "sexismo",
            "discrimination", "discriminação",
            
            # Autolesão
            "suicide", "suicídio", "self-harm", "autolesão",
            "cut myself", "me cortar",
            
            # Conteúdo sexual inadequado
            "sexual explicit", "sexo explícito", "pornography", "pornografia",
            
            # Atividades ilegais
            "drugs", "drogas", "illegal", "ilegal", "crime", "criminal"
        ]
        
        # Palavras que indicam conteúdo positivo/construtivo
        self.positive_keywords = [
            "help", "ajuda", "support", "apoio", "growth", "crescimento",
            "learning", "aprendizagem", "ethics", "ética", "peace", "paz",
            "mindfulness", "meditation", "meditação", "wellness", "bem-estar",
            "empathy", "empatia", "compassion", "compaixão"
        ]
        
        # Tópicos que requerem aviso (não bloqueio, mas cuidado)
        self.sensitive_topics = [
            "depression", "depressão", "anxiety", "ansiedade",
            "mental health", "saúde mental", "therapy", "terapia",
            "relationship", "relacionamento", "family", "família"
        ]
    
    async def check_input(self, text: str) -> bool:
        """
        Verificar se o input do usuário é seguro e apropriado.
        
        Returns:
            True se o input for seguro, False caso contrário
        """
        text_lower = text.lower()
        
        # Verificar palavras-chave prejudiciais
        harmful_count = sum(1 for keyword in self.harmful_keywords if keyword in text_lower)
        
        # Se encontrar muitas palavras prejudiciais, bloquear
        if harmful_count >= 2:
            return False
        
        # Verificar padrões específicos
        if self._check_harmful_patterns(text_lower):
            return False
        
        return True
    
    async def check_output(self, text: str) -> bool:
        """
        Verificar se a resposta gerada é segura e apropriada.
        
        Returns:
            True se a resposta for segura, False caso contrário
        """
        text_lower = text.lower()
        
        # Verificações mais rigorosas para outputs
        harmful_count = sum(1 for keyword in self.harmful_keywords if keyword in text_lower)
        
        if harmful_count >= 1:  # Mais restritivo para outputs
            return False
        
        # Verificar se contém conselhos médicos específicos não apropriados
        if self._contains_inappropriate_advice(text_lower):
            return False
        
        return True
    
    def _check_harmful_patterns(self, text: str) -> bool:
        """
        Verificar padrões específicos que podem ser prejudiciais.
        """
        harmful_patterns = [
            r"how to (kill|hurt|harm)",
            r"como (matar|ferir|machucar)",
            r"i want to (die|kill myself)",
            r"quero (morrer|me matar)",
            r"hate (all|everyone)",
            r"odeio (todos|todo mundo)"
        ]
        
        for pattern in harmful_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def _contains_inappropriate_advice(self, text: str) -> bool:
        """
        Verificar se o texto contém conselhos médicos, legais ou financeiros específicos.
        """
        inappropriate_advice_patterns = [
            r"you should take (medication|pills|drugs)",
            r"deve tomar (medicamento|remédio|droga)",
            r"diagnose you with",
            r"diagnostico você com",
            r"legal advice.*sue",
            r"conselho legal.*processar",
            r"invest.*money.*guaranteed",
            r"invista.*dinheiro.*garantido"
        ]
        
        for pattern in inappropriate_advice_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    def analyze_content_safety(self, text: str) -> Dict[str, any]:
        """
        Análise detalhada da segurança do conteúdo.
        
        Returns:
            Dicionário com análise detalhada
        """
        text_lower = text.lower()
        
        analysis = {
            "is_safe": True,
            "risk_level": "low",  # low, medium, high
            "detected_issues": [],
            "sensitive_topics": [],
            "recommendations": []
        }
        
        # Contar palavras prejudiciais
        harmful_found = [kw for kw in self.harmful_keywords if kw in text_lower]
        if harmful_found:
            analysis["detected_issues"].extend(harmful_found)
            analysis["risk_level"] = "high" if len(harmful_found) >= 2 else "medium"
            analysis["is_safe"] = False
        
        # Identificar tópicos sensíveis
        sensitive_found = [topic for topic in self.sensitive_topics if topic in text_lower]
        if sensitive_found:
            analysis["sensitive_topics"] = sensitive_found
            if analysis["risk_level"] == "low":
                analysis["risk_level"] = "medium"
        
        # Gerar recomendações
        if not analysis["is_safe"]:
            analysis["recommendations"].append("Reformular resposta com foco construtivo")
            analysis["recommendations"].append("Incluir recursos de apoio apropriados")
        elif analysis["sensitive_topics"]:
            analysis["recommendations"].append("Incluir aviso sobre busca por ajuda profissional")
            analysis["recommendations"].append("Fornecer recursos de apoio")
        
        return analysis
    
    def get_ethical_prompt_enhancement(self, topic: str) -> str:
        """
        Obter melhorias éticas para o prompt baseado no tópico.
        """
        enhancements = {
            "mental_health": """
            IMPORTANTE: Para questões de saúde mental, sempre:
            - Demonstre empatia e compreensão
            - Encoraje busca por ajuda profissional quando apropriado
            - Forneça recursos de apoio (linhas de ajuda, etc.)
            - Evite diagnósticos ou conselhos médicos específicos
            """,
            
            "relationships": """
            IMPORTANTE: Para questões de relacionamento:
            - Promova comunicação saudável e respeitosa
            - Encoraje resolução pacífica de conflitos
            - Respeite autonomia e limites pessoais
            - Sugira busca por mediação profissional se necessário
            """,
            
            "general": """
            IMPORTANTE: Mantenha sempre:
            - Foco em crescimento pessoal e bem-estar
            - Respeito pela dignidade humana
            - Promoção de valores éticos positivos
            - Encorajamento de reflexão crítica construtiva
            """
        }
        
        return enhancements.get(topic, enhancements["general"])
