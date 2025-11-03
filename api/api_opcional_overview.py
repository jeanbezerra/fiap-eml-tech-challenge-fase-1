from http.client import HTTPException
from fastapi import APIRouter
from data_base import get_connection, release_connection
import psycopg2 # Importar psycopg2 para tratamento de erros

router = APIRouter(prefix="/stats", tags=["Opcionais"])

@router.get("/overview", summary="Estatísticas gerais da coleção de livros")
def stats_overview():
    """
    Retorna estatísticas gerais da coleção, incluindo a distribuição de ratings
    e o percentual que cada rating representa no total de livros.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Estatísticas gerais (incluindo o total_books para o cálculo do percentual)
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_books,
                ROUND(AVG(price), 2) AS avg_price
            FROM public.book_scraping_data;
        """)
        totals = cursor.fetchone()
        
        # O total de livros deve ser diferente de zero para evitar divisão por zero
        total_books = totals[0] if totals and totals[0] else 0
        avg_price = totals[1]

        # 2. Distribuição de ratings (ex: quantos livros têm rating 5, 4, etc.)
        cursor.execute("""
            SELECT 
                rating,
                COUNT(*) AS count
            FROM public.book_scraping_data
            WHERE rating IS NOT NULL AND rating != ''
            GROUP BY rating
            ORDER BY rating::NUMERIC DESC;
        """)
        ratings = cursor.fetchall()
        
        rating_distribution = []
        # Calcular o percentual apenas se houver livros no total
        if total_books > 0:
            for row in ratings:
                rating = row[0]
                count = row[1]
                
                # Cálculo do percentual: (contagem / total de livros) * 100
                percentage = round((count / total_books) * 100, 2)
                
                rating_distribution.append({
                    "rating": rating, 
                    "count": count,
                    "percentage": percentage  # <-- NOVO CAMPO
                })

        return {
            "total_books": total_books,
            "avg_price": avg_price,
            "rating_distribution": rating_distribution
        }
    
    except psycopg2.Error as db_err:
        # Adicionado tratamento de erro de DB para robustez
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {db_err}")

    finally:
        if conn:
            release_connection(conn)