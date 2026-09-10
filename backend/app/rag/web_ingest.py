"""Index approved public web pages as source-backed travel context."""

from html.parser import HTMLParser
import hashlib
from urllib.request import Request, urlopen

from app.rag.chroma import collection, embedding_client
from app.rag.ingest import chunk_text


class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts: list[str] = []
        self._ignored = 0

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "nav", "footer", "header"}:
            self._ignored += 1

    def handle_endtag(self, tag):
        if tag in {"script", "style", "nav", "footer", "header"} and self._ignored:
            self._ignored -= 1

    def handle_data(self, data):
        if not self._ignored and data.strip():
            self.parts.append(data.strip())


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": "WonderWiseBot/1.0"})
    try:
        with urlopen(request, timeout=20) as response:
            parser = TextExtractor()
            parser.feed(response.read().decode("utf-8", errors="ignore"))
    except Exception as error:
        raise RuntimeError(
            f"Could not securely fetch source {url}. Download it manually and place the reviewed file in knowledge/."
        ) from error
    return " ".join(parser.parts)


def ingest_urls(sources: dict[str, str]) -> int:
    """Ingest a mapping of source URL to publisher label."""
    total_chunks = 0
    for url, publisher in sources.items():
        chunks = chunk_text(fetch_text(url), chunk_size=500, overlap=80)
        if not chunks:
            continue
        collection.upsert(
            documents=chunks,
            ids=[
                f"web-{hashlib.sha256(url.encode()).hexdigest()[:16]}-{index}"
                for index in range(len(chunks))
            ],
            metadatas=[
                {
                    "source": publisher,
                    "url": url,
                    "source_type": "web",
                    "chunk_index": index,
                }
                for index in range(len(chunks))
            ],
            embeddings=embedding_client.embed_documents(chunks),
        )
        total_chunks += len(chunks)
    return total_chunks