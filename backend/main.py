import asyncio
import logging
import time
import uuid
from urllib.request import urlopen

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.api.chat import router as chat_router
from app.api.auth import router as auth_router
from app.api.conversations import router as conversations_router
from app.api.websocket import router as ws_router
from app.config.settings import settings
from app.database.database import SessionLocal
from app.observability.metrics import metrics
from app.security.rate_limit import allow_request

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("wonderwise.api")

app = FastAPI(title="WonderWise AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(auth_router)
app.include_router(conversations_router)
app.include_router(ws_router)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    client_host = request.client.host if request.client else "unknown"
    path = request.url.path
    if path not in {"/", "/health", "/ready", "/metrics"}:
        limit = settings.CHAT_RATE_LIMIT_REQUESTS if path in {"/chat", "/ws/chat"} else settings.RATE_LIMIT_REQUESTS
        allowed, retry_after = allow_request(f"http:{client_host}:{path}", limit)
        if not allowed:
            return JSONResponse(
                status_code=429,
                headers={"Retry-After": str(retry_after)},
                content={"error": {"code": "RATE_LIMITED", "message": "Too many requests. Please try again later."}},
            )
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    started_at = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        logger.exception("Unhandled request error request_id=%s path=%s", request_id, request.url.path)
        response = JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred.",
                    "request_id": request_id,
                }
            },
        )

    elapsed_ms = (time.perf_counter() - started_at) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_id=%s method=%s path=%s status=%s duration_ms=%.2f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The request contains invalid data.",
                "details": jsonable_encoder(exc.errors()),
            }
        },
    )

@app.get("/")
async def root():
    return {
        "status": "running"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    database_ready, ollama_ready = await asyncio.gather(
        asyncio.to_thread(_check_database),
        asyncio.to_thread(_check_ollama),
    )
    checks = {"database": database_ready, "ollama": ollama_ready}
    status_code = 200 if all(checks.values()) else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "ready" if status_code == 200 else "not_ready", "checks": checks},
    )


@app.get("/metrics")
async def metrics_endpoint():
    return {"metrics": metrics.snapshot()}


def _check_database() -> bool:
    session = SessionLocal()
    try:
        session.execute(text("SELECT 1"))
        return True
    except Exception:
        logger.exception("Database readiness check failed")
        return False
    finally:
        session.close()


def _check_ollama() -> bool:
    try:
        with urlopen(f"{settings.OLLAMA_BASE_URL}/api/tags", timeout=2) as response:
            return response.status == 200
    except Exception:
        logger.warning("Ollama readiness check failed")
        return False
