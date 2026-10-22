# MNEMORA AI

MNEMORA AI is a personal memory assistant project built around a persistent PostgreSQL database and a simple FastAPI backend.

## Project structure

- `app/` - application code
- `tests/` - test suite
- `Dockerfile` - application container
- `compose.yaml` - local development environment
- `.env.example` - example environment variables
- `.dockerignore` - Docker build exclusions

## Local setup

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

### Run the API

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Docker

```powershell
docker compose up -d --build
```

Then open:

- http://localhost:8000

## Health check

```powershell
curl http://localhost:8000/health
```

## Notes

This is the initial foundation of the project. The memory layer, task management, and AI integrations will be added in subsequent phases.
