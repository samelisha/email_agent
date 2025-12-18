# email_agent

📧 Local Email AI Agent (Offline RAG POC)
A fully local, email-driven AI agent that:
Monitors a Gmail inbox
Answers user questions using a local knowledge base
Uses FAISS + local embeddings
Uses a local LLM via Ollama
Supports live knowledge base updates without restart
Requires no OpenAI / cloud billing

🧠 Architecture Overview
Email Interface: Gmail (IMAP + SMTP)
Vector DB: FAISS (local)
Embeddings: sentence-transformers (local)
LLM: Ollama (local, e.g. qwen2.5:1.5b)
Memory: JSON files (per sender)
KB Reload: Automatic on file change

📁 Project Structure
email_agent_poc/
├── agent.py                # Core agent logic + KB hot-reload
├── email_listener.py       # Gmail polling & email handling
├── ingest_kb.py            # Build / rebuild FAISS index
├── kb_utils.py             # KB change detection
├── mailer.py               # SMTP email sender
├── memory_store.py         # Per-sender conversation memory
├── config.py               # Configuration
├── requirements.txt
├── .env                    # Gmail credentials (not committed)
├── kb/                     # Knowledge base files
│   └── faq.md
├── faiss_store/            # Persisted vector index
└── memory/                 # Conversation memory (JSON)

🧩 Dependencies

✅ System Requirements
Python 3.10+
macOS / Linux
Minimum 8 GB RAM (16 GB recommended)
Gmail account with App Password
Ollama installed and running

📦 Python Dependencies (requirements.txt)
numpy<2.0

llama-index==0.14.10
llama-index-vector-stores-faiss==0.5.1

sentence-transformers==2.6.1
faiss-cpu==1.7.4

ollama==0.1.8

imapclient==3.0.1
pyzmail36==1.0.5
python-dotenv==1.0.1

🐍 Environment Setup
1️⃣ Create virtual environment
python3 -m venv email_agent_py_env
source email_agent_py_env/bin/activate
2️⃣ Install dependencies
pip install -r requirements.txt

🔐 Gmail Setup (Required)
Generate Gmail App Password
Enable 2-Step Verification
Go to: https://myaccount.google.com/apppasswords
App → Mail
Device → Other
Name → email-agent-poc
Copy generated password
Create .env file
touch .env
GMAIL_ADDRESS=yourbot@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
⚠️ Do NOT remove spaces in the password
⚠️ Do NOT commit .env to Git

🤖 Ollama Setup (Local LLM)
Install Ollama (macOS)
Download and install:
https://ollama.com/download
Open the Ollama app (must be running).
Start Ollama server
ollama serve
Pull a lightweight model (recommended)
ollama pull qwen2.5:1.5b
Test it:
ollama run qwen2.5:1.5b

📚 Knowledge Base Setup
Add knowledge files under kb/:
mkdir kb
Example:
echo "Refunds are processed within 7 business days." > kb/faq.md
🧠 Build Vector Index (One-Time)
python ingest_kb.py
Expected output:
Loading documents...
Setting local embedding model...
Creating FAISS index...
Knowledge base ingestion complete.
This creates:
faiss_store/

▶️ Run the Email Agent
python email_listener.py
Expected log:
📬 Email agent started. Polling inbox every 5 minutes...

✉️ How It Works (Runtime)
User sends email to bot address
Agent:
Filters system/no-reply emails
Retrieves relevant KB context
Generates answer using local LLM
Adds auto-generated disclaimer
Reply is sent via Gmail SMTP
Conversation memory is stored per sender
🔄 Live Knowledge Base Updates (No Restart)
While the agent is running:
echo "New policy added today." >> kb/faq.md
Next user email triggers:
🔄 KB change detected. Rebuilding index...
✔ No restart
✔ No downtime

🎯 POC Highlights
✔ Fully local AI
✔ Zero cloud billing
✔ Email-based UX
✔ Live KB updates
✔ Privacy-friendly
✔ Enterprise-style RAG architecture

🚀 Future Enhancements
Admin KB reload via email
Confidence thresholding
Gmail labels (Answered, Ignored)
Web UI for KB updates
Docker deployment

📌 One-Line Summary
A fully local, email-driven AI agent that answers questions using a live-updating knowledge base with zero cloud dependency.
