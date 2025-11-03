import os
import csv
import psycopg2
from psycopg2.extras import execute_batch
from decimal import Decimal, InvalidOperation

# --------------------------------------------
# CONFIGURAÇÕES DO BANCO DE DADOS (via variáveis de ambiente)
# --------------------------------------------
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "fiap_eml_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "postgres")
}

# --------------------------------------------
# MAPA DE CONVERSÃO DE RATING (texto → número)
# --------------------------------------------
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


def convert_rating(rating_str):
    """Converte o rating textual ('Three', 'Five') para número inteiro."""
    return RATING_MAP.get(rating_str, None)


def parse_price(value: str) -> Decimal:
    """
    Converte o preço em Decimal de forma segura.
    Remove símbolos, converte vírgulas e trata erros.
    """
    if not value:
        return Decimal("0.00")

    cleaned = value.strip().replace("£", "").replace(",", ".")
    try:
        return Decimal(cleaned)
    except (InvalidOperation, ValueError):
        print(f"Valor de preço inválido detectado: '{value}', usando 0.00")
        return Decimal("0.00")


# --------------------------------------------
# FUNÇÃO PRINCIPAL
# --------------------------------------------
def insert_books_from_csv(csv_file_path):
    connection = None
    try:
        print(f"Conectando ao banco: {DB_CONFIG['host']}:{DB_CONFIG['port']} / {DB_CONFIG['dbname']}")
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # 1. Limpa a tabela antes de inserir novos dados
        print("Removendo registros existentes da tabela book_scraping_data...")
        cursor.execute("DELETE FROM public.book_scraping_data;")
        connection.commit()
        print("Tabela limpa com sucesso.")

        # 2. Lê o CSV e prepara os dados
        with open(csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []

            for row in reader:
                try:
                    title = row["title"].strip()
                    book_url = row["book_url"].strip()
                    category = row.get("category", "").strip() or None
                    price = parse_price(row.get("price", ""))
                    availability = row.get("availability", "").strip()
                    rating = convert_rating(row.get("rating", "").strip()) if row.get("rating") else None
                    image_url = row.get("image_url", "").strip()

                    # Ignora registros com preço zero
                    if price == Decimal("0.00"):
                        continue

                    rows.append((
                        title,
                        book_url,
                        category,
                        price,
                        availability,
                        rating,
                        image_url
                    ))

                except Exception as row_err:
                    print(f"Erro ao processar linha: {row_err}")

        if not rows:
            print("Nenhum dado válido encontrado para inserção.")
            return

        # 3. Inserção em lote
        insert_query = """
            INSERT INTO public.book_scraping_data
                (title, book_url, category, price, availability, rating, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        execute_batch(cursor, insert_query, rows, page_size=100)
        connection.commit()

        print(f"Inserção concluída com sucesso — {len(rows)} registros salvos.")

    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Conexão com o banco encerrada.")


# --------------------------------------------
# EXECUÇÃO DIRETA
# --------------------------------------------
if __name__ == "__main__":
    insert_books_from_csv("./data/books_to_scrape.csv")