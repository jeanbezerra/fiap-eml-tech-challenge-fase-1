from fastapi import APIRouter, HTTPException
from uuid import UUID
from data_base import get_connection, release_connection
import psycopg2

router = APIRouter(prefix="/books")

@router.get("/{id}")
def get_book_by_id(book_id: UUID):
    """
    Retorna um livro pelo seu ID.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, title, book_url, price, availability, rating, image_url, collected_at
            FROM public.book_scraping_data
            WHERE id = %s;
        """, (str(book_id),))

        book = cursor.fetchone()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        columns = [desc[0] for desc in cursor.description]
        book_dict = dict(zip(columns, book))

        return book_dict

    except psycopg2.Error as db_err:
        raise HTTPException(status_code=500, detail=f"Database error: {db_err}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
    finally:
        if conn:
            release_connection(conn)
