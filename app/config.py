from pydantic import BaseSettings


class Settings(BaseSettings):
    # Database and external services
    DATABASE_URL: str = "postgresql://postgres:password@db:5432/postgres"
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/2"

    # Vector settings
    PGVECTOR_DIM: int = 1536

    # App
    SECRET_KEY: str = "replace-me-with-secure-key"

    class Config:
        env_file = ".env"


settings = Settings()
