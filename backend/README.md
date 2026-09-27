# Backend

FastAPI application for safe local video uploads and offline analysis-job
management. The code is organized by entity under `app/entities`; each feature
owns its HTTP router, schemas, persistence model, repository, and service.

The API deliberately queues analysis records without inventing results. The
computer-vision worker described in the root architecture document is not yet
implemented, so readiness reports `analysis_worker: not_configured`.

## Run locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
cp .env.example .env
uvicorn app.main:app --reload
```

Open <http://localhost:8000/docs>. Uploaded videos and the development SQLite
database are written below `backend/data/` by default.

## Checks

```bash
ruff check .
pytest
```

Configuration uses environment variables prefixed with `BOXING_`. CORS origins
are encoded as a JSON list. Production deployments should disable interactive
docs as appropriate, store media outside the application container, add
authentication/authorization, and replace automatic table creation with
versioned migrations.
