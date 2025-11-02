from fastapi import APIRouter
from .data_base import get_connection, release_connection

router = APIRouter(prefix="/api/v1/books", tags=["Opcionais"])

@router.get("/price-range", summary="Filtra livros dentro de uma faixa de preço específica")
def filter_by_price(min: float = 0, max: float = 9999):
    """
    Filtra livros com preço entre os valores informados.
    Exemplo: /api/v1/books/price-range?min=10&max=30
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                id, title, book_url, price, availability, rating, image_url, collected_at
            FROM public.book_scraping_data
            WHERE price BETWEEN %s AND %s
            ORDER BY price ASC;
        """, (min, max))

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        books = [dict(zip(columns, row)) for row in rows]

        return {"count": len(books), "books": books}

    finally:
        release_connection(conn)
