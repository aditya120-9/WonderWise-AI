try:
    # pydantic v2 separate package
    # type: ignore - optional package may not be installed in all environments
    from pydantic_settings import BaseSettings  # type: ignore
except Exception:
    # fallback to pydantic (v1 or when bundled)
    from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "WonderWise AI"
    SECRET_KEY: str = "change-this-secret-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: str = "http://127.0.0.1:5173,http://localhost:5173"
    REQUIRE_EMAIL_VERIFICATION: bool = False
    APP_BASE_URL: str = "http://127.0.0.1:5173"
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = ""
    RATE_LIMIT_REQUESTS: int = 120
    CHAT_RATE_LIMIT_REQUESTS: int = 10

    OLLAMA_MODEL: str = "qwen2.5:3b"
    OLLAMA_EMBEDDING_MODEL: str = "all-minilm"

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    RAG_MIN_DISTANCE: float = 1.2
    RAG_CACHE_TTL_SECONDS: int = 300
    LLM_TIMEOUT_SECONDS: int = 90
    OLLAMA_NUM_PREDICT: int = 120
    OLLAMA_KEEP_ALIVE: str = "5m"


settings = Settings()