from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/stats", tags=["Opcionais"])

@router.get("/categories", summary="Estatísticas detalhadas por categoria")
def stats_by_category():
    """
    Retorna estatísticas detalhadas por categoria:
    - Quantidade de livros
    - Preço médio
    *Este endpoint depende da coluna 'category' no banco.*
    """
    return {
        "message": "Endpoint indisponível — a tabela 'book_scraping_data' não possui coluna 'category'. "
                   "Adicione a coluna para habilitar estatísticas por categoria."
    }

