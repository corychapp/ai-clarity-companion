from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Tuple, Dict

# Lazy singleton-ish
_client = None
_embedder = None

def _client_instance():
    global _client
    if _client is None:
        _client = Client(Settings(is_persistent=True, persist_directory=".chroma"))
    return _client

def _embedder_instance():
    global _embedder
    if _embedder is None:
        _embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
    return _embedder

def get_user_collection(user_id: str):
    client = _client_instance()
    name = f"notes_{user_id}"
    try:
        return client.get_collection(name, embedding_function=_embedder_instance())
    except Exception:
        return client.create_collection(name, embedding_function=_embedder_instance())

def add_note(user_id: str, note_id: str, text: str, meta: Dict):
    col = get_user_collection(user_id)
    col.add(documents=[text], ids=[note_id], metadatas=[meta])

def search_notes(user_id: str, query: str, k: int = 3) -> List[Tuple[str, Dict]]:
    col = get_user_collection(user_id)
    res = col.query(query_texts=[query], n_results=k)
    if not res["documents"]:
        return []
    return list(zip(res["documents"][0], res["metadatas"][0]))