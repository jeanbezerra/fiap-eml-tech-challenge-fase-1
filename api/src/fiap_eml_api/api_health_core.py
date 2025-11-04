from fastapi import APIRouter, HTTPException, Depends
from fiap_eml_api.auth_jwt import get_current_user
from data_base import get_connection, release_connection

router = APIRouter(prefix="/health")

@router.get("/")
def health_check(current_user: str = Depends(get_current_user)):
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
