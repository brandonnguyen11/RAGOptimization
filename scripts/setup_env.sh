# ============================================
# FILE: scripts/setup_env.sh
# ============================================
#!/bin/bash

# Setup script for Financial RAG Chatbot

echo "Setting up Financial RAG Chatbot..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data/uploads
mkdir -p data/sample

echo "Setup complete! Run 'streamlit run app.py' to start."