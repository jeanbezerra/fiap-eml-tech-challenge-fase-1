from fastapi import FastAPI

# ------------------------------
# Imports das APIs obrigatórias
# ------------------------------
from api_id_book_core import router as books_router
from api_title_or_categorie import router as search_router
from api_categories import router as categories_router
from api_health_core import router as health_router
from api_books import router as list_books_router

# ------------------------------
# Imports das APIs opcionais
# ------------------------------
from api_opcional_overview import router as stats_overview_router
from api_opcional_categories import router as stats_categories_router
from api_opcional_books_best_rated import router as best_rated_router
from api_opcional_books_price_range import router as price_range_router


# ------------------------------
# Configuração principal da API
# ------------------------------
app = FastAPI(
    title="FIAP - Machine Learning Engineering (7MLET) - Tech Challenge",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc",
    description="API para consulta de livros, categorias e status do sistema."
)


# ------------------------------
# Rotas obrigatórias
# ------------------------------
app.include_router(categories_router, prefix="/api/v1", tags=["Obrigatórios"])
app.include_router(books_router, prefix="/api/v1", tags=["Obrigatórios"])
app.include_router(search_router, prefix="/api/v1", tags=["Obrigatórios"])
app.include_router(health_router, prefix="/api/v1", tags=["Obrigatórios"])
app.include_router(list_books_router, prefix="/api/v1", tags=["Obrigatórios"])


# ------------------------------
# Rotas opcionais
# ------------------------------
app.include_router(stats_overview_router, prefix="/api/v1", tags=["Opcionais"])
app.include_router(stats_categories_router, prefix="/api/v1", tags=["Opcionais"])
app.include_router(best_rated_router, prefix="/api/v1", tags=["Opcionais"])
app.include_router(price_range_router, prefix="/api/v1", tags=["Opcionais"])



# ------------------------------
# Rota raiz (home)
# ------------------------------
# @app.get("/", tags=["Obrigatórios"])
# def root():
#     return {"message": "API Tech Challenge - FIAP"}
