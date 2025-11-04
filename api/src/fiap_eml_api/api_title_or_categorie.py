from fastapi import APIRouter, Query, HTTPException, Depends
from fiap_eml_api.auth_jwt import get_current_user
from typing import Optional
import psycopg2
from data_base import get_connection, release_connection

router = APIRouter(prefix="/books")

@router.get("/filters", summary="Listar livros por título e/ou categoria")
def list_books(
    title: Optional[str] = Query(None, description="Parte ou nome completo do título"),
    category: Optional[str] = Query(None, description="Categoria"),
    current_user: str = Depends(get_current_user)
):
    """
    Lista todos os livros ou filtra por título e/ou categoria.
    Exemplo:
        GET /api/v1/books?title=python&category=programming
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT id, title, book_url, price, availability, rating, image_url, collected_at
            FROM public.book_scraping_data
            WHERE 1=1
        """
        params = []

        if title:
            query += " AND title ILIKE %s"
            params.append(f"%{title}%")

        if category:
            query += " AND category ILIKE %s"
            params.append(f"%{category}%")

        query += " ORDER BY collected_at DESC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum livro encontrado com os filtros fornecidos.")

        columns = [desc[0] for desc in cursor.description]
        books = [dict(zip(columns, row)) for row in rows]

        return {"count": len(books), "books": books}

    except psycopg2.Error as db_err:
        raise HTTPException(status_code=500, detail=f"Database error: {db_err}")
    finally:
        if conn:
            release_connection(conn)