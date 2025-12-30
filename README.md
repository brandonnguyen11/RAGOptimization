# ============================================
# FILE: README.md
# ============================================
# 📊 Financial Report RAG Chatbot

AI-powered financial report analysis using RAG (Retrieval-Augmented Generation) to eliminate hallucinations and provide accurate, data-driven insights.

## 🚀 Features

- **Upload PDF Reports**: Process financial reports in PDF format
- **RAG Architecture**: Retrieval-Augmented Generation eliminates hallucinations
- **Dual API Support**: Choose between OpenAI or Groq
- **Vector Search**: ChromaDB for efficient semantic search
- **Interactive Chat**: Natural language Q&A interface
- **Example Prompts**: Quick-start questions for common queries

## 📦 Installation

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd financial-rag-chatbot
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys
Create a `.env` file:
```env
OPENAI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

## 🎯 Usage

### Run the Application
```bash
streamlit run app.py
```

### Using the App
1. Select your AI provider (OpenAI or Groq)
2. Enter your API key
3. Upload a financial report PDF
4. Ask questions or use example prompts
5. Get accurate, quantitative answers!

## 🏗️ Architecture

```
User Query
    ↓
Vector Store (ChromaDB)
    ↓
Retrieve Top-K Chunks
    ↓
Augment with Context
    ↓
LLM (OpenAI/Groq)
    ↓
Grounded Response
```

## 📁 Project Structure

```
financial-rag-chatbot/
├── app.py                    # Main Streamlit app
├── config.py                 # Configuration
├── src/
│   ├── document_processor.py # PDF processing
│   ├── vector_store.py       # ChromaDB operations
│   ├── llm_handler.py        # API calls
│   └── rag_pipeline.py       # RAG orchestration
├── utils/                    # Utilities
├── tests/                    # Unit tests
└── data/                     # Data directory
```

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Vector DB**: ChromaDB
- **LLMs**: OpenAI GPT-4 / Groq Llama 3.3
- **PDF**: PyPDF2

## 🧪 Testing

```bash
pytest tests/
```

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.
