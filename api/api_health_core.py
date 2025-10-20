from fastapi import APIRouter
from .data_base import get_connection, release_connection

router = APIRouter(prefix="/api/v1/health")

@router.get("/")
def health_check():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if conn:
            release_connection(conn)
