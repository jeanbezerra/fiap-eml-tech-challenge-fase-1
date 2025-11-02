from fastapi import APIRouter
# import pandas as pd

router = APIRouter(prefix="/api/v1/stats", tags=["Opcionais"])

DATA_FILE = "scripts/books_to_scrape.csv"

def load_books_df():
    df = pd.read_csv(DATA_FILE)
    if "id" not in df.columns:
        df = df.reset_index().rename(columns={"index": "id"})
        df["id"] = df["id"] + 1
    df["price"] = df["price"].replace("£", "", regex=True).astype(float)
    rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    if df["rating"].dtype == object:
        df["rating"] = df["rating"].map(rating_map).fillna(0)
    return df


@router.get("/overview")
def stats_overview():
    """Estatísticas gerais da coleção de livros"""
    df = load_books_df()
    return {
        "total_books": len(df),
        "avg_price": round(df["price"].mean(), 2),
        "avg_rating": round(df["rating"].mean(), 2),
    }
