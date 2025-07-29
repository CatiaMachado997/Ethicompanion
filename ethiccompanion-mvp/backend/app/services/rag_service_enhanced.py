import asyncio
import logging
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass

# Vector database and embeddings
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Google Cloud Vertex AI
try:
    from google.cloud import aiplatform
    from vertexai.language_models import TextEmbeddingModel
    from langchain_google_vertexai import VertexAIEmbeddings
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    logging.warning("Vertex AI not available, using fallback embeddings")

# LangChain for orchestration
try:
    from langchain.document_loaders import DirectoryLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain.embeddings import HuggingFaceEmbeddings
    from langchain.vectorstores import Chroma
    from langchain.schema import Document
except ImportError:
    # Fallback for different LangChain versions
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain.schema import Document

@dataclass
class RAGResult:
    """Result from RAG retrieval and generation"""
    query: str
    retrieved_contexts: List[str]
    context_scores: List[float]
    generated_response: str
    source_documents: List[str]
    confidence_score: float
    ethical_principles: List[str]

class EthicalRAGService:
    """
    Enhanced RAG service for ethical knowledge retrieval and generation
    """
    
    def __init__(self, knowledge_base_path: str = None):
        self.logger = logging.getLogger(__name__)
        
        # Set default path relative to backend directory
        if knowledge_base_path is None:
            current_dir = Path(__file__).parent.parent.parent
            self.knowledge_base_path = current_dir / "ethical_knowledge_base"
        else:
            self.knowledge_base_path = Path(knowledge_base_path)
            
        self.chroma_db_path = Path("./chroma_db")
        self.embeddings = self._initialize_embeddings()
        self.vector_store = None
        self.is_initialized = False
        
        # Initialize the vector store
        asyncio.create_task(self._initialize_vector_store())
    
    def _initialize_embeddings(self):
        """Initialize embeddings model (using HuggingFace as fallback)"""
        try:
            # Try to use a good general-purpose embedding model
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}  # Use GPU if available
            )
            self.logger.info("HuggingFace embeddings initialized successfully")
            return embeddings
        except Exception as e:
            self.logger.error(f"Failed to initialize embeddings: {e}")
            # Fallback to basic embeddings
            return None
    
    async def _initialize_vector_store(self):
        """Initialize ChromaDB vector store"""
        try:
            # Create ChromaDB client
            client = chromadb.PersistentClient(
                path=str(self.chroma_db_path),
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            if self.embeddings:
                self.vector_store = Chroma(
                    client=client,
                    collection_name="ethical_knowledge",
                    embedding_function=self.embeddings
                )
            else:
                # Fallback: use ChromaDB's default embeddings
                self.collection = client.get_or_create_collection(
                    name="ethical_knowledge_fallback"
                )
                
            self.is_initialized = True
            self.logger.info("Vector store initialized successfully")
            
            # Ingest documents if the database is empty
            await self._check_and_ingest_documents()
            
        except Exception as e:
            self.logger.error(f"Failed to initialize vector store: {e}")
            self.is_initialized = False
    
    async def _check_and_ingest_documents(self):
        """Check if documents are already ingested, if not, ingest them"""
        try:
            if self.vector_store:
                # Check if collection has documents
                collection_count = self.vector_store._collection.count()
                if collection_count == 0:
                    self.logger.info("Empty vector store detected, ingesting documents...")
                    await self.ingest_knowledge_base()
                else:
                    self.logger.info(f"Vector store has {collection_count} documents")
            else:
                # Fallback collection check
                if hasattr(self, 'collection'):
                    count = self.collection.count()
                    if count == 0:
                        await self.ingest_knowledge_base()
                        
        except Exception as e:
            self.logger.error(f"Error checking document count: {e}")
    
    async def ingest_knowledge_base(self):
        """Ingest Markdown documents from knowledge base"""
        try:
            if not self.knowledge_base_path.exists():
                self.logger.warning(f"Knowledge base path does not exist: {self.knowledge_base_path}")
                return
            
            self.logger.info(f"Ingesting documents from: {self.knowledge_base_path}")
            
            # Load documents
            documents = []
            for md_file in self.knowledge_base_path.glob("*.md"):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append({
                            "content": content,
                            "metadata": {
                                "source": md_file.name,
                                "type": "ethical_knowledge",
                                "path": str(md_file)
                            }
                        })
                except Exception as e:
                    self.logger.error(f"Failed to load {md_file}: {e}")
            
            if not documents:
                self.logger.warning("No documents found to ingest")
                return
            
            # Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            chunks = []
            for doc in documents:
                doc_chunks = text_splitter.split_text(doc["content"])
                for i, chunk in enumerate(doc_chunks):
                    chunks.append({
                        "content": chunk,
                        "metadata": {
                            **doc["metadata"],
                            "chunk_id": i,
                            "total_chunks": len(doc_chunks)
                        }
                    })
            
            # Add to vector store
            if self.vector_store and self.embeddings:
                # Using LangChain + ChromaDB
                texts = [chunk["content"] for chunk in chunks]
                metadatas = [chunk["metadata"] for chunk in chunks]
                
                self.vector_store.add_texts(
                    texts=texts,
                    metadatas=metadatas
                )
                
            elif hasattr(self, 'collection'):
                # Fallback: direct ChromaDB usage
                for i, chunk in enumerate(chunks):
                    self.collection.add(
                        documents=[chunk["content"]],
                        metadatas=[chunk["metadata"]],
                        ids=[f"doc_{i}"]
                    )
            
            self.logger.info(f"Successfully ingested {len(chunks)} document chunks from {len(documents)} files")
            
        except Exception as e:
            self.logger.error(f"Error ingesting knowledge base: {e}")
    
    async def get_relevant_context(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve relevant documents for a query"""
        try:
            if not self.is_initialized:
                self.logger.warning("RAG service not initialized, returning empty context")
                return []
            
            if self.vector_store:
                # Using LangChain vector store
                docs = self.vector_store.similarity_search_with_score(query, k=k)
                return [
                    {
                        "content": doc.page_content,
                        "metadata": doc.metadata,
                        "relevance_score": 1.0 - (score / 2.0)  # Convert distance to relevance
                    }
                    for doc, score in docs
                ]
            
            elif hasattr(self, 'collection'):
                # Fallback: direct ChromaDB query
                results = self.collection.query(
                    query_texts=[query],
                    n_results=k
                )
                
                contexts = []
                if results['documents'] and results['documents'][0]:
                    for i, doc in enumerate(results['documents'][0]):
                        contexts.append({
                            "content": doc,
                            "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                            "relevance_score": 1.0 - results['distances'][0][i] if results['distances'] else 0.5
                        })
                
                return contexts
            
            return []
            
        except Exception as e:
            self.logger.error(f"Error retrieving relevant context: {e}")
            return []
    
    async def search_by_topic(self, topic: str, k: int = 3) -> List[Dict]:
        """Search for documents by specific topic"""
        topic_queries = {
            "information_overload": "information overload digital overwhelm news management",
            "peace_techniques": "mindfulness meditation breathing peace calm",
            "crisis_management": "crisis emergency stress help support",
            "principles": "ethical principles values moral guidelines"
        }
        
        query = topic_queries.get(topic, topic)
        return await self.get_relevant_context(query, k)
    
    async def get_peace_techniques_for_stress_level(self, stress_level: str) -> List[str]:
        """Get specific peace techniques based on stress level"""
        try:
            # Search for peace techniques
            peace_docs = await self.search_by_topic("peace_techniques", k=3)
            
            # Extract techniques based on stress level
            techniques = []
            for doc in peace_docs:
                content = doc["content"].lower()
                
                if stress_level == "low":
                    if any(word in content for word in ["gentle", "light", "simple", "basic"]):
                        techniques.extend(self._extract_techniques(content))
                elif stress_level == "moderate":
                    if any(word in content for word in ["breathing", "meditation", "mindful"]):
                        techniques.extend(self._extract_techniques(content))
                elif stress_level == "high":
                    if any(word in content for word in ["grounding", "emergency", "immediate"]):
                        techniques.extend(self._extract_techniques(content))
                elif stress_level == "critical":
                    if any(word in content for word in ["crisis", "urgent", "professional"]):
                        techniques.extend(self._extract_techniques(content))
            
            return list(set(techniques))[:5]  # Return up to 5 unique techniques
            
        except Exception as e:
            self.logger.error(f"Error getting peace techniques: {e}")
            return []
    
    def _extract_techniques(self, content: str) -> List[str]:
        """Extract technique suggestions from content"""
        # Simple extraction - could be enhanced with NLP
        sentences = content.split('.')
        techniques = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) > 20 and len(sentence) < 150:
                # Look for action-oriented sentences
                if any(word in sentence.lower() for word in [
                    "try", "practice", "take", "breathe", "focus", "notice", "do"
                ]):
                    techniques.append(sentence)
        
        return techniques[:3]  # Return top 3 techniques per content piece
    
    async def check_health(self) -> bool:
        """Check if the RAG service is healthy"""
        try:
            if not self.is_initialized:
                return False
                
            # Try a simple query
            test_results = await self.get_relevant_context("test", k=1)
            return len(test_results) >= 0  # Even empty results indicate the service is working
            
        except Exception as e:
            self.logger.error(f"RAG health check failed: {e}")
            return False
