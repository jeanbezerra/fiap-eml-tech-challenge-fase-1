from fastapi import APIRouter
from data_base import get_connection, release_connection

router = APIRouter(prefix="/books")

@router.get("/categories")
def get_categories():
    """
    Lista todas as categorias disponíveis.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT availability
            FROM public.book_scraping_data
            ORDER BY availability;
        """)
        categories = [row[0] for row in cursor.fetchall()]
        return {"count": len(categories), "categories": categories}
    finally:
        release_connection(conn)
