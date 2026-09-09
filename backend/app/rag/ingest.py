from pathlib import Path
from pypdf import PdfReader
from app.rag.chroma import collection, embedding_client

BASE_DIR = Path(__file__).resolve().parents[2]
PDF_DIR = BASE_DIR / "knowledge"


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)
    return "\n\n".join(text)


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start : start + chunk_size])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def ingest_documents() -> None:
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError("No PDF documents found in the knowledge directory.")

    for pdf_path in pdf_files:
        text = extract_pdf_text(pdf_path)
        chunks = chunk_text(text)
        ids = [f"{pdf_path.stem}-{idx}" for idx in range(len(chunks))]
        metadatas = [{"source": pdf_path.name, "chunk_index": idx} for idx in range(len(chunks))]

        if embedding_client is None:
            raise RuntimeError(
                "Ollama embedding client is not configured. Pull and run a supported Ollama embedding model (for example, all-minilm) and ensure the Ollama server exposes /api/embed."
            )

        try:
            embeddings = embedding_client.embed_documents(chunks)
        except Exception as e:
            raise RuntimeError(
                "Embedding service unavailable. Verify that your Ollama server supports the embed endpoint and that the configured embedding model exists locally."
            ) from e

        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    collection.persist()


if __name__ == "__main__":
    ingest_documents()
