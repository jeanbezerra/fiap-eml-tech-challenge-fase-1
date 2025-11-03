import os
import concurrent.futures
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


def scrape_all_books(start_url, max_pages=50, max_workers=8):
    """
    Percorre todas as páginas em paralelo e agrega os resultados.
    """
    all_books = []
    base = start_url.rstrip("/").rsplit("/", 1)[0] + "/catalogue/page-{}.html"

    page_urls = [base.format(i) for i in range(1, max_pages + 1)]

    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(scrape_book_list, url): url for url in page_urls}

        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                books = future.result()
                if books:
                    all_books.extend(books)
            except requests.HTTPError as e:
                print(f"Erro HTTP em {url}: {e}")

    elapsed = time.time() - start_time
    print(f"Coleta finalizada: {len(all_books)} livros em {elapsed:.2f}s (threads={max_workers})")
    return all_books


def save_to_csv(books, filename="./data/books_to_scrape.csv"):
    """
    Salva os dados coletados em um arquivo CSV com codificação UTF-8.
    Cria automaticamente o diretório de destino, trata erros de I/O
    e exibe mensagens de status.
    """
    if not books:
        print("Nenhum dado para salvar.")
        return

    # Garante que o diretório existe
    output_dir = os.path.dirname(filename)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()
    try:
        keys = books[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(books)

        elapsed = time.time() - start_time
        print(f"Arquivo salvo com sucesso: {filename}")
        print(f"Total de registros: {len(books)} | Tempo: {elapsed:.2f}s")

    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")



if __name__ == "__main__":
    start = "https://books.toscrape.com/index.html"
    books = scrape_all_books(start, max_pages=50)
    print(f"Total de registros coletados: {len(books)}")

    if books:
        save_to_csv(books, "./data/books_to_scrape.csv")

    print("Coleta de dados finalizada com sucesso.")