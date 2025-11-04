# Tech Challenge - API Pública de Livros  

**FIAP Pós-Graduação em Machine Learning Engineering – Fase 1**

Este projeto entrega uma pipeline inicial para **obtenção e disponibilização de dados** visando uso futuro em modelos de Machine Learning.  
Nesta fase, implementamos o fluxo completo:

**Web Scraping → Tratamento → Persistência → API REST → Autenticação JWT → Desenho Arquitetural**

## Membros do Grupo

| Nome | RA | Função no Projeto |
|------|----|------------------|
| *(Preencher Integrante 1)* | *(RA)* | Desenvolvimento da API e modularização |
| *(Preencher Integrante 2)* | *(RA)* | Web Scraping e tratamento de dados |
| *(Preencher Integrante 3)* | *(RA)* | Persistência e camada de acesso aos dados |
| *(Preencher Integrante 4)* | *(RA)* | Documentação, arquitetura e segurança (JWT) |


## Objetivos da Fase

1. Realizar **Web Scraping** do site público https://books.toscrape.com/.
2. **Normalizar e armazenar** os dados coletados em **CSV**.
3. Disponibilizar os dados por meio de uma **API REST** documentada com **Swagger/OpenAPI**.
4. Implementar **autenticação JWT** para rotas protegidas.
5. Entregar o **desenho arquitetural** do sistema (C4 — nível 3).

---

## Arquitetura da Solução

```
+------------------+       +------------------+       +----------------------+
|  Web Scraping    | --->  |  Camada de Dados | --->  |      API Pública     |
| (scripts/)       |       | (CSV / DB)       |       | (FastAPI + JWT)      |
+------------------+       +------------------+       +----------------------+
                                                         |
                                                         v
                                                 Consumidores / ML Pipelines
```

- **Scraping:** coleta título, categoria, preço, rating e disponibilidade.
- **Data Layer:** persistência local em CSV (expansível para PostgreSQL).
- **API:** disponibilização dos dados com filtros e busca.
- **JWT:** rotas de administração acessíveis apenas com token.

Diagramas (entregues nesta fase):  
```
/docs/arquitetura-atual-c4-nivel-3.png
/docs/arquitetura-atual-c4-nivel-3.svg
```

## Estrutura do Projeto

### API

```
api/
├── pyproject.toml
├── render.yaml
├── README.md
├── uv.lock
│
└── src/
    └── fiap_eml_api/
        ├── __init__.py
        ├── api_main.py                      # Entrypoint da API
        ├── data_base.py                     # Conexão / Adaptador de dados
        ├── security_core.py                 # Regras de autorização/segurança
        │
        ├── auth_jwt.py                      # Autenticação e geração de JWT
        │
        ├── api_books.py                     # Listagem e filtros de livros
        ├── api_id_book_core.py              # Detalhes por ID
        ├── api_categories.py                # Listagem de categorias
        ├── api_title_or_categorie.py        # Busca refinada (título + categoria)
        ├── api_health_core.py               # Health check / status da API
        │
        ├── api_opcional_overview.py               # Estatísticas gerais dos livros
        ├── api_opcional_categories.py             # Estatísticas por categoria
        ├── api_opcional_books_best_rated.py       # Livros com melhor avaliação
        └── api_opcional_books_price_range.py      # Filtro por faixa de preço
```

### Scripts / Scraping

```
scripts/
├── data/                               # Diretório para armazenar a base gerada
│   └── books_to_scrape.csv             # Arquivo CSV após o scraping (gerado em runtime)
│
├── scrape_books.py                     # Script de Web Scraping (BooksToScrape → CSV)
└── save_books_to_postgres.py           # Script de carga (CSV → Banco) / opcional
```

## Instalação e Execução

### Requisitos
- Python 3.13
- Gerenciamento de Dependencias `uv`

### Instalar dependências
```bash
uv sync
```

### Executar API
```bash
uv run uvicorn fiap_eml_api.api_main:app --reload
```

### Documentação (Desenvolvimento e Produtivo)

Após iniciar o servidor, acesse no navegador para o ambiente de desenvolvimento:

- Swagger UI: http://localhost:8000/
- ReDoc: http://localhost:8000/redoc

A API está publicada no ambiente de produção através do Render como ambiente produtivo:

- Produção (Swagger): https://fiap-eml-tech-challenger-fase-1.onrender.com
- Produção (ReDoc): https://fiap-eml-tech-challenger-fase-1.onrender.com/redoc

## Endpoints Principais

### Obrigatórios

|  Método | Rota                                     | Descrição                                             |
| :-----: | ---------------------------------------- | ----------------------------------------------------- |
| **GET** | `/api/v1/books/categories`               | Lista todas as categorias disponíveis                 |
| **GET** | `/api/v1/books/id/{book_id}`             | Busca livro por **ID** (formato UUID ou hash interno) |
| **GET** | `/api/v1/books/filters?title=&category=` | Lista livros filtrando por título e/ou categoria      |
| **GET** | `/api/v1/health`                         | Verifica se a API está ativa (Health Check)           |
| **GET** | `/api/v1/books`                          | Lista todos os livros disponíveis (com paginação)     |

### Opcionais

|  Método | Rota                                  | Descrição                                                                                     |
| :-----: | ------------------------------------- | --------------------------------------------------------------------------------------------- |
| **GET** | `/api/v1/stats/overview`              | Exibe estatísticas gerais da coleção (média de preço, média de rating, total de livros, etc.) |
| **GET** | `/api/v1/stats/categories`            | Estatísticas agregadas por categoria (ex.: contagem de livros, preço médio)                   |
| **GET** | `/api/v1/books/best-rated`            | Lista livros com **melhor avaliação** (rating mais alto)                                      |
| **GET** | `/api/v1/books/price-range?min=&max=` | Lista livros filtrando por **faixa de preço** (min/max)                                       |

### Autenticação (JWT)

|  Método  | Rota                   | Descrição                                                      |
| :------: | ---------------------- | -------------------------------------------------------------- |
| **POST** | `/api/v1/auth/login`   | Gera um **Access Token (JWT)** a partir de credenciais válidas |
| **POST** | `/api/v1/auth/refresh` | Gera um novo token JWT a partir de um Refresh Token            |



## Autenticação JWT (Entregue)

| Método | Rota                | Descrição |
|-------:|---------------------|-----------|
| POST   | `/api/v1/auth/login` | Geração de token JWT |

Exemplo:
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin"}'
```

Requisições autenticadas:
```bash
-H "Authorization: Bearer <token>"
```

## Diagrama Arquitetural (C4 – Nível 3)

Os arquivos se encontram em `/docs`.

O diagrama reflete:
- Separação entre **API**, **Data Layer** e **Scraping**.
- Fluxo de consulta e ingestão.
- Expansão natural para **feature store** + pipelines de ML na próxima fase.

## Status da Entrega

| Item | Status |
|------|:------:|
| Web Scraping funcionando | OK |
| CSV gerado e persistido | OK |
| API REST documentada | OK |
| Autenticação JWT | OK |
| Diagrama Arquitetural C4 N3 | OK |

## Próxima Fase (Fase 2 — ML)

- Análise exploratória (EDA)
- Feature Engineering
- Treinamento e avaliação de modelos
- Versionamento de datasets e modelos
- Pipeline de inferência (serving)
