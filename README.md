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

```
.
├── api/
│   ├── api_main.py                         # Entrypoint da API
│   ├── api_books.py                        # Listagem e filtros de livros
│   ├── api_categories.py                   # Categorias disponíveis
│   ├── api_id_book_core.py                 # Detalhe por ID
│   ├── api_title_or_categorie.py           # Busca refinada
│   ├── api_health_core.py                  # Health Check
│   ├── api_auth_jwt.py                     # Login e autenticação JWT
│   └── data_base.py                        # Adaptação de acesso a dados (DB opcional)
│
├── scripts/
│   └── scrape_books.py                     # Coleta automatizada
│
├── data/
│   └── books_to_scrape.csv                 # Base local gerada
│
├── docs/
│   └── arquitetura-atual-c4-nivel-3.png
│   └── arquitetura-atual-c4-nivel-3.svg
│
├── pyproject.toml
└── README.md
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
uv run uvicorn api.api_main:app --reload
```

### Documentação (Swagger)
```
http://localhost:8000/docs
```

## Endpoints Principais

| Método | Rota                                                | Descrição |
|-------:|-----------------------------------------------------|-----------|
| GET    | `/api/v1/health`                                    | Status da API |
| GET    | `/api/v1/books`                                     | Lista paginada de livros |
| GET    | `/api/v1/books/{id}`                                | Detalhe por ID |
| GET    | `/api/v1/books/search?title=&category=`             | Busca refinada |
| GET    | `/api/v1/categories`                                | Lista de categorias |

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
