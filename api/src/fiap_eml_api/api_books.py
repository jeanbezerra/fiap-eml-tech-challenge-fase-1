from fastapi import APIRouter, HTTPException, Depends
from fiap_eml_api.auth_jwt import get_current_user
from data_base import get_connection, release_connection
import psycopg2

router = APIRouter()

@router.get("/books", summary="Listar todos os livros disponíveis")
def listar_todos_os_livros(current_user: str = Depends(get_current_user)):
    """
    Retorna todos os livros armazenados no banco de dados, ordenados pela data de coleta mais recente.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, book_url, price, availability, rating, image_url, collected_at, category
            FROM public.book_scraping_data
            ORDER BY collected_at DESC;
        """)
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum livro encontrado.")

        columns = [desc[0] for desc in cursor.description]
        livros = [dict(zip(columns, row)) for row in rows]

        return {
            "usuario": current_user,  # opcional — remove se não quiser mostrar
            "quantidade": len(livros),
            "livros": livros
        }

    except psycopg2.Error as db_err:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {db_err}")
    finally:
        release_connection(conn)