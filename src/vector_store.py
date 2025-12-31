# ============================================
# FILE: src/vector_store.py
# ============================================
"""Vector store implementation using ChromaDB"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os

class VectorStore:
    """Manages document embeddings and retrieval using ChromaDB"""
    
    def __init__(self, persist_directory="./chroma_db"):
        """Initialize ChromaDB client and collection"""
        if not os.path.exists(persist_directory):
            os.makedirs(persist_directory)

        # PersistentClient ensures data is written to disk, not just RAM
        self.client = chromadb.PersistentClient(path=persist_directory)
        
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
        batch_size = 100
        total_chunks = len(chunks)

        for i in range(0, total_chunks, batch_size):
            batch = chunks[i : i + batch_size]
            
            # Create IDs and Metadata for this specific batch
            ids = [f"{filename}_chunk_{i + j}" for j in range(len(batch))]
            metadatas = [{"source": filename, "chunk_id": i + j} for j in range(len(batch))]
            
            self.collection.add(
                documents=batch,
                ids=ids,
                metadatas=metadatas
            )
    
    def retrieve(self, query: str, n_results: int = 5) -> Dict:
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
