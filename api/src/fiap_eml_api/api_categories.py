from fastapi import APIRouter, HTTPException
from data_base import get_connection, release_connection

router = APIRouter(prefix="/books")

@router.get("/categories", summary="Listar todas as categorias disponíveis")
def get_categories():
    """
    Retorna todas as categorias distintas dos livros disponíveis em estoque.
    Não requer parâmetros.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT category
            FROM public.book_scraping_data
            WHERE availability = 'In stock'
            ORDER BY category ASC;
        """)
        rows = cursor.fetchall()

        # Caso não haja categorias
        if not rows:
            raise HTTPException(status_code=404, detail="Nenhuma categoria encontrada.")

        categorias = [row[0] for row in rows if row[0] is not None]
        return {"quantidade": len(categorias), "categorias": categorias}

    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco de dados: {e}")
    finally:
        if conn:
            release_connection(conn)