from fastapi import APIRouter
from .data_base import get_connection, release_connection

router = APIRouter(prefix="/api/v1/stats", tags=["Opcionais"])

@router.get("/categories", summary="Estatísticas detalhadas por categoria")
def stats_by_category():
    """
    Retorna estatísticas detalhadas por categoria:
    - Quantidade total de livros por categoria
    - Preço médio por categoria
    - Média de avaliação (rating) por categoria
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                category,
                COUNT(*) AS total_books,
                ROUND(AVG(price), 2) AS avg_price,
                ROUND(AVG(rating::NUMERIC), 2) AS avg_rating
            FROM public.book_scraping_data
            WHERE category IS NOT NULL
            GROUP BY category
            ORDER BY total_books DESC;
        """)

        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]

        return {"count": len(result), "categories_stats": result}

    finally:
        release_connection(conn)

