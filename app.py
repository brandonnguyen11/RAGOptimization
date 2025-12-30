# ============================================
# FILE: app.py
# ============================================
import streamlit as st
from src.document_processor import extract_text_from_pdf, chunk_text
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
from config import *
import os

# Page config
st.set_page_config(
    page_title="Financial Report AI Assistant",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'document_indexed' not in st.session_state:
    st.session_state.document_indexed = False

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_choice = st.selectbox("Select AI Provider", ["OpenAI", "Groq"])
    api_key = st.text_input(f"{api_choice} API Key", type="password")
    
    st.divider()
    st.header("📁 Upload Financial Report")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file and not st.session_state.document_indexed:
        with st.spinner("Processing and indexing document..."):
            text = extract_text_from_pdf(uploaded_file)
            chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            
            # Initialize RAG pipeline
            vector_store = VectorStore()
            vector_store.index_chunks(chunks, uploaded_file.name)
            
            st.session_state.rag_pipeline = RAGPipeline(
                vector_store=vector_store,
                api_choice=api_choice,
                api_key=api_key
            )
            
            st.session_state.document_indexed = True
            st.success(f"✅ Indexed {len(chunks)} chunks!")
    
    if st.session_state.document_indexed:
        st.info("📄 Document ready")
        if st.button("🗑️ Clear"):
            # Trigger the method you just showed me
            st.session_state.rag_pipeline.vector_store.clear()
            
            # Reset UI states
            st.session_state.messages = []
            st.session_state.document_indexed = False
            st.rerun()

# Main UI
st.title("📊 Financial Report AI Assistant")
st.markdown("Upload your financial report and ask questions to get accurate insights.")

# Example prompts
if st.session_state.document_indexed:
    st.subheader("💡 Example Questions")
    col1, col2 = st.columns(2)
    
    example_prompts = [
        "What's the total revenue for 2024?",
        "Show profit or loss for this period",
        "Compare Q1 vs Q4 performance",
        "Summarize key financial metrics"
    ]
    
    for i, prompt in enumerate(example_prompts):
        col = col1 if i % 2 == 0 else col2
        if col.button(f"📈 {prompt}", use_container_width=True, key=f"btn_{i}"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

st.divider()

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your financial report...", disabled=not st.session_state.document_indexed or not api_key):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = st.session_state.rag_pipeline.generate_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

if not st.session_state.document_indexed:
    st.info("👆 Upload a financial report PDF to get started")
