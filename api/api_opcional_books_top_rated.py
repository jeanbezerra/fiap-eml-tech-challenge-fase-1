from fastapi import APIRouter
# import pandas as pd
from .api_opcional_overview import load_books_df

router = APIRouter(prefix="/api/v1/books", tags=["Opcionais"])

@router.get("/top-rated")
def top_rated_books(limit: int = 10):
    """Lista os livros com melhor avaliação (rating mais alto)"""
    df = load_books_df()
    top_books = df.sort_values(by="rating", ascending=False).head(limit)
    return top_books.to_dict(orient="records")
