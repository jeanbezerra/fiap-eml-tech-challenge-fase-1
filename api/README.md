# API - FastAPI

## Como iniciar o projeto com uv

```powershell
uv init
```

## Como rodar

```powershell
uv add uvicorn fastapi
```

```powershell
uv sync
```

```powershell
uv run uvicorn api.api_main:app

uv run uvicorn api.api_main:app -reload
```