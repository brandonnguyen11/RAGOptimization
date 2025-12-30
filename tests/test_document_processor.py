# ============================================
# FILE: tests/test_document_processor.py
# ============================================
"""Tests for document processor"""
import pytest
from src.document_processor import chunk_text

def test_chunk_text():
    text = "A" * 2500
    chunks = chunk_text(text, chunk_size=1000, overlap=200)
    
    assert len(chunks) > 1
    assert all(len(chunk) <= 1000 for chunk in chunks)
