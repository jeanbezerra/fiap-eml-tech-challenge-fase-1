from fastapi import APIRouter
from .data_base import get_connection, release_connection
import psycopg2

router = APIRouter(prefix="/api/v1/books")

@router.get("/", summary=" list all available books")
def list_all_books():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, book_url, price, availability, rating, image_url, collected_at
            FROM public.book_scraping_data
            ORDER BY collected_at DESC;
        """)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        books = [dict(zip(columns, row)) for row in rows]
        return {"count": len(books), "books": books}
    finally:
        release_connection(conn)
