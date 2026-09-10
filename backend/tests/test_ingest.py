from app.rag.ingest import chunk_text


def test_chunk_text_preserves_overlap_and_usable_chunk_size():
    chunks = chunk_text(" ".join(f"word{index}" for index in range(20)), chunk_size=8, overlap=2)

    assert len(chunks) == 4
    assert chunks[0].split()[-2:] == chunks[1].split()[:2]