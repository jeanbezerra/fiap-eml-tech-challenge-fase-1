import csv
import logging
from pathlib import Path

# Configuração de log (com timestamp para auditoria)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline_audit.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

CSV_FILE = Path("books_to_scrape.csv")


def step_load_csv(file_path: Path):
    """Etapa 1 - Carregar o CSV."""
    logging.info("Iniciando etapa: Carregar CSV")
    rows = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    logging.info(f"Total de linhas carregadas: {len(rows)}")
    return rows


def step_filter_by_price(rows, threshold=30.0):
    """Etapa 2 - Filtrar livros por preço (maior que threshold)."""
    logging.info(f"Iniciando etapa: Filtrar livros com preço > {threshold}")
    filtered = []
    for row in rows:
        price = float(row["price"].replace("£", "").strip())
        if price > threshold:
            filtered.append(row)
    logging.info(f"Total após filtro de preço: {len(filtered)}")
    return filtered


def step_filter_by_availability(rows):
    """Etapa 3 - Manter apenas os livros disponíveis em estoque."""
    logging.info("Iniciando etapa: Filtrar livros em estoque")
    available = [row for row in rows if "In stock" in row["availability"]]
    logging.info(f"Total após filtro de disponibilidade: {len(available)}")
    return available


def step_group_by_rating(rows):
    """Etapa 4 - Agrupar livros por rating."""
    logging.info("Iniciando etapa: Agrupar por rating")
    groups = {}
    for row in rows:
        rating = row["rating"]
        groups.setdefault(rating, []).append(row)
    for rating, books in groups.items():
        logging.info(f"Livros que possuem classificação {rating}: {len(books)} livros")
    return groups


def run_pipeline():
    """Executa todas as etapas na ordem (simulando um DAG)."""
    logging.info("===== INICIANDO PIPELINE =====")
    rows = step_load_csv(CSV_FILE)
    rows = step_filter_by_price(rows, threshold=30.0)
    rows = step_filter_by_availability(rows)
    grouped = step_group_by_rating(rows)
    logging.info("===== PIPELINE CONCLUÍDO =====")
    return grouped


if __name__ == "__main__":
    resultado = run_pipeline()