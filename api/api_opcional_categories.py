from fastapi import APIRouter
# import pandas as pd
from .api_opcional_overview import load_books_df

router = APIRouter(prefix="/api/v1/stats", tags=["Opcionais"])

@router.get("/categories")
def stats_by_category():
    """Retorna estatísticas detalhadas por categoria"""
    df = load_books_df()
    grouped = df.groupby("category").agg(
        total_books=("title", "count"),
        avg_price=("price", "mean")
    ).reset_index()
    grouped["avg_price"] = grouped["avg_price"].round(2)
    return grouped.to_dict(orient="records")
