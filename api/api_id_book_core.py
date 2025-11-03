from fastapi import APIRouter, HTTPException
from uuid import UUID
from data_base import get_connection, release_connection
import psycopg2

router = APIRouter(prefix="/books")

@router.get("/id/{book_id}", summary="Buscar livro por ID (UUID)")
def get_book_by_id(book_id: UUID):
    """
    Retorna os detalhes de um livro específico com base no seu UUID.
    Exemplo: /api/v1/books/id/d51ff023-6918-4663-8a27-60abd6e1eac3
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, category, price, availability, rating, image_url
            FROM public.book_scraping_data
            WHERE id = %s;
        """, (str(book_id),))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Livro não encontrado.")

        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {e}")
    finally:
        if conn:
            release_connection(conn)
