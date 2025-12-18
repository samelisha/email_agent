import os
import subprocess
from typing import Optional

from llama_index.core import (
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from memory_store import load_memory, save_memory
from config import (
    FAISS_DIR,
    OLLAMA_MODEL,
    EMBEDDING_MODEL_NAME,
)
from kb_utils import get_kb_last_modified


# =====================================================
# Force LOCAL embeddings (prevents OpenAI fallback)
# =====================================================

Settings.embed_model = HuggingFaceEmbedding(
    model_name=EMBEDDING_MODEL_NAME
)


# =====================================================
# Local LLM (Ollama)
# =====================================================

llm = Ollama(
    model=OLLAMA_MODEL,
    temperature=0.2,
    request_timeout=120,
    options={
        "num_ctx": 2048,
        "num_predict": 256,
    },
)


# =====================================================
# KB / Index state (cached in memory)
# =====================================================

_index = None  # type: Optional[object]
_last_kb_version: float = 0.0


# =====================================================
# Index management
# =====================================================

def _load_index():
    """Load FAISS index from disk via LlamaIndex storage."""
    global _index

    if not os.path.exists(FAISS_DIR):
        raise RuntimeError(
            f"FAISS directory '{FAISS_DIR}' not found. "
            "Run `python ingest_kb.py` first."
        )

    storage_context = StorageContext.from_defaults(
        persist_dir=FAISS_DIR
    )
    _index = load_index_from_storage(storage_context)
    print("✅ Knowledge base loaded into memory")


def _rebuild_index():
    """Rebuild FAISS index by re-running ingestion."""
    print("🔄 KB change detected. Rebuilding index...")
    subprocess.run(
        ["python", "ingest_kb.py"],
        check=True,
    )
    _load_index()


def _get_index():
    """Return a valid index, reloading if KB changed."""
    global _last_kb_version

    current_kb_version = get_kb_last_modified()

    if _index is None:
        _load_index()
        _last_kb_version = current_kb_version

    elif current_kb_version > _last_kb_version:
        _rebuild_index()
        _last_kb_version = current_kb_version

    return _index


# =====================================================
# Public API (used by email_listener.py)
# =====================================================

def handle_question(sender: str, question: str) -> str:
    """
    Main agent entry point.
    - Reloads KB if needed
    - Retrieves context
    - Uses local LLM to answer
    - Stores per-sender memory
    """

    index = _get_index()

    query_engine = index.as_query_engine(
        similarity_top_k=3,
        llm=llm,
    )

    memory = load_memory(sender)

    history_text = "\n".join(
        f"{m['role']}: {m['content']}"
        for m in memory
    )

    prompt = f"""
You are a helpful email support assistant.

Conversation history:
{history_text}

User question:
{question}

Instructions:
- Answer clearly and professionally
- Be concise
- If unsure, say you will follow up
"""

    response = query_engine.query(prompt).response

    # Update memory
    memory.append({"role": "user", "content": question})
    memory.append({"role": "assistant", "content": response})
    save_memory(sender, memory)

    return response
