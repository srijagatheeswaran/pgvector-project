import psycopg2, os

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "appdb"),
        user=os.getenv("POSTGRES_USER", "user"),
        password=os.getenv("POSTGRES_PASSWORD", "pass"),
        host=os.getenv("POSTGRES_HOST", "db")
    )