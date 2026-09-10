# WonderWise AI

Privacy-focused AI travel planning with local LLM inference, retrieval-augmented generation, and real-time streaming.

WonderWise AI is a full-stack travel assistant built with FastAPI, React, TypeScript, Ollama, ChromaDB, SQLite, and WebSockets. It supports authenticated users, private conversations, source-aware responses, latency monitoring, rate limiting, and Docker deployment.

> **Data integrity:** The assistant does not invent current fares, prices, availability, or schedules. Exact travel data requires reviewed documents in `knowledge/` or a configured live provider integration. Without verified sources, responses clearly label prices as not verified.

## Highlights

- Local `qwen2.5:3b` inference through Ollama for privacy and offline control.
- WebSocket token streaming with cancellation and reconnect handling.
- ChromaDB retrieval with chunking, similarity filtering, caching, and source citations.
- JWT authentication, Argon2 password hashing, conversation ownership, reset tokens, and optional email verification.
- Structured travel responses with confidence labels and server-side protection against unsupported currency claims.
- Rate limiting, request IDs, health/readiness checks, latency metrics, Docker Compose, and GitHub Actions CI.

## Stack

| Layer | Technologies |
| --- | --- |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS, Axios, Framer Motion |
| Backend | Python 3.12+, FastAPI, Uvicorn, SQLAlchemy, Pydantic |
| AI | Ollama, LangChain, ChromaDB, retrieval-augmented generation |
| Storage | SQLite for local conversations, ChromaDB for vector search |
| Delivery | Docker, Docker Compose, Nginx, GitHub Actions |

## Project Structure

```text
wonderwise ai/
├── backend/
│   ├── app/
│   │   ├── api/              # Chat, auth, conversations, WebSocket routes
│   │   ├── auth/             # JWT and password hashing
│   │   ├── config/           # Environment-backed settings
│   │   ├── database/         # SQLAlchemy models and database setup
│   │   ├── llm/              # Ollama client
│   │   ├── observability/    # In-process metrics
│   │   ├── rag/              # Chroma retrieval and ingestion
│   │   ├── schemas/          # Request and response models
│   │   ├── security/         # Rate limiting
│   │   └── services/         # Chat, streaming, parsing, grounding
│   ├── scripts/              # Benchmarking and source ingestion
│   ├── Dockerfile
│   └── main.py
├── frontend/frontend/
│   ├── src/
│   │   ├── components/       # Chat and layout UI
│   │   ├── hooks/            # Chat and WebSocket state
│   │   ├── pages/            # Auth, dashboard, and chat views
│   │   └── services/         # API, auth, conversation, and socket clients
│   ├── Dockerfile
│   └── nginx.conf
├── knowledge/                # Reviewed travel documents
├── docker-compose.yml
├── DEPLOYMENT.md
└── run-dev.ps1
```

## Local Setup

### Prerequisites

- Python 3.12+
- Node.js 18+
- Ollama
- Models: `qwen2.5:3b` and `all-minilm`

### Install

From the repository root:

```powershell
cd backend
python -m venv .venv
..\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-phase2.txt

cd ..\frontend\frontend
npm install
```

Start Ollama in another terminal:

```powershell
ollama pull qwen2.5:3b
ollama pull all-minilm
ollama serve
```

### Run Development Services

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\run-dev.ps1
```

Or start manually:

```powershell
# Backend
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload

# Frontend, in another terminal
cd frontend\frontend
npm run dev
```

Open `http://127.0.0.1:5173` and use the backend docs at `http://127.0.0.1:8000/docs`.

## Real Travel Data

The `knowledge/` directory is intentionally not populated with unreviewed data. Add dated, trusted `.pdf`, `.txt`, or `.md` documents from tourism boards, transport operators, or other approved publishers.

Then ingest local documents:

```powershell
cd backend
..\.venv\Scripts\python.exe -m app.rag.ingest
```

For reviewed web sources, update `backend/scripts/ingest_sources.py` and run:

```powershell
..\.venv\Scripts\python.exe scripts\ingest_sources.py
```

Every exact price or availability claim should have a source and date. Without indexed sources, the assistant returns general guidance and marks prices as not verified.

## API Surface

| Endpoint | Purpose |
| --- | --- |
| `POST /auth/register` | Create an account |
| `POST /auth/login` | Get a bearer token |
| `GET /conversations` | List the authenticated user's conversations |
| `POST /conversations` | Create a conversation |
| `PATCH /conversations/{id}` | Rename an owned conversation |
| `DELETE /conversations/{id}` | Delete an owned conversation |
| `POST /chat` | Generate a structured authenticated response |
| `WS /ws/chat?token=...` | Stream an authenticated response |
| `GET /health` | Process liveness |
| `GET /ready` | Database and Ollama readiness |
| `GET /metrics` | Cache, latency, and timeout counters |

## Performance

The included benchmark measures setup, HTTP chat, WebSocket first-message, and total streaming latency:

```powershell
cd backend
..\.venv\Scripts\python.exe scripts\benchmark_latency.py
```

On the development machine, measured HTTP latency improved from approximately `14.3s` to `2.0-3.6s` for a short query after RAG caching, concurrent context preparation, Ollama keep-alive, lower token generation, and streaming optimizations. Results vary by hardware, model state, and prompt.

## Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for Docker, environment, volume, health-check, SMTP, and CI guidance.

```powershell
docker compose up --build -d
docker compose exec ollama ollama pull qwen2.5:3b
docker compose exec ollama ollama pull all-minilm
```

The production frontend is served at `http://localhost:8080`.

## CI and Quality

GitHub Actions validates:

- Backend Python compilation
- Frontend linting and production build
- Backend and frontend Docker image builds

Local checks:

```powershell
cd frontend\frontend
npm run lint
npm run build

cd ..\..\backend
..\.venv\Scripts\python.exe -m compileall -q .
```

## Security Notes

- Never commit `.env`, credentials, database files, Chroma data, or model artifacts.
- Use a unique `SECRET_KEY` in production.
- Restrict `CORS_ORIGINS` to the deployed frontend origin.
- Keep Ollama private and behind the backend.
- Use Redis-backed rate limiting before running multiple backend instances.
- Use PostgreSQL and a migration workflow before scaling beyond local SQLite.
