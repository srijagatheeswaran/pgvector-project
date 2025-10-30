import hashlib, os, datetime
from app.db import get_db_connection

SALT = os.getenv("HASH_SALT", "default-salt")

def hash_user_id(user_id: str):
    return hashlib.sha256((SALT + user_id).encode()).hexdigest()

def log_event(event_type: str, user_id: str, metadata: dict):
    conn = get_db_connection()
    cur = conn.cursor()
    user_hash = hash_user_id(user_id)
    retention = datetime.datetime.now() + datetime.timedelta(days=90)
    cur.execute(
        "INSERT INTO audit_logs (event_type, user_hash, metadata, retention_until) VALUES (%s, %s, %s, %s);",
        (event_type, user_hash, json.dumps(metadata), retention)
    )
    conn.commit()
    conn.close()
