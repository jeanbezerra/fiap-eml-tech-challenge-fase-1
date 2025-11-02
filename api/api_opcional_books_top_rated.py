from fastapi import APIRouter
from .data_base import get_connection, release_connection

router = APIRouter(prefix="/api/v1/books", tags=["Opcionais"])

@router.get("/top-rated", summary="Lista os livros com melhor avaliação (rating mais alto)")
def top_rated_books(limit: int = 10):
    """
    Retorna os livros com melhor rating.
    Ordena do maior para o menor rating.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                id, title, book_url, price, availability, rating, image_url, collected_at
            FROM public.book_scraping_data
            WHERE rating IS NOT NULL
            ORDER BY rating::NUMERIC DESC, collected_at DESC
            LIMIT %s;
        """, (limit,))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        books = [dict(zip(columns, row)) for row in rows]

        return {"count": len(books), "books": books}

    finally:
        release_connection(conn)
