# ============================================
# FILE: src/rag_pipeline.py
# ============================================
"""RAG pipeline orchestration"""
from src.vector_store import VectorStore
from src.llm_handler import LLMHandler
from config import SYSTEM_PROMPT, N_RESULTS

class RAGPipeline:
    """Orchestrates the RAG pipeline: Retrieve → Augment → Generate"""
    
    def __init__(self, vector_store: VectorStore, api_choice: str, api_key: str):
        """
        Initialize RAG pipeline
        
        Args:
            vector_store: VectorStore instance
            api_choice: LLM provider choice
            api_key: API key
        """
        self.vector_store = vector_store
        self.llm_handler = LLMHandler(api_choice, api_key)
    
    def generate_response(self, query: str) -> str:
        """
        Generate response using RAG pipeline
        
        Args:
            query: User question
            
        Returns:
            str: Generated response
        """
        # Step 1: Retrieve relevant chunks
        results = self.vector_store.retrieve(query, N_RESULTS)
        
        if not results['documents'][0]:
            return "I couldn't find relevant information in the financial report."
        
        # Step 2: Augment - combine chunks as context
        context = "\n\n".join(results['documents'][0])
        
        # Step 3: Generate response
        user_prompt = f"""Context from financial report:
{context}

Question: {query}

Provide a detailed answer with specific numbers and calculations from the context."""
        
        response = self.llm_handler.generate(SYSTEM_PROMPT, user_prompt)
        
        return response

