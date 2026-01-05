# ============================================
# IMPORTS
# ============================================
import streamlit as st
from src.document_processor import extract_text_from_pdf, chunk_text
from src.vector_store import VectorStore
from src.rag_pipeline import RAGPipeline
from config import *
import time

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Financial Intelligence",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS STYLES WITH DEBUG BORDERS
# ============================================
st.markdown("""
<style>
    /* ===== FONT IMPORT ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400..700;1,400..700&display=swap');
    
    /* ===== GLOBAL STYLES ===== */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ===== MAIN BACKGROUND ===== */
    .stApp {
        padding-top: 0 !important;
        background: #f8f8f6;
    }
    
    /* ===== NAVIGATION BAR ===== */
    .nav-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: #ffffff;
        border-bottom: 1px solid #e5e5e5;
        padding: 1rem 0; /* Remove side padding */
        border: 3px solid darkblue; /* DEBUG BORDER */
        margin-bottom: 7rem;
        height: 72px;
    }
    
    .nav-bar-inner {
        max-width: 1200px; /* Same as your main content */
        margin: 0 auto; /* Center the container */
        padding: 0 2rem; /* Space on sides */
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 3px solid purple; /* DEBUG BORDER */
    }
            
    /* ===== NAV LOGO/COMPANY NAME ===== */
    .nav-logo {
        font-size: 18px;
        font-family: 'Libre Baskerville', serif;
        font-weight: 700;
        color: #1a1a1a;
        border: 3px solid darkred; /* DEBUG BORDER */
        padding: 0.5rem;
    }
    
    /* ===== NAV LINKS CONTAINER ===== */
    .nav-links {
        display: flex;
        gap: 2rem;
        align-items: center;
        border: 3px solid darkgreen; /* DEBUG BORDER */
        padding: 0.5rem;
    }
    
    /* ===== NAV LINK ITEMS ===== */
    .nav-link {
        color: #666666;
        text-decoration: none;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .nav-link:hover {
        color: #1a1a1a;
    }
    
    /* ===== CONTENT CONTAINER ===== */
    .main {
        padding-top: 0 !important;
        border: 3px solid red; /* DEBUG BORDER */
    }

    .main .block-container {
        padding-top: 72px !important;
        margin-top: 0 !important;
        padding-bottom: 2rem;
        max-width: 1200px;
        border: 3px solid blue; /* DEBUG BORDER */
    }
    
    /* ===== HERO SECTION (TOP TITLE AREA) ===== */
    .hero-section {
        margin-top: 40px;
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 2rem;
        border: 3px solid orange; /* DEBUG BORDER */
    }
    
    /* ===== HERO TITLE (GRADIENT TEXT) ===== */
    .hero-title {
        font-family: 'Libre Baskerville', serif !important;
        font-size: 35px !important;
        font-weight: 300 !important;
        margin-bottom: 0.5rem;
        letter-spacing: 0.01em;
        border: 3px solid purple; /* DEBUG BORDER */
    }
    
    /* ===== HERO SUBTITLE ===== */
    .hero-subtitle {
        font-size: 1.2rem;
        color: #8b9dc3;
        font-weight: 400;
        margin-top: 0;
        border: 3px solid pink; /* DEBUG BORDER */
    }
    
    /* ===== UPLOAD CONTAINER (GLASSMORPHIC CARD) ===== */
    .upload-container {
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(10px);
        border: 3px solid yellow; /* DEBUG BORDER */
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 600px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    /* ===== UPLOAD CONTAINER HOVER STATE ===== */
    .upload-container:hover {
        border: 3px solid lime; /* DEBUG BORDER */
        transform: translateY(-2px);
    }
    
    /* ===== ALL BUTTONS (GRADIENT STYLE) ===== */
    .stButton>button {
        background: linear-gradient(135deg, #00f5a0 0%, #00d9f5 100%);
        color: #0a0e27;
        border: 3px solid cyan; /* DEBUG BORDER */
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin: 0.25rem 0;
    }
    
    /* ===== BUTTON HOVER STATE ===== */
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 40px rgba(0, 245, 160, 0.3);
        border: 3px solid magenta; /* DEBUG BORDER */
    }
    
    /* ===== EXAMPLE PROMPT BUTTONS (DARKER STYLE) ===== */
    .example-btn {
        background: rgba(26, 31, 58, 0.8) !important;
        color: #00f5a0 !important;
        border: 3px solid gold !important; /* DEBUG BORDER */
    }
    
    /* ===== EXAMPLE BUTTON HOVER ===== */
    .example-btn:hover {
        background: rgba(0, 245, 160, 0.1) !important;
        border: 3px solid darkgreen !important; /* DEBUG BORDER */
    }
    
    /* ===== CHAT MESSAGE BUBBLES ===== */
    .stChatMessage {
        background: rgba(26, 31, 58, 0.4);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 3px solid teal; /* DEBUG BORDER */
    }
    
    /* ===== CHAT MESSAGE TEXT COLOR ===== */
    [data-testid="stChatMessageContent"] {
        color: #e8ecf3;
        border: 3px solid navy; /* DEBUG BORDER */
    }
    
    /* ===== USER MESSAGE (GRADIENT BACKGROUND) ===== */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: linear-gradient(135deg, rgba(0, 245, 160, 0.1) 0%, rgba(0, 217, 245, 0.1) 100%);
        border: 3px solid brown; /* DEBUG BORDER */
    }
    
    /* ===== CHAT INPUT BOX ===== */
    .stChatInput {
        background: rgba(26, 31, 58, 0.8);
        border: 3px solid olive; /* DEBUG BORDER */
        border-radius: 16px;
        color: #e8ecf3;
    }
    
    /* ===== CHAT INPUT FOCUS STATE ===== */
    .stChatInput:focus {
        border: 3px solid hotpink; /* DEBUG BORDER */
        box-shadow: 0 0 0 2px rgba(0, 245, 160, 0.1);
    }
    
    /* ===== TEXT INPUT FIELDS ===== */
    .stTextInput>div>div>input {
        background: rgba(26, 31, 58, 0.8);
        border: 3px solid crimson; /* DEBUG BORDER */
        border-radius: 12px;
        color: #e8ecf3;
        padding: 0.75rem 1rem;
    }
    
    /* ===== TEXT INPUT FOCUS STATE ===== */
    .stTextInput>div>div>input:focus {
        border: 3px solid coral; /* DEBUG BORDER */
        box-shadow: 0 0 0 2px rgba(0, 245, 160, 0.1);
    }
    
    /* ===== SELECT BOX (DROPDOWN) ===== */
    .stSelectbox>div>div {
        background: rgba(26, 31, 58, 0.8);
        border: 3px solid indigo; /* DEBUG BORDER */
        border-radius: 12px;
        color: #e8ecf3;
    }
    
    /* ===== FILE UPLOADER AREA ===== */
    [data-testid="stFileUploader"] {
        background: rgba(26, 31, 58, 0.4);
        border: 3px dashed tomato; /* DEBUG BORDER */
        border-radius: 16px;
        padding: 2rem;
    }
    
    /* ===== FILE UPLOADER HOVER STATE ===== */
    [data-testid="stFileUploader"]:hover {
        border: 3px dashed salmon; /* DEBUG BORDER */
        background: rgba(26, 31, 58, 0.6);
    }
    
    /* ===== SUCCESS MESSAGES ===== */
    .stSuccess {
        background: rgba(0, 245, 160, 0.1);
        border: 3px solid springgreen; /* DEBUG BORDER */
        border-radius: 12px;
        color: #00f5a0;
    }
    
    /* ===== INFO MESSAGES ===== */
    .stInfo {
        background: rgba(0, 217, 245, 0.1);
        border: 3px solid skyblue; /* DEBUG BORDER */
        border-radius: 12px;
        color: #00d9f5;
    }
    
    /* ===== DIVIDER LINE ===== */
    hr {
        border: 3px solid silver; /* DEBUG BORDER */
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 245, 160, 0.3), transparent);
        margin: 2rem 0;
    }
    
    /* ===== LOADING SPINNER ===== */
    .stSpinner>div {
        border-top-color: #00f5a0 !important;
        border: 3px solid violet; /* DEBUG BORDER */
    }
    
    /* ===== EXPANDER HEADER ===== */
    .streamlit-expanderHeader {
        background: rgba(26, 31, 58, 0.6);
        border-radius: 12px;
        color: #e8ecf3;
        border: 3px solid maroon; /* DEBUG BORDER */
    }
    
    /* ===== EXPANDER CONTENT ===== */
    .streamlit-expanderContent {
        border: 3px solid chocolate; /* DEBUG BORDER */
    }
    
    /* ===== CUSTOM METRIC CARDS ===== */
    .metric-card {
        background: rgba(26, 31, 58, 0.6);
        border: 3px solid sienna; /* DEBUG BORDER */
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    /* ===== METRIC CARD HOVER STATE ===== */
    .metric-card:hover {
        border: 3px solid tan; /* DEBUG BORDER */
        transform: translateY(-4px);
        box-shadow: 0 10px 40px rgba(0, 245, 160, 0.1);
    }
    
    /* ===== SIDEBAR BACKGROUND ===== */
    [data-testid="stSidebar"] {
        background: rgba(10, 14, 39, 0.95);
        backdrop-filter: blur(10px);
        border: 3px solid wheat; /* DEBUG BORDER */
    }
    
    /* ===== SIDEBAR TEXT COLOR ===== */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #8b9dc3;
        border: 3px solid plum; /* DEBUG BORDER */
    }
    
    /* ===== COLUMNS (TWO COLUMN LAYOUT) ===== */
    [data-testid="column"] {
        border: 3px solid orchid; /* DEBUG BORDER */
        padding: 0.5rem;
    }
    
    /* ===== MARKDOWN CONTAINERS ===== */
    [data-testid="stMarkdownContainer"] {
        border: 3px solid khaki; /* DEBUG BORDER */
    }
    
    /* ===== SCROLLBAR TRACK ===== */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    /* ===== SCROLLBAR BACKGROUND ===== */
    ::-webkit-scrollbar-track {
        background: rgba(26, 31, 58, 0.4);
    }
    
    /* ===== SCROLLBAR THUMB ===== */
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 245, 160, 0.3);
        border-radius: 4px;
    }
    
    /* ===== SCROLLBAR THUMB HOVER ===== */
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 245, 160, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'document_indexed' not in st.session_state:
    st.session_state.document_indexed = False
if 'show_config' not in st.session_state:
    st.session_state.show_config = False

# ============================================
# NAVIGATION BAR
# ============================================
st.markdown("""
<div class="nav-bar">
    <div class="nav-bar-inner">
        <div class="nav-logo">rago</div>
        <div class="nav-links">
            <span class="nav-link">Features</span>
            <span class="nav-link">About</span>
            <span class="nav-link">Pricing</span>
            <span class="nav-link">Contact</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# HERO SECTION (TOP TITLE AND SUBTITLE)
# ============================================
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">How can I help you?</h1>
</div>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION EXPANDER (API SETTINGS)
# ============================================
# with st.expander("⚙️ Configuration", expanded=not st.session_state.document_indexed):
#     # --- Layout: Two Columns ---
#     col1, col2 = st.columns(2)
    
#     # --- Element: API Provider Dropdown ---
#     with col1:
#         api_choice = st.selectbox("AI Provider", ["OpenAI", "Groq"], label_visibility="collapsed")
#         st.caption("Select AI Provider")
    
#     # --- Element: API Key Input ---
#     with col2:
#         api_key = st.text_input("API Key", type="password", label_visibility="collapsed", placeholder="Enter your API key")
#         st.caption("API Key")

# ============================================
# UPLOAD SECTION (EMPTY STATE - NO DOCUMENT)
# ============================================
if not st.session_state.document_indexed:
    
    # --- Element: Upload Container Card ---
    st.markdown("""
    <div class="upload-container">
        <h3 style="color: #00f5a0; margin-bottom: 1rem;">📄 Upload Your Financial Report</h3>
        <p style="color: #8b9dc3; margin-bottom: 1.5rem;">Upload a PDF to begin your analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Element: File Uploader ---
    uploaded_file = st.file_uploader("", type=['pdf'], label_visibility="collapsed")
    
    # --- Logic: Process Uploaded File ---
    if uploaded_file and api_key:
        # Show processing spinner
        with st.spinner("🔮 Processing your document..."):
            # Progress bar animation
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Extract text from PDF
            text = extract_text_from_pdf(uploaded_file)
            
            # Chunk text into pieces
            chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
            
            # Create vector store
            vector_store = VectorStore()
            vector_store.index_chunks(chunks, uploaded_file.name)
            
            # Initialize RAG pipeline
            st.session_state.rag_pipeline = RAGPipeline(
                vector_store=vector_store,
                api_choice=api_choice,
                api_key=api_key
            )
            
            # Update state
            st.session_state.document_indexed = True
            
            # Show success message
            st.success(f"✨ Successfully indexed {len(chunks)} sections from your report")
            time.sleep(1)
            st.rerun()

# ============================================
# CHAT INTERFACE (DOCUMENT LOADED STATE)
# ============================================
if st.session_state.document_indexed:
    
    # --- Header: Quick Insights ---
    st.markdown("### 💡 Quick Insights")
    
    # --- Layout: Two Columns for Example Buttons ---
    col1, col2 = st.columns(2)
    
    # --- Element: Example Prompt Buttons ---
    example_prompts = [
        ("📈", "What's the total revenue?"),
        ("💰", "Show profit or loss"),
        ("📊", "Compare quarterly performance"),
        ("🎯", "Key financial metrics")
    ]
    
    # Create buttons in alternating columns
    for i, (emoji, prompt) in enumerate(example_prompts):
        col = col1 if i % 2 == 0 else col2
        if col.button(f"{emoji} {prompt}", key=f"ex_{i}", use_container_width=True):
            # Add prompt to messages
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.rerun()
    
    # --- Element: Divider ---
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- Section: Chat Message History ---
    for message in st.session_state.messages:
        # Display each message with custom avatar
        with st.chat_message(message["role"], avatar="💎" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])
    
    # --- Element: Chat Input Box ---
    if prompt := st.chat_input("Ask anything about your financial report...", key="chat_input"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Generate AI response
        with st.chat_message("assistant", avatar="💎"):
            with st.spinner("Analyzing..."):
                # Call RAG pipeline
                response = st.session_state.rag_pipeline.generate_response(prompt)
                st.markdown(response)
        
        # Add AI response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # --- Element: Clear/Reset Button ---
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Start New Analysis", use_container_width=False):
        # Reset all session state
        st.session_state.messages = []
        st.session_state.document_indexed = False
        st.session_state.rag_pipeline = None
        st.rerun()

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #8b9dc3; font-size: 0.9rem; border: 3px solid turquoise;">
    <p>Powered by RAG Technology • Secure • Private</p>
</div>
""", unsafe_allow_html=True)