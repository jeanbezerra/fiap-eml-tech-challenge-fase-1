from fastapi import FastAPI
from api.api_id_book_core import router as books_router
from api.api_title_or_categorie import router as search_router
from api.api_Categories import router as categories_router
from api.api_health_core import router as health_router
from api.api_books import router as list_books_router 


app = FastAPI(
    title="Tech Challenge - FIAP",
    version="1.0",
    description="API para consulta de livros, categorias e status do sistema."
)

# 
app.include_router(books_router, prefix="/api/v1", tags=["Obrigatórios"])          
app.include_router(search_router, prefix="/api/v1", tags=["Obrigatórios"])         
app.include_router(categories_router, prefix="/api/v1", tags=["Obrigatórios"])     
app.include_router(health_router, prefix="/api/v1", tags=["Obrigatórios"])         
app.include_router(list_books_router, prefix="/api/v1", tags=["Obrigatórios"])


@app.get("/", tags=["Obrigatórios"]) 
def root():
    return {"message": " API Tech Challenge - FIAP"}
