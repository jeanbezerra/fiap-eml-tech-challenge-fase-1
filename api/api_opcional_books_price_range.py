from fastapi import APIRouter
# import pandas as pd
from .api_opcional_overview import load_books_df

router = APIRouter(prefix="/api/v1/books", tags=["Opcionais"])

@router.get("/price-range")
def filter_by_price(min: float = 0, max: float = 9999):
    """Filtra livros dentro de uma faixa de preço específica"""
    df = load_books_df()
    filtered = df[(df["price"] >= min) & (df["price"] <= max)]
    return filtered.to_dict(orient="records")
