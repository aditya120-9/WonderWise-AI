try:
    # langchain_ollama is an optional dependency; silence editor/type-checker import warnings
    from langchain_ollama import ChatOllama  # type: ignore[import]
except Exception:  # pragma: no cover - fallback when package not installed
    class ChatOllama:  # minimal fallback to avoid import errors in editors
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "langchain_ollama is not installed. Install it to use Ollama ChatLlama client."
            )

from app.config.settings import settings

# Keep local responses fast enough for streaming while improving readability and travel quality.
llm = ChatOllama(
    model=settings.OLLAMA_MODEL,
    base_url=settings.OLLAMA_BASE_URL,
    temperature=0.3,
    top_p=0.85,
    streaming=True,
    repeat_penalty=1.06,
    num_predict=settings.OLLAMA_NUM_PREDICT,
    keep_alive=settings.OLLAMA_KEEP_ALIVE,
)

