from celery import Celery
from app.db import get_db_connection
import os, time, requests

app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'))

# Grok configuration
GROK_API_URL = os.getenv("GROK_API_URL", "https://api.grok.ai/v1/embeddings")
GROK_API_KEY = os.getenv("GROK_API_KEY")


def get_embedding(content: str):
    headers = {"Content-Type": "application/json"}
    if GROK_API_KEY:
        headers["Authorization"] = f"Bearer {GROK_API_KEY}"
    payload = {"input": content, "model": os.getenv("GROK_EMBEDDING_MODEL", "grok-embedding-1")}
    r = requests.post(GROK_API_URL, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()

@app.task(bind=True, max_retries=3)
def compute_and_store_embedding(self, doc_id: int):
    """Fetch document, compute embedding, and store it in Postgres."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT content FROM documents WHERE id=%s;", (doc_id,))
        row = cur.fetchone()
        if not row:
            return "Document not found"

        content = row[0]
    # Get embedding
    response = get_embedding(content)
        embedding = response["data"][0]["embedding"]

        # Store embedding in Postgres
        cur.execute("UPDATE documents SET embedding = %s WHERE id = %s;", (embedding, doc_id))
        conn.commit()
        conn.close()
        return "Success"

    except Exception as e:
        raise self.retry(exc=e, countdown=60)
