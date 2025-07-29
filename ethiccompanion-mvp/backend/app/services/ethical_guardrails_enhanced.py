import asyncio
import logging
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import os

@dataclass
class ModerationResult:
    is_safe: bool
    flags: List[str]
    confidence: float
    explanation: str

class EthicalGuardrailsService:
    """
    Enhanced content moderation and ethical boundary enforcement service
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.ethical_keywords = self._load_ethical_keywords()
        self.crisis_keywords = self._load_crisis_keywords()
        self.off_topic_patterns = self._load_off_topic_patterns()
        
        # Initialize external moderation APIs if available
        self.perspective_client = self._init_perspective_api()
        self.openai_client = self._init_openai_client()
    
    def _load_ethical_keywords(self) -> Dict[str, List[str]]:
        """Load keywords that indicate on-topic ethical discussions"""
        return {
            "information_management": [
                "information overload", "news fatigue", "digital overwhelm",
                "media consumption", "social media", "news anxiety",
                "fact checking", "misinformation", "filter bubble"
            ],
            "peace_techniques": [
                "mindfulness", "meditation", "breathing", "stress relief",
                "anxiety", "calm", "peace", "relaxation", "grounding",
                "mental health", "wellness", "self care"
            ],
            "ethical_guidance": [
                "ethics", "moral", "values", "principles", "right", "wrong",
                "responsibility", "conscience", "integrity", "compassion"
            ],
            "constructive_action": [
                "help", "volunteer", "community", "support", "positive impact",
                "make a difference", "contribute", "assist", "aid"
            ]
        }
    
    def _load_crisis_keywords(self) -> List[str]:
        """Load keywords that indicate crisis situations requiring immediate attention"""
        return [
            "suicide", "kill myself", "end it all", "can't go on",
            "self harm", "hurt myself", "cutting", "overdose",
            "emergency", "crisis", "desperate", "hopeless",
            "abuse", "violence", "threat", "danger"
        ]
    
    def _load_off_topic_patterns(self) -> List[str]:
        """Load patterns that indicate off-topic discussions"""
        return [
            r"\b(invest|stock|crypto|bitcoin|trading|money|financial advice)\b",
            r"\b(political|election|vote|democrat|republican|liberal|conservative)\b",
            r"\b(medical|doctor|diagnose|treatment|medication|prescription)\b",
            r"\b(legal|lawyer|court|lawsuit|sue|illegal)\b",
            r"\b(sexual|adult|explicit|nsfw)\b"
        ]
    
    def _init_perspective_api(self):
        """Initialize Google Perspective API client if available"""
        try:
            # This would require google-cloud-perspective library
            # For now, return None as placeholder
            return None
        except ImportError:
            self.logger.info("Perspective API not available")
            return None
    
    def _init_openai_client(self):
        """Initialize OpenAI moderation client if available"""
        try:
            openai_key = os.getenv("OPENAI_API_KEY")
            if openai_key:
                import openai
                openai.api_key = openai_key
                return openai
            return None
        except ImportError:
            self.logger.info("OpenAI moderation not available")
            return None
    
    async def moderate_content(self, text: str) -> ModerationResult:
        """
        Comprehensive content moderation
        """
        try:
            flags = []
            confidence = 0.8
            
            # Check for crisis indicators
            crisis_result = self._detect_crisis_situations(text)
            if crisis_result["is_crisis"]:
                flags.extend(crisis_result["indicators"])
                confidence = 0.95
            
            # Check for off-topic content
            off_topic_result = self._detect_off_topic_content(text)
            if off_topic_result["is_off_topic"]:
                flags.extend(off_topic_result["topics"])
            
            # Check for toxic content (basic implementation)
            toxicity_result = await self._check_basic_toxicity(text)
            if toxicity_result["is_toxic"]:
                flags.extend(toxicity_result["issues"])
            
            # Check with external APIs if available
            if self.openai_client:
                external_result = await self._check_external_moderation(text)
                if external_result["flagged"]:
                    flags.extend(external_result["categories"])
            
            # Determine if content is safe
            is_safe = len(flags) == 0 or all(flag in ["mild_off_topic"] for flag in flags)
            
            explanation = self._generate_explanation(flags, is_safe)
            
            return ModerationResult(
                is_safe=is_safe,
                flags=flags,
                confidence=confidence,
                explanation=explanation
            )
            
        except Exception as e:
            self.logger.error(f"Error in content moderation: {e}")
            # Fail safe - allow content but log error
            return ModerationResult(
                is_safe=True,
                flags=["moderation_error"],
                confidence=0.1,
                explanation="Content moderation service temporarily unavailable"
            )
    
    def _detect_crisis_situations(self, text: str) -> Dict[str, Any]:
        """Detect crisis situations requiring immediate intervention"""
        text_lower = text.lower()
        indicators = []
        
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                indicators.append(f"crisis_indicator_{keyword.replace(' ', '_')}")
        
        # Pattern-based detection
        crisis_patterns = [
            r"\bi want to (die|kill myself|end it all)\b",
            r"\bi can't (take it|go on|handle this) anymore\b",
            r"\bnothing matters\b.*\bwhat's the point\b",
            r"\bno one would miss me\b"
        ]
        
        for pattern in crisis_patterns:
            if re.search(pattern, text_lower):
                indicators.append("crisis_pattern_detected")
        
        return {
            "is_crisis": len(indicators) > 0,
            "indicators": indicators
        }
    
    def _detect_off_topic_content(self, text: str) -> Dict[str, Any]:
        """Detect off-topic content that should be redirected"""
        text_lower = text.lower()
        detected_topics = []
        
        # Check against off-topic patterns
        for pattern in self.off_topic_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                topic_name = pattern.split(r'\b(')[1].split('|')[0] if '|' in pattern else "general"
                detected_topics.append(f"off_topic_{topic_name}")
        
        # Check for on-topic content
        on_topic_score = 0
        for category, keywords in self.ethical_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    on_topic_score += 1
        
        # If content has some on-topic elements, it's only mildly off-topic
        if detected_topics and on_topic_score > 0:
            detected_topics = ["mild_off_topic"]
        
        return {
            "is_off_topic": len(detected_topics) > 0 and on_topic_score == 0,
            "topics": detected_topics
        }
    
    async def _check_basic_toxicity(self, text: str) -> Dict[str, Any]:
        """Basic toxicity detection using keyword patterns"""
        text_lower = text.lower()
        toxic_patterns = [
            r"\b(hate|stupid|idiot|moron|dumb)\b.*\b(people|person|you)\b",
            r"\b(kill|hurt|harm).*\b(others|someone|people)\b",
            r"\bfuck (you|off|this)\b",
            r"\b(racist|sexist|homophobic)\b"
        ]
        
        issues = []
        for pattern in toxic_patterns:
            if re.search(pattern, text_lower):
                issues.append("toxic_language")
                break
        
        return {
            "is_toxic": len(issues) > 0,
            "issues": issues
        }
    
    async def _check_external_moderation(self, text: str) -> Dict[str, Any]:
        """Check content using external moderation APIs"""
        try:
            if self.openai_client:
                response = self.openai_client.Moderation.create(input=text)
                result = response["results"][0]
                
                flagged_categories = []
                if result["flagged"]:
                    for category, flagged in result["categories"].items():
                        if flagged:
                            flagged_categories.append(f"openai_{category}")
                
                return {
                    "flagged": result["flagged"],
                    "categories": flagged_categories
                }
            
            return {"flagged": False, "categories": []}
            
        except Exception as e:
            self.logger.error(f"External moderation API error: {e}")
            return {"flagged": False, "categories": []}
    
    def _generate_explanation(self, flags: List[str], is_safe: bool) -> str:
        """Generate human-readable explanation of moderation decision"""
        if is_safe and not flags:
            return "Content appears to be appropriate ethical guidance discussion."
        
        if "crisis" in " ".join(flags):
            return "Content indicates a potential crisis situation. Please consider reaching out to mental health professionals or crisis hotlines."
        
        if "off_topic" in " ".join(flags):
            return "Content appears to be outside EthicCompanion's focus area of ethical information management and inner peace."
        
        if "toxic" in " ".join(flags):
            return "Content contains potentially harmful language that doesn't align with constructive ethical discussion."
        
        return "Content flagged for review to ensure it aligns with ethical guidance principles."
    
    def steer_conversation_ethically(self, user_query: str) -> Optional[str]:
        """
        Provide gentle redirection for off-topic queries
        """
        text_lower = user_query.lower()
        
        # Financial advice redirection
        if re.search(r"\b(invest|crypto|trading|money|financial)\b", text_lower):
            return ("I'm designed to help with ethical guidance on information management and finding inner peace. "
                   "For financial advice, I'd recommend consulting with certified financial advisors who can provide "
                   "personalized guidance based on your specific situation.")
        
        # Political redirection
        if re.search(r"\b(political|election|vote|party)\b", text_lower):
            return ("I focus on helping with ethical information management rather than political discussions. "
                   "I can help you find peace with overwhelming political news or develop healthy media consumption habits. "
                   "Would you like guidance on managing political information overload?")
        
        # Medical redirection
        if re.search(r"\b(medical|doctor|symptoms|diagnosis)\b", text_lower):
            return ("I can't provide medical advice, but I can help with the ethical aspects of health information management. "
                   "For medical concerns, please consult healthcare professionals. I can help you manage health-related "
                   "information overwhelm or anxiety about medical news if that would be helpful.")
        
        # Legal redirection
        if re.search(r"\b(legal|lawyer|court|lawsuit)\b", text_lower):
            return ("I'm not able to provide legal advice, but I can help with ethical guidance on information management. "
                   "For legal matters, please consult qualified legal professionals. Is there an ethical dimension to "
                   "information or peace-finding that I can help with instead?")
        
        return None
    
    async def check_health(self) -> bool:
        """Check if the guardrails service is healthy"""
        try:
            # Test moderation with safe content
            test_result = await self.moderate_content("This is a test message about mindfulness.")
            return test_result is not None
        except Exception as e:
            self.logger.error(f"Guardrails health check failed: {e}")
            return False
