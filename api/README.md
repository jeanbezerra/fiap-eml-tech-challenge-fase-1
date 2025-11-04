# API - FastAPI

## Como iniciar o projeto com uv

```powershell
uv init
```

## Como rodar

```powershell
uv add uvicorn fastapi psycopg2 psycopg2-binary python-multipart python-jose[cryptography]
```

```powershell
uv sync
```

```powershell
uv build
```

```powershell
uv run uvicorn fiap_eml_api.api_main:app
```

```powershell
uv run uvicorn fiap_eml_api.api_main:app --reload
```