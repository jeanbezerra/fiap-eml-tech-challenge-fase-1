# API – FastAPI

Este projeto utiliza **FastAPI** como framework web e o **uv** como gerenciador de dependências e ambiente virtual.  
Abaixo estão as instruções essenciais para configurar, instalar dependências e iniciar o servidor localmente.

---

## Inicializar o projeto com `uv`

Cria a estrutura inicial do ambiente e o arquivo `pyproject.toml`:

```powershell
uv init
```

## Instalar dependências

Adiciona os pacotes principais para execução da API:

```powershell
uv add uvicorn fastapi psycopg2 psycopg2-binary python-multipart python-jose[cryptography]
```

Em seguida, sincronize o ambiente virtual com as dependências listadas no pyproject.toml

```powershell
uv sync
```

## Construir o projeto

Gera os artefatos necessários para distribuição (build local):

```powershell
uv build
```

## Executar o servidor FastAPI

Durante o desenvolvimento, use o modo hot reload (reinício automático ao salvar arquivos):

```powershell
uv run uvicorn fiap_eml_api.api_main:app --reload
```

Inicia o servidor de aplicação FastAPI utilizando o Uvicorn:

```powershell
uv run uvicorn fiap_eml_api.api_main:app
```

## Acesso à documentação interativa

Após iniciar o servidor, acesse no navegador:

- Swagger UI: http://localhost:8000/
- ReDoc: http://localhost:8000/redoc

## URL de Produção

A API está publicada no ambiente de produção através do Render:
- Produção (Swagger): https://fiap-eml-tech-challenger-fase-1.onrender.com
- Produção (ReDoc): https://fiap-eml-tech-challenger-fase-1.onrender.com/redoc