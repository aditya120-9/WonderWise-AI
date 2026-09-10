from app.rag import retriever


def test_retrieve_filters_low_relevance_documents(monkeypatch):
    class FakeEmbeddingClient:
        def embed_query(self, query):
            return [0.1, 0.2]

    monkeypatch.setattr(retriever, "embedding_client", FakeEmbeddingClient())
    monkeypatch.setattr(
        retriever.collection,
        "query",
        lambda **kwargs: {
            "documents": [["useful", "unrelated"]],
            "metadatas": [[{"source": "useful.pdf"}, {"source": "unrelated.pdf"}]],
            "distances": [[0.4, 1.8]],
        },
    )

    results = retriever.retrieve("Jaipur itinerary", n_results=2, min_distance=1.2)

    assert len(results) == 1
    assert results[0]["metadata"]["source"] == "useful.pdf"
    assert results[0]["distance"] == 0.4