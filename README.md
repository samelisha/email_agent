# Email Agent

📧 Local Email AI Agent (Offline RAG POC)

A fully local, email-driven AI agent that monitors a Gmail inbox and answers user questions using a local knowledge base—all without cloud dependencies.

## Features

- ✅ Fully local AI (no OpenAI/cloud billing)
- ✅ Monitors Gmail inbox via IMAP
- ✅ Answers questions using a local knowledge base (RAG)
- ✅ FAISS vector database + local embeddings
- ✅ Local LLM via Ollama
- ✅ Live knowledge base updates without restart
- ✅ Per-sender conversation memory
- ✅ Privacy-friendly & enterprise-ready

## Architecture Overview

| Component | Technology |
|-----------|-----------|
| Email Interface | Gmail (IMAP + SMTP) |
| Vector DB | FAISS (local) |
| Embeddings | sentence-transformers (local) |
| LLM | Ollama (local, e.g. qwen2.5:1.5b) |
| Memory | JSON files (per sender) |
| KB Reload | Automatic on file change |

## Project Structure

```
email_agent/
├── agent.py                # Core agent logic + KB hot-reload
├── email_listener.py       # Gmail polling & email handling
├── ingest_kb.py            # Build / rebuild FAISS index
├── kb_utils.py             # KB change detection
├── mailer.py               # SMTP email sender
├── memory_store.py         # Per-sender conversation memory
├── config.py               # Configuration
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .env                    # Gmail credentials (not committed)
├── kb/                     # Knowledge base files
│   └── faq.md
├── faiss_store/            # Persisted vector index
└── memory/                 # Conversation memory (JSON)
```

## Prerequisites

### System Requirements

- Python 3.10+
- macOS or Linux
- Minimum 8 GB RAM (16 GB recommended)
- Gmail account with App Password
- Ollama installed and running

### Python Dependencies

```
numpy<2.0
llama-index==0.14.10
llama-index-vector-stores-faiss==0.5.1
sentence-transformers==2.6.1
faiss-cpu==1.7.4
ollama==0.1.8
imapclient==3.0.1
pyzmail36==1.0.5
python-dotenv==1.0.1
```

## Setup Instructions

### 1. Create Python Virtual Environment

```bash
python3 -m venv email_agent_py_env
source email_agent_py_env/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gmail

1. **Enable 2-Step Verification**
   - Go to https://myaccount.google.com/security

2. **Generate App Password**
   - Visit https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Name it "email-agent-poc"
   - Copy the generated password

3. **Create `.env` file**

```bash
touch .env
```

Add to `.env`:
```
GMAIL_ADDRESS=yourbot@gmail.com
GMAIL_APP_PASSWORD=abcd efgh ijkl mnop
```

⚠️ **Important:**
- Do NOT remove spaces in the password
- Do NOT commit `.env` to Git

### 4. Set Up Ollama (Local LLM)

1. **Install Ollama**
   - Download from https://ollama.com/download

2. **Start Ollama Server**
   ```bash
   ollama serve
   ```

3. **Pull a Lightweight Model**
   ```bash
   ollama pull qwen2.5:1.5b
   ```

4. **Test the Model**
   ```bash
   ollama run qwen2.5:1.5b
   ```

### 5. Set Up Knowledge Base

1. **Add Knowledge Files**
   ```bash
   mkdir -p kb
   echo "Refunds are processed within 7 business days." > kb/faq.md
   ```

2. **Build Vector Index** (one-time)
   ```bash
   python ingest_kb.py
   ```

   Expected output:
   ```
   Loading documents...
   Setting local embedding model...
   Creating FAISS index...
   Knowledge base ingestion complete.
   ```

## Running the Agent

Start the email agent:

```bash
python email_listener.py
```

Expected log output:
```
📬 Email agent started. Polling inbox every 5 minutes...
```

## How It Works

### Runtime Flow

1. User sends email to bot address
2. Agent:
   - Filters system/no-reply emails
   - Retrieves relevant KB context using FAISS
   - Generates answer using local LLM
   - Adds auto-generated disclaimer
   - Sends reply via Gmail SMTP
   - Stores conversation memory per sender

### Live Knowledge Base Updates

While the agent is running, update your KB:

```bash
echo "New policy added today." >> kb/faq.md
```

Next time a user sends an email:
- 🔄 KB change detected. Rebuilding index...
- ✔ No restart required
- ✔ No downtime

## Future Enhancements

- 🔧 Admin KB reload via email
- 📊 Confidence thresholding for responses
- 🏷️ Gmail labels (Answered, Ignored)
- 🌐 Web UI for KB updates
- 🐳 Docker deployment

## Summary

A fully local, email-driven AI agent that answers questions using a live-updating knowledge base with zero cloud dependency.

