import csv
import psycopg2
from psycopg2.extras import execute_batch
from decimal import Decimal

# --------------------------------------------
# CONFIGURAÇÕES DO BANCO DE DADOS
# --------------------------------------------
DB_CONFIG = {
    "host": "201.23.68.219",
    "port": 5432,
    "dbname": "fiap_eml_db",
    "user": "postgres",
    "password": "(Pk3LfT7N;P5zfPc"
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

# --------------------------------------------
# FUNÇÃO PRINCIPAL
# --------------------------------------------
def insert_books_from_csv(csv_file_path):
    connection = None
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        cursor = connection.cursor()

        with open(csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []

            for row in reader:
                # Limpeza e conversão dos dados
                title = row["title"].strip()
                book_url = row["book_url"].strip()
                category = row.get("category", "").strip() or None
                price_str = row["price"].replace("£", "").strip()
                price = Decimal(price_str) if price_str else Decimal("0.00")
                availability = row["availability"].strip()
                rating = convert_rating(row["rating"].strip()) if row["rating"] else None
                image_url = row.get("image_url", "").strip()

                rows.append((
                    title,
                    book_url,
                    category,
                    price,
                    availability,
                    rating,
                    image_url
                ))

        # --------------------------------------------
        # INSERT EM LOTE (com categoria)
        # --------------------------------------------
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