# Vector Project (scaffold)

This repository contains a minimal scaffold for a FastAPI application that stores documents and their vector embeddings in Postgres using pgvector. Celery is included for background embedding generation.

Structure created:

  - app/
    - main.py: FastAPI entrypoint
    - db.py: SQLAlchemy engine and session
    - models.py: SQLAlchemy models (documents + GDPR tables)
    - tasks.py: Celery tasks + example embedding generator
    - utils.py: hashing and helper embedding function
    - config.py: environment settings (pydantic)

  - migrations/: example SQL migrations to enable pgvector and create tables
  - tests/: basic pytest for embedding generation
  - Dockerfile / docker-compose.yml
  - requirements.txt

Quick start (with Docker):

1. Copy `.env.example` to `.env` and adjust values.
2. Start with Docker Compose:

   docker-compose up --build

3. Visit: http://localhost:8000/docs

Notes:
- The `hash_text_to_embedding` is a placeholder. Replace with real model calls.
- Use proper migrations (alembic, flyway, or your preferred tool) in production.
