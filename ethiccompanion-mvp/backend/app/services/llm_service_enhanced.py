import asyncio
import logging
import time
import os
import kagglehub
import torch
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum

# Google AI imports
import google.generativeai as genai
from google.cloud import aiplatform

# Anthropic
from anthropic import Anthropic

# Gemma 3n specific imports
from transformers import (
    AutoProcessor, 
    Gemma3nForConditionalGeneration,
    pipeline
)

# Import enhanced models
try:
    from ..models.chat_models_enhanced import LLMProvider, EthicalRequest, EthicalResponse
except ImportError:
    # Fallback for direct execution
    class LLMProvider(Enum):
        GEMINI = "gemini"
        GEMMA_3N = "gemma_3n"
        CLAUDE = "claude"
        OPENAI = "openai"

@dataclass
class LLMResponse:
    content: str
    model_used: str
    confidence: float
    reasoning: str
    token_count: int
    processing_time: float
    fallback_used: bool = False
    provider: str = "unknown"
    multimodal_processed: bool = False

class Gemma3nManager:
    """
    Dedicated manager for Gemma 3n models with multimodal capabilities
    """
    
    def __init__(self):
        self.models = {}
        self.processors = {}
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_configs = {
            "e2b": {
                "model_id": "google/gemma-3n-e2b",
                "effective_params": "2B",
                "use_case": "Fast ethical classifications and content moderation"
            },
            "e4b": {
                "model_id": "google/gemma-3n-e4b", 
                "effective_params": "4B",
                "use_case": "Complex ethical reasoning and guidance generation"
            }
        }
        
    async def load_model(self, model_size: str = "e2b") -> bool:
        """Load Gemma 3n model for inference"""
        try:
            if model_size in self.models:
                return True
                
            config = self.model_configs.get(model_size)
            if not config:
                logging.error(f"Unknown Gemma 3n model size: {model_size}")
                return False
            
            model_id = config["model_id"]
            
            # Try to load via kagglehub first, fallback to direct transformers
            try:
                import kagglehub
                gemma_path = kagglehub.model_download(f"google/gemma-3n/transformers/gemma-3n-{model_size}")
                model = Gemma3nForConditionalGeneration.from_pretrained(
                    gemma_path, 
                    torch_dtype=torch.bfloat16,
                    device_map="auto"
                ).eval()
                processor = AutoProcessor.from_pretrained(gemma_path)
            except ImportError:
                # Fallback to direct model loading
                model = Gemma3nForConditionalGeneration.from_pretrained(
                    model_id,
                    torch_dtype=torch.bfloat16,
                    device_map="auto"
                ).eval()
                processor = AutoProcessor.from_pretrained(model_id)
            
            self.models[model_size] = model
            self.processors[model_size] = processor
            
            logging.info(f"✅ Loaded Gemma 3n {model_size.upper()} ({config['effective_params']}) for {config['use_case']}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to load Gemma 3n {model_size}: {str(e)}")
            return False
    
    async def generate_response(
        self, 
        prompt: str, 
        model_size: str = "e2b",
        images: Optional[List] = None,
        max_tokens: int = 512
    ) -> LLMResponse:
        """Generate response using Gemma 3n with multimodal support"""
        start_time = time.time()
        
        try:
            # Ensure model is loaded
            if not await self.load_model(model_size):
                raise Exception(f"Failed to load Gemma 3n {model_size}")
            
            model = self.models[model_size]
            processor = self.processors[model_size]
            
            # Prepare inputs
            if images:
                # Multimodal processing
                model_inputs = processor(
                    text=prompt, 
                    images=images, 
                    return_tensors="pt"
                ).to(model.device)
                multimodal_processed = True
            else:
                # Text-only processing
                model_inputs = processor(
                    text=prompt, 
                    return_tensors="pt"
                ).to(model.device)
                multimodal_processed = False
            
            input_len = model_inputs["input_ids"].shape[-1]
            
            # Generate response
            with torch.inference_mode():
                generation = model.generate(
                    **model_inputs, 
                    max_new_tokens=max_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    disable_compile=True
                )
                
            # Decode response
            generated_tokens = generation[0][input_len:]
            response_text = processor.decode(generated_tokens, skip_special_tokens=True)
            
            processing_time = time.time() - start_time
            
            return LLMResponse(
                content=response_text,
                model_used=f"gemma-3n-{model_size}",
                confidence=0.85,  # Gemma 3n typically provides reliable outputs
                reasoning=f"Generated using Gemma 3n {model_size.upper()} with {self.model_configs[model_size]['effective_params']} effective parameters",
                token_count=len(generated_tokens),
                processing_time=processing_time,
                provider="gemma_3n",
                multimodal_processed=multimodal_processed
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            logging.error(f"Gemma 3n generation failed: {str(e)}")
            
            return LLMResponse(
                content=f"Error generating response with Gemma 3n: {str(e)}",
                model_used=f"gemma-3n-{model_size}-error",
                confidence=0.0,
                reasoning=f"Failed to generate response: {str(e)}",
                token_count=0,
                processing_time=processing_time,
                fallback_used=True,
                provider="gemma_3n"
            )

class LLMOrchestrator:
    """
    Enhanced multi-LLM service orchestrator for EthicCompanion
    Supports Gemini, Gemma 3n, Claude, and automatic provider selection with fallbacks.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.providers = {}
        self.gemma_manager = Gemma3nManager()
        
        # Provider priorities for different use cases
        self.provider_priorities = {
            "ethical_classification": [LLMProvider.GEMMA_3N, LLMProvider.GEMINI, LLMProvider.CLAUDE],
            "crisis_detection": [LLMProvider.GEMMA_3N, LLMProvider.CLAUDE, LLMProvider.GEMINI],
            "general_guidance": [LLMProvider.GEMINI, LLMProvider.GEMMA_3N, LLMProvider.CLAUDE],
            "multimodal": [LLMProvider.GEMMA_3N, LLMProvider.GEMINI]
        }
        self._initialize_providers()
        
    def _initialize_providers(self):
        """Initialize all available LLM providers"""
        # Initialize Gemini
        try:
            gemini_key = os.getenv("GEMINI_API_KEY")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                self.providers["gemini"] = {
                    "client": genai.GenerativeModel('gemini-pro'),
                    "multimodal_client": genai.GenerativeModel('gemini-pro-vision'),
                    "available": True
                }
                self.logger.info("Gemini provider initialized successfully")
            else:
                self.logger.warning("Gemini API key not found")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gemini: {e}")
            
        # Initialize Claude
        try:
            claude_key = os.getenv("CLAUDE_API_KEY")
            if claude_key:
                self.providers["claude"] = {
                    "client": Anthropic(api_key=claude_key),
                    "available": True
                }
                self.logger.info("Claude provider initialized successfully")
            else:
                self.logger.warning("Claude API key not found")
        except Exception as e:
            self.logger.error(f"Failed to initialize Claude: {e}")
            
        # Gemma 3n would be initialized here for local inference
        # For now, we'll use a placeholder
        self.providers["gemma_3n"] = {
            "client": None,  # Would be HuggingFace pipeline
            "available": False  # Set to True when implemented
        }
    
    async def get_ethical_guidance(
        self, 
        query: str, 
        context: Dict[str, Any] = None,
        preferred_model: str = "auto",
        max_tokens: int = 1000,
        temperature: float = 0.7
    ) -> LLMResponse:
        """
        Get ethical guidance using the specified or automatically selected LLM
        """
        start_time = time.time()
        context = context or {}
        
        # Determine which provider to use
        provider = self._select_provider(preferred_model, context)
        
        # Build the prompt
        prompt = self._build_ethical_prompt(query, context)
        
        try:
            if provider == "gemini":
                response = await self._call_gemini(prompt, context, max_tokens, temperature)
            elif provider == "claude":
                response = await self._call_claude(prompt, context, max_tokens, temperature)
            elif provider == "gemma_3n":
                response = await self._call_gemma_3n(prompt, context, max_tokens, temperature)
            else:
                # Fallback to available provider
                response = await self._fallback_provider(prompt, context, max_tokens, temperature)
                response.fallback_used = True
                
            response.processing_time = time.time() - start_time
            return response
            
        except Exception as e:
            self.logger.error(f"Error with primary provider {provider}: {e}")
            # Try fallback
            try:
                response = await self._fallback_provider(prompt, context, max_tokens, temperature)
                response.fallback_used = True
                response.processing_time = time.time() - start_time
                return response
            except Exception as fallback_error:
                self.logger.error(f"Fallback also failed: {fallback_error}")
                raise Exception(f"All LLM providers failed: {e}")
    
    def _select_provider(self, preferred: str, context: Dict[str, Any]) -> str:
        """Select the best provider based on preferences and context"""
        if preferred != "auto" and preferred in self.providers and self.providers[preferred]["available"]:
            return preferred
            
        # Auto-selection logic
        has_image = context.get("image_data") is not None
        
        # Prefer Gemini for multimodal queries
        if has_image and self.providers.get("gemini", {}).get("available"):
            return "gemini"
            
        # Default priority: Gemini -> Claude -> Gemma 3n
        for provider in ["gemini", "claude", "gemma_3n"]:
            if self.providers.get(provider, {}).get("available"):
                return provider
                
        raise Exception("No LLM providers available")
    
    def _build_ethical_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Build a comprehensive prompt for ethical guidance"""
        
        # Extract relevant context
        relevant_docs = context.get("relevant_docs", [])
        stress_level = context.get("user_stress_level", "moderate")
        conversation_history = context.get("conversation_history", [])
        
        # Build context from RAG documents
        context_text = ""
        if relevant_docs:
            context_text = "Relevant information from knowledge base:\n"
            for i, doc in enumerate(relevant_docs[:3], 1):
                context_text += f"{i}. {doc['content'][:300]}...\n"
        
        # Build conversation history
        history_text = ""
        if conversation_history:
            history_text = "Previous conversation context:\n"
            for msg in conversation_history[-3:]:  # Last 3 messages
                history_text += f"- {msg}\n"
        
        prompt = f"""You are EthicCompanion, an AI assistant focused on providing ethical guidance for information management and finding inner peace in our digital age.

User's stress level: {stress_level}
User's question: {query}

{context_text}

{history_text}

Please provide:
1. Clear, empathetic ethical guidance
2. Concrete reasoning for your advice
3. Practical steps the user can take
4. Mindfulness techniques if appropriate

Guidelines:
- Focus on constructive, positive actions
- Be culturally sensitive and inclusive
- Encourage professional help for serious issues
- Stay within ethical information management scope
- Provide hope and actionable guidance

Response format:
ADVICE: [Your main ethical guidance]
REASONING: [Explanation of your advice]
"""
        
        return prompt
    
    async def _call_gemini(self, prompt: str, context: Dict[str, Any], max_tokens: int, temperature: float) -> LLMResponse:
        """Call Google Gemini API"""
        try:
            # Handle multimodal if image present
            if context.get("image_data"):
                # For multimodal queries, you'd need to implement image handling
                client = self.providers["gemini"]["multimodal_client"]
                # Implementation would handle base64 image conversion
                response = client.generate_content(prompt)
            else:
                client = self.providers["gemini"]["client"]
                response = client.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=temperature
                    )
                )
            
            content = response.text
            
            # Parse the structured response
            advice, reasoning = self._parse_structured_response(content)
            
            return LLMResponse(
                content=advice,
                model_used="gemini-pro",
                confidence=0.85,  # Would implement actual confidence scoring
                reasoning=reasoning,
                token_count=len(content.split()) * 1.3,  # Rough estimation
                processing_time=0  # Will be set by caller
            )
            
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise
    
    async def _call_claude(self, prompt: str, context: Dict[str, Any], max_tokens: int, temperature: float) -> LLMResponse:
        """Call Anthropic Claude API"""
        try:
            client = self.providers["claude"]["client"]
            
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text
            
            # Parse the structured response
            advice, reasoning = self._parse_structured_response(content)
            
            return LLMResponse(
                content=advice,
                model_used="claude-3-sonnet",
                confidence=0.87,
                reasoning=reasoning,
                token_count=response.usage.output_tokens if hasattr(response, 'usage') else len(content.split()) * 1.3,
                processing_time=0
            )
            
        except Exception as e:
            self.logger.error(f"Claude API error: {e}")
            raise
    
    async def _call_gemma_3n(self, prompt: str, context: Dict[str, Any], max_tokens: int, temperature: float) -> LLMResponse:
        """Call Gemma 3n local model (placeholder implementation)"""
        # This would be implemented with HuggingFace Transformers
        # For now, return a placeholder response
        raise NotImplementedError("Gemma 3n local inference not yet implemented")
    
    async def _fallback_provider(self, prompt: str, context: Dict[str, Any], max_tokens: int, temperature: float) -> LLMResponse:
        """Try fallback providers in order of preference"""
        for provider in ["gemini", "claude"]:
            if self.providers.get(provider, {}).get("available"):
                try:
                    if provider == "gemini":
                        return await self._call_gemini(prompt, context, max_tokens, temperature)
                    elif provider == "claude":
                        return await self._call_claude(prompt, context, max_tokens, temperature)
                except Exception as e:
                    self.logger.error(f"Fallback provider {provider} failed: {e}")
                    continue
        
        # Ultimate fallback - simple response
        return LLMResponse(
            content="I'm experiencing technical difficulties. Please try again later or contact support.",
            model_used="fallback",
            confidence=0.1,
            reasoning="System fallback due to LLM provider unavailability",
            token_count=20,
            processing_time=0,
            fallback_used=True
        )
    
    def _parse_structured_response(self, content: str) -> tuple:
        """Parse structured response into advice and reasoning"""
        try:
            lines = content.split('\n')
            advice = ""
            reasoning = ""
            
            current_section = None
            for line in lines:
                if line.startswith("ADVICE:"):
                    current_section = "advice"
                    advice = line.replace("ADVICE:", "").strip()
                elif line.startswith("REASONING:"):
                    current_section = "reasoning"
                    reasoning = line.replace("REASONING:", "").strip()
                elif current_section == "advice" and line.strip():
                    advice += " " + line.strip()
                elif current_section == "reasoning" and line.strip():
                    reasoning += " " + line.strip()
            
            # Fallback if structured parsing fails
            if not advice:
                advice = content
                reasoning = "Comprehensive ethical guidance based on knowledge base and best practices."
                
            return advice, reasoning
            
        except Exception:
            return content, "Ethical guidance provided based on available information."
    
    async def check_health(self) -> Dict[str, bool]:
        """Check health of all LLM providers"""
        health_status = {}
        
        for provider_name, provider_info in self.providers.items():
            try:
                if provider_info["available"]:
                    # You could implement actual health checks here
                    health_status[provider_name] = True
                else:
                    health_status[provider_name] = False
            except Exception:
                health_status[provider_name] = False
        
        return health_status
