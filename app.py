# ============================================
# FILE: app.py
# ============================================
import streamlit as st
from src.document_processor import process_pdf
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
if 'indexed_files' not in st.session_state:
    st.session_state.indexed_files = []

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    api_choice = st.selectbox("Select AI Provider", ["OpenAI", "Groq"])
    api_key = st.text_input(f"{api_choice} API Key", type="password")
    
    st.divider()
    st.header("📁 Upload Financial Reports")
    # accept_multiple_files=True allows batch processing
    uploaded_files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)

    # Initialize a file tracker in session state if not present
    if 'indexed_files' not in st.session_state:
        st.session_state.indexed_files = []

    if uploaded_files and api_key:
        for uploaded_file in uploaded_files:
            # Only process if this specific file hasn't been indexed yet
            if uploaded_file.name not in st.session_state.indexed_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    
                    # 1. NEW: Process large file page-by-page (avoids RAM crash)
                    # This calls the method from our new document_processor.py
                    chunks = process_pdf(uploaded_file, CHUNK_SIZE, CHUNK_OVERLAP)
                    
                    # 2. Initialize RAG pipeline if first time
                    if st.session_state.rag_pipeline is None:
                        # Ensure your VectorStore uses PersistentClient
                        st.session_state.rag_pipeline = RAGPipeline(
                            vector_store=VectorStore(),
                            api_choice=api_choice,
                            api_key=api_key
                        )
                    
                    # 3. Add chunks using the new BATCH method in vector_store.py
                    st.session_state.rag_pipeline.vector_store.index_chunks(chunks, uploaded_file.name)
                    
                    # Update tracking
                    st.session_state.indexed_files.append(uploaded_file.name)
                    st.session_state.document_indexed = True
                
                st.success(f"✅ Added {uploaded_file.name} ({len(chunks)} chunks)")

    # Display List of Loaded Documents
    if st.session_state.indexed_files:
        st.write("---")
        st.write("📊 **Documents in Database:**")
        for f in st.session_state.indexed_files:
            st.caption(f"• {f}")
        
        if st.button("🗑️ Clear All Data"):
            st.session_state.rag_pipeline.vector_store.clear()
            #st.session_state.messages = []
            st.session_state.indexed_files = []
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
