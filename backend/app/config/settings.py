try:
    # pydantic v2 separate package
    # type: ignore - optional package may not be installed in all environments
    from pydantic_settings import BaseSettings  # type: ignore
except Exception:
    # fallback to pydantic (v1 or when bundled)
    from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "WonderWise AI"

    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_EMBEDDING_MODEL: str = "all-minilm"

    OLLAMA_BASE_URL: str = "http://localhost:11434"


settings = Settings()