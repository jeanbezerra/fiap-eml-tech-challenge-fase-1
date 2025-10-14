from fastapi import FastAPI, HTTPException
import csv

app = FastAPI(title="Books API", version="1.0")

DATA_FILE = "scripts/books_to_scrape.csv"

# Função para carregar os livros do CSV
def load_books():
    books = []
    with open(DATA_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            books.append(row)
    return books

#Endpoints Core


@app.get("/api/v1/books", tags=["Obrigatório"])
def get_books():
    """Lista todos os livros"""
    return load_books()

@app.get("/api/v1/books/{book_id}")
def get_book(book_id: int):
    """Retorna detalhes de um livro específico pelo ID"""
    books = load_books()
    if 0 <= book_id < len(books):
        return books[book_id]
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/api/v1/books/search", tags=["Opcional"])
def search_books(title: str = "", category: str = ""):
    """Busca livros por título e/ou categoria"""
    books = load_books()
    results = [b for b in books if title.lower() in b['title'].lower() and category.lower() in b['category'].lower()]
    return results

@app.get("/api/v1/categories")
def get_categories():
    """Lista todas as categorias de livros disponíveis"""
    books = load_books()
    categories = set(b['category'] for b in books)
    return list(categories)


@app.get("/api/v1/health")
def health_check():
    """Verifica status da API"""
    return {"status": "ok"}
