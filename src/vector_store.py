# ============================================
# FILE: src/vector_store.py
# ============================================
"""Vector store implementation using ChromaDB"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict

class VectorStore:
    """Manages document embeddings and retrieval using ChromaDB"""
    
    def __init__(self):
        """Initialize ChromaDB client and collection"""
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            is_persistent=False
        ))
        
        self.collection = self.client.get_or_create_collection(
            name="financial_reports",
            metadata={"hnsw:space": "cosine"}
        )
    
    def index_chunks(self, chunks: List[str], filename: str):
        """
        Index document chunks into ChromaDB
        
        Args:
            chunks: List of text chunks to index
            filename: Source document filename
        """
        ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
        
        self.collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
    
    def retrieve(self, query: str, n_results: int = 3) -> Dict:
        """
        Retrieve most relevant chunks for a query
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            Dict: Query results with documents and metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return results
    
    def clear(self):
        """Clear all documents from collection"""
        self.client.delete_collection("financial_reports")
        self.collection = self.client.get_or_create_collection(
            name="financial_reports",
            metadata={"hnsw:space": "cosine"}
        )
