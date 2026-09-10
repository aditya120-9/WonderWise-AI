# Production Deployment

## Local Docker deployment

1. Copy `.env.example` to `.env` and replace `SECRET_KEY` with a long random value.
2. Start the stack:

```powershell
docker compose up --build -d
```

3. Pull the configured models into Ollama:

```powershell
docker compose exec ollama ollama pull qwen2.5:3b
docker compose exec ollama ollama pull all-minilm
```

4. Open `http://localhost:8080`.

The API is available at `http://localhost:8000`; health checks are at `/health`, `/ready`, and `/metrics`.

## Production requirements

- Use a unique `SECRET_KEY` and keep `.env` outside version control.
- Set `CORS_ORIGINS` to the exact HTTPS frontend origin.
- Put the stack behind an HTTPS reverse proxy.
- Back up the `backend_db`, `chroma_data`, and `ollama_data` volumes.
- Do not expose Ollama directly to the public internet.
- Use a managed database and migration workflow before scaling beyond a single host.

## CI

GitHub Actions runs backend tests and compilation, frontend lint/build, and Docker image builds on pushes and pull requests.
