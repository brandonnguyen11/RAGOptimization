# ============================================
# FILE: src/document_processor.py
# ============================================
"""Document processing utilities for PDF extraction and text chunking"""
import PyPDF2
from typing import List
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from uploaded PDF file
    
    Args:
        pdf_file: Uploaded file object
        
    Returns:
        str: Extracted text from all pages
    """
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Input text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List[str]: List of text chunks
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # Clean up chunk
        chunk = chunk.strip()
        if chunk:
            chunks.append(chunk)
        
        start += chunk_size - overlap
    
    return chunks