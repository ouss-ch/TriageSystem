# TriageSystem

Backend that ingests support ticket emails, runs LLM analysis (sentiment, category, keywords, priority), and exposes metrics for a dashboard.

## Stack

- FastAPI — API
- Celery + RabbitMQ — async task queue (email ingestion, LLM analysis)
- PostgreSQL — storage
- Docker Compose — local orchestration
- LLM provider (Anthropic) — analysis engine

## Structure

```
app/
  api/            # FastAPI routers (v1)
  core/           # config, celery app, logging
  db/             # DB session/engine
  models/         # SQLAlchemy ORM models
  schemas/        # Pydantic schemas
  services/       # business logic (email ingestion, LLM calls)
  tasks/          # Celery task definitions
  main.py         # app entrypoint
migrations/       # Alembic migrations
docker/           # Dockerfiles
tests/
```

## Setup

```bash
cp .env.example .env
docker compose up --build
```

API docs: http://localhost:8000/docs
RabbitMQ management: http://localhost:15672

## Status

Skeleton only — no business logic implemented yet.

<!-- TODO: architecture diagram, API reference, dev workflow, testing instructions -->
