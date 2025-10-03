import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

def scrape_book_list(page_url):
    """
    Extrai a lista de livros de uma página de catálogo,
    retornando dados básicos (título, link para página do livro, preço, disponibilidade).
    """
    resp = requests.get(page_url)
    resp.encoding = "utf-8"  # força encoding UTF-8
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    books = []
    for art in soup.select('article.product_pod'):
        title = art.h3.a['title']
        href = art.h3.a['href']
        book_url = urljoin(page_url, href)
        price = art.select_one('p.price_color').text.strip()
        availability = art.select_one('p.instock.availability').text.strip()
        rating_classes = art.select_one('p.star-rating')['class']
        rating = next((cls for cls in rating_classes if cls != "star-rating"), None)

        books.append({
            'title': title,
            'book_url': book_url,
            'price': price,
            'availability': availability,
            'rating': rating
        })
    return books

"""
O metodo possui 3 parametros, para customizacao da execução da coleta de dados
1. start_url = Qual a página de inicio da coleta de dados
2. Quantidade máxima de páginas por coleta
3. Tempo de 'Think Time', tempo entre cada coleta de dados
"""
def scrape_all_books(start_url, max_pages=50, delay=1.0):

    """
    Vetor que irá armazenar dados do item
    """
    all_books = []

    base = start_url.rstrip('/').rsplit('/', 1)[0] + '/catalogue/page-{}.html'

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

"""
Metodo responsavel por armazenar os registros do vetor para o arquivo CSV
"""
def save_to_csv(books, filename='books.csv'):
    if not books:
        return
    keys = books[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as f:  # força UTF-8 na gravação, estava com problemas de enconding, ou seja, caracteres especiais
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(books)

"""
Metodo de inicializacao do programa em python
"""
if __name__ == '__main__':
    start = 'https://books.toscrape.com/index.html'
    books = scrape_all_books(start, max_pages=50, delay=1.0)
    print(f"Total de registros coletados: {len(books)}")
    if books:
        save_to_csv(books, 'books_to_scrape.csv')
    print("Coleta de dados realizada com sucesso.")