# Tech Challenge — API Pública de Livros (Fase 1: Machine Learning Engineering)

> **Resumo:** Este repositório entrega um pipeline completo de **Web Scraping → Transformação → API pública** com foco em escalabilidade e reuso para projetos de **Machine Learning**. Inclui documentação das rotas, exemplos de requisições, instruções de instalação/execução e diretrizes para deploy público.

---

## 🔭 Objetivos do Projeto

- **Extrair** dados do site `https://books.toscrape.com/`.
- **Persistir** os dados em **CSV** (e, opcionalmente, SQLite/PostgreSQL).
- **Servir** os dados via **API RESTful** (FastAPI ou Flask) com documentação **Swagger/OpenAPI**.
- **Facilitar** o consumo por cientistas de dados e pipelines de ML (endpoints de **features** e **training-data** opcionais).
- **Preparar** o deploy público (Render/Heroku/Vercel/Fly.io etc).

---

## 🧱 Arquitetura (Visão Macro)

```
[Web Scraping] --> [Camada de Dados] --> [API Pública] --> [Consumidores/Clients/ML]
       |               |                     |                 |
  scripts/             data/               api/             notebooks/ (opcional)
```

- **Web Scraping:** Coleta robusta de todos os livros (título, preço, rating, disponibilidade, categoria, imagem).
- **Transformação:** Normalização/limpeza + gravação em CSV (ex.: `data/books.csv`).
- **API:** Endpoints REST para listar/consultar livros, categorias, estatísticas e saúde da aplicação.
- **Escalabilidade futura:** Separação em módulos, logs estruturados, autenticação (JWT) e endpoints ML-ready (opcionais).

> Um diagrama C4/fluxo pode ser incluído em `docs/architecture.png`. Gere com PlantUML/Mermaid e referencie abaixo em **Arquitetura Visual**.

---

## 📁 Estrutura de Pastas

```
.
├── api/
│   ├── api_main.py                         # Entrypoint principal da API
│   ├── api_books.py                        # Endpoint: listar livros
│   ├── api_id_book_core.py                 # Endpoint: detalhes por ID
│   ├── api_title_or_categorie.py           # Endpoint: busca por título/categoria
│   ├── api_Categories.py                   # Endpoint: categorias
│   ├── api_health_core.py                  # Endpoint: health check
│   ├── api_opcional_overview.py            # Endpoint opcional: estatísticas gerais
│   ├── api_opcional_categories.py          # Endpoint opcional: estatísticas por categoria
│   ├── api_opcional_books_top_rated.py     # Endpoint opcional: livros com melhor rating
│   ├── api_opcional_books_price_range.py   # Endpoint opcional: filtro por faixa de preço
│   └── data_base.py                        # Conexão com banco de dados (opcional)
│
├── scripts/
│   └── scrape_books.py                     # Script de scraping automatizado
│
├── data/
│   └── books_to_scrape.csv                 # Base local com os dados extraídos
│
├── README.md
├── pyproject.toml
└── uv.lock

```

## ⚙️ Instalação & Configuração

### Opção A) Ambiente Local (Python moderno com `uv` ou `pip`)
> Requer **Python 3.11+**.

**Com `uv` (recomendado):**
```bash
# Instalar uv (Windows PowerShell)
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Instalar dependências (gera venv automaticamente)
uv sync

# Ativar ambiente (se necessário)
# Linux/MacOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

**Com `pip`:**
```bash
python -m venv .venv
# Linux/MacOS:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

**Variáveis de Ambiente (`.env`)**
```
# Copie .env.example para .env e ajuste conforme necessário
DATA_FILE_PATH=data/books.csv
API_TITLE=Books API
API_VERSION=v1
ENABLE_AUTH=false          # true para JWT (bônus)
SECRET_KEY=change-me       # necessário se ENABLE_AUTH=true
ACCESS_TOKEN_EXPIRE_MIN=30
```

---

## 🕷️ Web Scraping

**Execução (local):**
```bash
# Via Makefile
make scrape
# ou diretamente
python scripts/scrape_books.py --out data/books.csv --images false
```

**Parâmetros comuns:**
- `--out`: caminho do CSV (default: `data/books.csv`)
- `--images`: baixa imagens? (`true/false`, default: `false`)

**Schema do CSV (sugerido):**
```csv
id,title,price,rating,availability,category,image_url,product_page_url
```

---

## 🚀 Execução da API

### FastAPI (com uv)
```bash
# Executar localmente com hot reload
uv run uvicorn api.api_main:app --reload

```

- **Documentação Swagger**: `http://localhost:8000/docs`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

📦 As APIs foram modularizadas em arquivos separados dentro de api/, mantendo uma arquitetura mais escalável e limpa.
---

## 🔌 Endpoints da API (Core)

| Método | Rota                                                | Descrição                                      |
|-------:|-----------------------------------------------------|-----------------------------------------------|
| GET    | `/api/v1/health`                                    | Verifica status da API e conectividade.       |
| GET    | `/api/v1/books`                                     | Lista todos os livros. Suporta paginação.     |
| GET    | `/api/v1/books/{id}`                                | Detalhes de um livro por ID.                  |
| GET    | `/api/v1/books/search?title={t}&category={c}`       | Busca por título e/ou categoria.              |
| GET    | `/api/v1/categories`                                | Lista categorias disponíveis.                  |

### Exemplos (cURL)

