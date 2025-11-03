from fastapi import APIRouter, Query, HTTPException
from data_base import get_connection, release_connection
import psycopg2

router = APIRouter(prefix="/books")

@router.get("/price-range", summary="Listar livros por faixa de preço")
def listar_livros_por_faixa_de_preco(
    min_price: float = Query(description="Preço mínimo para filtro", alias="min_price"),
    max_price: float = Query(description="Preço máximo para filtro", alias="max_price")
):
    """
    Retorna os livros cujo preço está entre os valores informados.
    Exemplo: `/api/v1/books?min_price=10&max_price=50`
    """
    conn = None
    try:

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT 
                id, title, book_url, price, availability, rating, image_url, collected_at, category
            FROM public.book_scraping_data
            WHERE price BETWEEN %s AND %s
            ORDER BY price ASC;
        """

        cursor.execute(query, (min_price, max_price))
        rows = cursor.fetchall()

        print(f"[DEBUG] Registros encontrados: {len(rows)}")

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum livro encontrado na faixa de preço especificada.")

        columns = [desc[0] for desc in cursor.description]
        livros = [dict(zip(columns, row)) for row in rows]

        return {"quantidade": len(livros), "livros": livros}

    except psycopg2.Error as db_err:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {db_err}")
    finally:
        if conn:
            release_connection(conn)