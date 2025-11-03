import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

def scrape_book_details(book_url):
    """
    Acessa a página individual de um livro e extrai:
      - Link absoluto da imagem
      - Categoria do breadcrumb
    """
    try:
        resp = requests.get(book_url)
        resp.encoding = "utf-8"
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # Extrai a imagem principal
        img_tag = soup.select_one("div.item.active img")
        full_img_url = urljoin(book_url, img_tag["src"]) if img_tag else "N/A"

        # Extrai a categoria (segundo item do breadcrumb)
        breadcrumb = soup.select("ul.breadcrumb li a")
        category = breadcrumb[2].get_text(strip=True) if len(breadcrumb) > 2 else "N/A"

        return full_img_url, category

    except Exception as e:
        print(f"[WARN] Falha ao obter detalhes de {book_url}: {e}")
        return None, "N/A"


def scrape_book_list(page_url):
    """
    Extrai a lista de livros de uma página de catálogo,
    incluindo categoria e imagem individual.
    """
    resp = requests.get(page_url)
    resp.encoding = "utf-8"
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    books = []

    for art in soup.select("article.product_pod"):
        title = art.h3.a["title"]
        href = art.h3.a["href"]
        book_url = urljoin(page_url, href)
        price = art.select_one("p.price_color").text.strip()
        availability = art.select_one("p.instock.availability").text.strip()
        rating_classes = art.select_one("p.star-rating")["class"]
        rating = next((cls for cls in rating_classes if cls != "star-rating"), None)

        # Busca imagem e categoria
        image_url, category = scrape_book_details(book_url)

        books.append({
            "title": title,
            "book_url": book_url,
            "category": category,
            "price": price,
            "availability": availability,
            "rating": rating,
            "image_url": image_url or "N/A"
        })

    return books


def scrape_all_books(start_url, max_pages=50, delay=0.1):
    """
    Percorre todas as páginas e agrega os resultados em uma única lista.
    """
    all_books = []
    base = start_url.rstrip("/").rsplit("/", 1)[0] + "/catalogue/page-{}.html"

    for i in range(1, max_pages + 1):
        page_url = base.format(i)
        print(f"Scraping página {i} → {page_url}")
        try:
            books = scrape_book_list(page_url)
        except requests.HTTPError as e:
            print("Erro HTTP:", e)
            break
        if not books:
            print("Nenhum livro encontrado — fim das páginas.")
            break
        all_books.extend(books)
        time.sleep(delay)
    return all_books


def save_to_csv(books, filename="books_to_scrape.csv"):
    """
    Salva os dados coletados em um arquivo CSV com codificação UTF-8.
    """
    if not books:
        return
    keys = books[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)


if __name__ == "__main__":
    start = "https://books.toscrape.com/index.html"
    books = scrape_all_books(start, max_pages=50, delay=0.1)
    print(f"Total de registros coletados: {len(books)}")
    if books:
        save_to_csv(books, "./data/books_to_scrape.csv")
    print("Coleta de dados realizada com sucesso.")