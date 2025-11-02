from fastapi import APIRouter
from .data_base import get_connection, release_connection

router = APIRouter(prefix="/api/v1/stats", tags=["Opcionais"])

@router.get("/overview", summary="Estatísticas gerais da coleção de livros")
def stats_overview():
    """
    Retorna estatísticas gerais da coleção:
    - Total de livros
    - Preço médio
    - Distribuição de ratings (contagem por nota)
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Estatísticas gerais
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_books,
                ROUND(AVG(price), 2) AS avg_price
            FROM public.book_scraping_data;
        """)
        totals = cursor.fetchone()
        total_books, avg_price = totals

        # Distribuição de ratings (ex: quantos livros têm rating 5, 4, etc.)
        cursor.execute("""
            SELECT 
                rating,
                COUNT(*) AS count
            FROM public.book_scraping_data
            WHERE rating IS NOT NULL
            GROUP BY rating
            ORDER BY rating::NUMERIC DESC;
        """)
        ratings = cursor.fetchall()
        rating_distribution = [
            {"rating": row[0], "count": row[1]} for row in ratings
        ]

        return {
            "total_books": total_books,
            "avg_price": avg_price,
            "rating_distribution": rating_distribution
        }

    finally:
        release_connection(conn)
