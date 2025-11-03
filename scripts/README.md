
# Dependencias

```powershell
uv add beautifulsoup4 requests psycopg2
```

## Como executar?

Sincronize as bibliotecas que o projeto tem como dependência, antes de executar o script de scraping.

```powershell
uv sync
```

```powershell
uv run python scrape_books.py
```

```powershell
uv run python save_books_to_postgres.py
```