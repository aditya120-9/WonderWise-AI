import time
from threading import Lock

from app.rag.chroma import collection, embedding_client
from app.config.settings import settings
from app.observability.metrics import metrics

_cache: dict[tuple[str, int, float], tuple[float, list[dict]]] = {}
_cache_lock = Lock()


def retrieve(query: str, n_results: int = 2, min_distance: float | None = None) -> list[dict]:
    """Retrieve relevant documents from Chroma.

    Keep n_results small to reduce prompt size and speed up travel queries.
    """
    n_results = max(1, min(int(n_results), 4))
    distance_limit = settings.RAG_MIN_DISTANCE if min_distance is None else min_distance
    cache_key = (query.strip().lower(), n_results, distance_limit)
    now = time.monotonic()
    with _cache_lock:
        cached = _cache.get(cache_key)
        if cached and now - cached[0] < settings.RAG_CACHE_TTL_SECONDS:
            metrics.increment("rag_cache_hits")
            return cached[1]

    started_at = time.perf_counter()
    try:
        query_embedding = embedding_client.embed_query(query)
    except Exception as e:
        print(f"RAG retrieval skipped: embedding error: {e}")
        return []

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    if not result or len(result.get("documents", [])) == 0:
        return []

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = (result.get("distances") or [[]])[0]
    retrievals = []
    for index, (docs, meta) in enumerate(zip(documents, metadatas)):
        distance = distances[index] if index < len(distances) else None
        if distance is not None and distance > distance_limit:
            continue
        retrievals.append({
            "document": docs,
            "metadata": meta or {},
            "distance": distance,
        })

    with _cache_lock:
        _cache[cache_key] = (time.monotonic(), retrievals)
    metrics.increment("rag_queries")
    metrics.observe("rag_duration_ms", (time.perf_counter() - started_at) * 1000)
    return retrievals

