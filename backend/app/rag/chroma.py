from pathlib import Path
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
from langchain_ollama import OllamaEmbeddings

from app.config.settings import settings

BASE_DIR = Path(__file__).resolve().parents[2]
PERSIST_DIR = BASE_DIR / "chroma"
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

client = Client(
    Settings(
        chroma_api_impl="chromadb.api.rust.RustBindingsAPI",
        persist_directory=str(PERSIST_DIR),
    )
)

chroma_embedding_function = OllamaEmbeddingFunction(
    url=settings.OLLAMA_BASE_URL,
    model_name=settings.OLLAMA_EMBEDDING_MODEL,
)

langchain_embedding_client = OllamaEmbeddings(
    model=settings.OLLAMA_EMBEDDING_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
)

# Expose the embedding client for RAG and ingestion use
embedding_client = langchain_embedding_client

try:
    collection = client.get_or_create_collection(
        name="wonderwise_travel",
        embedding_function=chroma_embedding_function,
    )
except Exception:
    collection = client.get_or_create_collection(name="wonderwise_travel")
