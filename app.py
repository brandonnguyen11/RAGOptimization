# ============================================
# FILE: app.py
# ============================================
import streamlit as st
from src.document_processor import process_pdf
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
from config import *
import os

# 1. Page Config (Hiding sidebar for a cleaner "Analyst" look)
st.set_page_config(
    page_title="Masan 2024 AI Analyst",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Sidebar via CSS for a professional "Search" feel
st.markdown("<style> [data-testid='stSidebar'] {display: none;} </style>", unsafe_allow_html=True)

# 2. Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'document_indexed' not in st.session_state:
    st.session_state.document_indexed = False

# 3. AUTO-INDEX FUNCTION (The "Pre-load" Logic)
def get_preloaded_pipeline():
    """Pre-loads the RAG pipeline with the Masan 2024 report if not already indexed"""
    # Initialize the store (connects to ./chroma_db)
    vector_store = VectorStore()
    
    pipeline = RAGPipeline(
        vector_store=vector_store,
        api_choice="Groq", 
        api_key=st.secrets["GROQ_API_KEY"]
    )

    # 🚀 The Logic: Only index if the database is empty!
    if vector_store.get_count() == 0:
        pdf_filename = "data/Masan_Annual_Report_2024.pdf"
        if os.path.exists(pdf_filename):
            chunks = process_pdf(pdf_filename, CHUNK_SIZE, CHUNK_OVERLAP)
            pipeline.vector_store.index_chunks(chunks, pdf_filename)
    
    return pipeline

# 4. Trigger Initialization
# If the pipeline isn't in state, get it from cache (instant after first run)
if st.session_state.rag_pipeline is None:
    cached_pipeline = get_preloaded_pipeline()
    if cached_pipeline:
        st.session_state.rag_pipeline = cached_pipeline
        st.session_state.document_indexed = True
    else:
        st.error("Document not found. Please check data/Masan_Annual_Report_2024.pdf")

# 4. Main UI Logic
st.title("📊 Masan 2024 AI Analyst")
st.caption("Strategic Intelligence Interface Powered by RAG & Groq Llama-3")

if st.session_state.document_indexed:
    # st.info("✅ **System Ready:** 2024 Annual Report is pre-loaded and indexed.")
    
    # Example prompts (Simplified for the "Analyst" persona)
    example_prompts = [
        "What was the total revenue in 2024?",
        "Explain the dividend policy mentioned in the report.",
        "Summarize the growth strategy for Masan Consumer.",
        "What are the major risk factors identified for 2025?"
    ]
    
    cols = st.columns(2)
    for i, prompt in enumerate(example_prompts):
        if cols[i % 2].button(f"🔍 {prompt}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()

st.divider()

# 5. Chat Interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a technical question about the 2024 report..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Retrieving facts and analyzing..."):
            response = st.session_state.rag_pipeline.generate_response(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})



# import streamlit as st
# from src.document_processor import process_pdf
# from src.vector_store import VectorStore
# from src.rag_pipeline import RAGPipeline
# from config import *
# import os

# # Page config
# st.set_page_config(
#     page_title="Financial Report AI Assistant",
#     page_icon="📊",
#     layout="wide"
# )

# # Initialize session state
# if 'messages' not in st.session_state:
#     st.session_state.messages = []
# if 'rag_pipeline' not in st.session_state:
#     st.session_state.rag_pipeline = None
# if 'document_indexed' not in st.session_state:
#     st.session_state.document_indexed = False
# if 'indexed_files' not in st.session_state:
#     st.session_state.indexed_files = []

# # Sidebar - Configuration
# with st.sidebar:
#     st.header("⚙️ Configuration")
    
#     api_choice = st.selectbox("Select AI Provider", ["OpenAI", "Groq"])
#     api_key = st.text_input(f"{api_choice} API Key", type="password")
    
#     st.divider()
#     st.header("📁 Upload Financial Reports")
#     # accept_multiple_files=True allows batch processing
#     uploaded_files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)

#     # Initialize a file tracker in session state if not present
#     if 'indexed_files' not in st.session_state:
#         st.session_state.indexed_files = []

#     if uploaded_files and api_key:
#         for uploaded_file in uploaded_files:
#             # Only process if this specific file hasn't been indexed yet
#             if uploaded_file.name not in st.session_state.indexed_files:
#                 with st.spinner(f"Processing {uploaded_file.name}..."):
                    
#                     # 1. NEW: Process large file page-by-page (avoids RAM crash)
#                     # This calls the method from our new document_processor.py
#                     chunks = process_pdf(uploaded_file, CHUNK_SIZE, CHUNK_OVERLAP)
                    
#                     # 2. Initialize RAG pipeline if first time
#                     if st.session_state.rag_pipeline is None:
#                         # Ensure your VectorStore uses PersistentClient
#                         st.session_state.rag_pipeline = RAGPipeline(
#                             vector_store=VectorStore(),
#                             api_choice=api_choice,
#                             api_key=api_key
#                         )
                    
#                     # 3. Add chunks using the new BATCH method in vector_store.py
#                     st.session_state.rag_pipeline.vector_store.index_chunks(chunks, uploaded_file.name)
                    
#                     # Update tracking
#                     st.session_state.indexed_files.append(uploaded_file.name)
#                     st.session_state.document_indexed = True
                
#                 st.success(f"✅ Added {uploaded_file.name} ({len(chunks)} chunks)")

#     # Display List of Loaded Documents
#     if st.session_state.indexed_files:
#         st.write("---")
#         st.write("📊 **Documents in Database:**")
#         for f in st.session_state.indexed_files:
#             st.caption(f"• {f}")
        
#         if st.button("🗑️ Clear All Data"):
#             st.session_state.rag_pipeline.vector_store.clear()
#             #st.session_state.messages = []
#             st.session_state.indexed_files = []
#             st.session_state.document_indexed = False
#             st.rerun()


# # Main UI
# st.title("📊 Financial Report AI Assistant")
# st.markdown("Upload your financial report and ask questions to get accurate insights.")

# # Example prompts
# if st.session_state.document_indexed:
#     st.subheader("💡 Example Questions")
#     col1, col2 = st.columns(2)
    
#     example_prompts = [
#         "What's the total revenue for 2024?",
#         "Show profit or loss for this period",
#         "Compare Q1 vs Q4 performance",
#         "Summarize key financial metrics"
#     ]
    
#     for i, prompt in enumerate(example_prompts):
#         col = col1 if i % 2 == 0 else col2
#         if col.button(f"📈 {prompt}", use_container_width=True, key=f"btn_{i}"):
#             st.session_state.messages.append({"role": "user", "content": prompt})
#             st.rerun()

# st.divider()

# # Chat interface
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# if prompt := st.chat_input("Ask about your financial report...", disabled=not st.session_state.document_indexed or not api_key):
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
#     with st.chat_message("user"):
#         st.markdown(prompt)
    
#     with st.chat_message("assistant"):
#         with st.spinner("Analyzing..."):
#             response = st.session_state.rag_pipeline.generate_response(prompt)
#             st.markdown(response)
    
#     st.session_state.messages.append({"role": "assistant", "content": response})

# if not st.session_state.document_indexed:
#     st.info("👆 Upload a financial report PDF to get started")