import os
from dotenv import load_dotenv
load_dotenv()

# ======================
# Gmail Configuration
# ======================
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ======================
# Paths
# ======================
KB_DIR = "kb"
MEMORY_DIR = "memory"
FAISS_DIR = "faiss_store"

# ======================
# Conversation Memory
# ======================
MAX_MEMORY_MESSAGES = 8

# ======================
# Local LLM (Ollama)
# ======================
#OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3")
OLLAMA_MODEL = "qwen2.5:1.5b"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# ======================
# Embeddings (Local)
# ======================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384
