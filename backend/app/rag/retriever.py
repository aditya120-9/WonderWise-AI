from app.rag.chroma import collection, embedding_client


def retrieve(query: str, n_results: int = 2) -> list[dict]:
    """Retrieve relevant documents from Chroma.

    Keep n_results small to reduce prompt size and speed up travel queries.
    """
    try:
        query_embedding = embedding_client.embed_query(query)
    except Exception as e:
        print(f"RAG retrieval skipped: embedding error: {e}")
        return []

    # Always cap n_results to avoid accidental prompt explosion
    n_results = max(1, min(int(n_results), 2))

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    if not result or len(result.get("documents", [])) == 0:
        return []

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    retrievals = []
    for docs, meta in zip(documents, metadatas):
        retrievals.append({
            "document": docs,
            "metadata": meta,
        })

    return retrievals

