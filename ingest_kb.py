import os
import faiss

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from config import (
    KB_DIR,
    FAISS_DIR,
    EMBEDDING_MODEL_NAME,
    EMBEDDING_DIMENSION,
)

print("Loading documents...")
documents = SimpleDirectoryReader(KB_DIR).load_data()

print("Setting local embedding model...")
Settings.embed_model = HuggingFaceEmbedding(
    model_name=EMBEDDING_MODEL_NAME
)

Settings.chunk_size = 1024
Settings.chunk_overlap = 50

print("Creating FAISS index...")
faiss_index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
vector_store = FaissVectorStore(faiss_index=faiss_index)

# ✅ THIS LINE WAS MISSING / MISPLACED
index = VectorStoreIndex.from_documents(
    documents,
    vector_store=vector_store
)

os.makedirs(FAISS_DIR, exist_ok=True)

# ✅ index is now defined, so this works
index.storage_context.persist(persist_dir=FAISS_DIR)

print("Knowledge base ingestion complete.")