```bash
# Health
curl -s http://localhost:8000/api/v1/health

# Listar livros (primeira página)
curl -s "http://localhost:8000/api/v1/books?page=1&size=50"

# Detalhe por ID
curl -s http://localhost:8000/api/v1/books/BOOK_000123

# Busca por título e categoria
curl -s "http://localhost:8000/api/v1/books/search?title=travel&category=Travel"

# Categorias
curl -s http://localhost:8000/api/v1/categories
```

---

## 📊 Endpoints Opcionais (Insights)

| Método | Rota                                      | Descrição                                                     |
|-------:|-------------------------------------------|--------------------------------------------------------------|
| GET    | `/api/v1/stats/overview`                  | Estatísticas gerais (total, preço médio, dist. de ratings).  |
| GET    | `/api/v1/stats/categories`                | Estatísticas por categoria (qtde, preços).                   |
| GET    | `/api/v1/books/top-rated`                 | Livros com melhor avaliação (rating mais alto).              |
| GET    | `/api/v1/books/price-range?min=&max=`     | Filtra livros por faixa de preço.                            |

### Exemplos (cURL)
```bash
curl -s http://localhost:8000/api/v1/stats/overview
curl -s http://localhost:8000/api/v1/stats/categories
curl -s http://localhost:8000/api/v1/books/top-rated
curl -s "http://localhost:8000/api/v1/books/price-range?min=10&max=25"
```

---

## 🔐 (Bônus) Autenticação JWT

- **Login:** `POST /api/v1/auth/login` → retorna `access_token`.
- **Refresh:** `POST /api/v1/auth/refresh`.
- **Proteção de rotas de admin** (ex.: `/api/v1/scraping/trigger`).

### Exemplo (cURL)
```bash
# Login
curl -s -X POST http://localhost:8000/api/v1/auth/login   -H "Content-Type: application/json"   -d '{"username":"admin","password":"admin"}'

# Requisição autenticada
curl -s http://localhost:8000/api/v1/scraping/trigger   -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---

## 🤖 (Bônus) Endpoints ML-Ready

- `GET /api/v1/ml/features` → dados prontos para features de modelos.
- `GET /api/v1/ml/training-data` → dataset de treinamento (CSV/JSON).
- `POST /api/v1/ml/predictions` → recebe payload e retorna predições.

> Padronize contratos para facilitar experimentação e MLOps (versione schemas).

---

## 📈 (Bônus) Monitoramento & Analytics

- **Logs estruturados** (JSON) por request/response.
- **Métricas** de latência, throughput, status code (ex.: Prometheus + Grafana).
- **Dashboard simples** (ex.: Streamlit) para visualização do uso.

---

## 🧪 Testes

```bash
# Testes unitários
make test
# ou
pytest -q
```

---

## 🐳 Docker (opcional)

```bash
# Build
docker build -t books-api:latest .

# Run
docker run -p 8000:8000 --env-file .env books-api:latest
```

---

## 🌐 Deploy Público

- **Plataformas sugeridas:** Render, Fly.io, Railway, Vercel (serverless), Heroku.
- **Checklist:**
  - Defina variáveis de ambiente (vide `.env.example`).
  - Ajuste o `start` da API (Uvicorn/Gunicorn).
  - Anexe persistência (se usar DB) ou gere `books.csv` no build/cron.

**Link do Deploy:** _adicione aqui após publicar_

---

## 🎬 Vídeo de Apresentação (3–12 min)

Inclua:
- Visão da **arquitetura** e **pipeline**.
- Demonstração do **scraping** e **API em produção** (chamadas reais).
- Comentários sobre **boas práticas** implementadas.

**Link do Vídeo:** _adicione aqui_

---

## 🗺️ Arquitetura Visual

> Adicione aqui uma imagem/diagrama (ex.: `docs/architecture.png`) descrevendo:
- Pipeline **ingestão → processamento → API → consumo**.
- Componentes para **escalabilidade** (fila/cache/DB/observabilidade).
- Integração futura com **modelos de ML** (features store/serving).

---

## 📌 Entregáveis Requeridos (Checklist)

- [x] Repositório organizado (`scripts/`, `api/`, `data/`, etc.)
- [x] README completo (este arquivo)
- [x] Script de scraping funcional → **CSV** gerado
- [x] API RESTful (Flask/FastAPI) + **Swagger**
- [x] Deploy público com link funcional
- [ ] Plano arquitetural (diagrama ou doc)
- [ ] Vídeo de apresentação (3–12 min)

> **Plus (10 pts):** concluir **Beginner: Introduction to Generative AI Learning Path** (Google Cloud Skill Boost) e anexar comprovante.

---

## 📎 Referências

- Books to Scrape: https://books.toscrape.com/
- FastAPI: https://fastapi.tiangolo.com/
- Requests/HTTPX, BeautifulSoup4/Selectolax, Uvicorn, Pydantic.
- Render/Fly.io/Heroku/Vercel para deploy.

---

## 📝 Licença

Este projeto é distribuído sob a licença MIT (ou defina a de sua preferência).

---

## 💡 Como contribuir

1. Crie uma branch a partir de `main`: `feat/minha-feature`.
2. Adicione testes e documentação.
3. Abra um Pull Request descrevendo o escopo da mudança.

---

> **Observação:** Este README segue integralmente os requisitos do enunciado da fase, incluindo endpoints obrigatórios e opcionais, deploy público e vídeo de apresentação. Preencher os campos de **deploy**, **vídeo** e **diagrama** quando finalizar cada etapa.
