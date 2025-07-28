import os
import json
from typing import List, Dict
from pathlib import Path

class RAGService:
    """
    Serviço para Retrieval-Augmented Generation (RAG).
    Gerencia a base de conhecimento ético e busca por contexto relevante.
    """
    
    def __init__(self):
        self.knowledge_base_path = Path(__file__).parent.parent / "ethical_knowledge_base"
        self.knowledge_cache = {}
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """
        Carregar todos os arquivos da base de conhecimento na memória.
        """
        try:
            for file_path in self.knowledge_base_path.glob("*.md"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.knowledge_cache[file_path.stem] = content
            print(f"Base de conhecimento carregada: {len(self.knowledge_cache)} documentos")
        except Exception as e:
            print(f"Erro ao carregar base de conhecimento: {e}")
    
    async def get_relevant_context(self, query: str, max_context_length: int = 2000) -> str:
        """
        Buscar contexto relevante na base de conhecimento.
        Por enquanto, implementação simples com busca por palavras-chave.
        """
        query_lower = query.lower()
        relevant_content = []
        
        # Mapear palavras-chave para documentos
        keyword_mapping = {
            "principios": "principles",
            "principles": "principles",
            "ética": "principles",
            "ethics": "principles",
            "sobrecarga": "information_overload_guide",
            "overload": "information_overload_guide",
            "informação": "information_overload_guide",
            "information": "information_overload_guide",
            "stress": "information_overload_guide",
            "ansiedade": "information_overload_guide",
            "anxiety": "information_overload_guide",
            "paz": "peace_techniques",
            "peace": "peace_techniques",
            "mindfulness": "peace_techniques",
            "meditação": "peace_techniques",
            "meditation": "peace_techniques",
            "respiração": "peace_techniques",
            "breathing": "peace_techniques"
        }
        
        # Buscar documentos relevantes
        relevant_docs = set()
        for keyword, doc_name in keyword_mapping.items():
            if keyword in query_lower:
                relevant_docs.add(doc_name)
        
        # Se não encontrar palavras-chave específicas, incluir princípios básicos
        if not relevant_docs:
            relevant_docs.add("principles")
        
        # Coletar conteúdo relevante
        for doc_name in relevant_docs:
            if doc_name in self.knowledge_cache:
                content = self.knowledge_cache[doc_name]
                # Pegar os primeiros parágrafos ou seções relevantes
                relevant_content.append(f"=== {doc_name.replace('_', ' ').title()} ===\n{content[:800]}")
        
        # Concatenar e limitar o tamanho
        context = "\n\n".join(relevant_content)
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        return context
    
    def search_knowledge_base(self, keywords: List[str]) -> Dict[str, str]:
        """
        Buscar na base de conhecimento por palavras-chave específicas.
        """
        results = {}
        
        for doc_name, content in self.knowledge_cache.items():
            content_lower = content.lower()
            score = 0
            
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    score += content_lower.count(keyword.lower())
            
            if score > 0:
                results[doc_name] = {
                    "content": content,
                    "relevance_score": score
                }
        
        # Ordenar por relevância
        sorted_results = dict(sorted(results.items(), key=lambda x: x[1]["relevance_score"], reverse=True))
        return sorted_results
    
    def add_knowledge_document(self, name: str, content: str) -> bool:
        """
        Adicionar novo documento à base de conhecimento.
        """
        try:
            file_path = self.knowledge_base_path / f"{name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Atualizar cache
            self.knowledge_cache[name] = content
            return True
        except Exception as e:
            print(f"Erro ao adicionar documento: {e}")
            return False
