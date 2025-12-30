# ============================================
# FILE: config.py
# ============================================
"""Configuration settings for Financial RAG Chatbot"""

# Chunking parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval parameters
N_RESULTS = 3

# LLM parameters
TEMPERATURE = 0.3
MAX_TOKENS = 1500

# Model configurations
MODELS = {
    "OpenAI": "gpt-4o-mini",
    "Groq": "llama-3.3-70b-versatile"
}

# System prompt
SYSTEM_PROMPT = """You are a financial analyst assistant. 
Provide accurate, quantitative answers based on the provided context. 
Always cite specific numbers from the financial report.
If the information is not in the context, say so clearly."""