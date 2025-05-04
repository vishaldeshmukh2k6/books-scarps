import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

def get_categories():
    html_content = requests.get("https://books.toscrape.com/").content
    soup = BeautifulSoup(html_content, 'html.parser')
    main_div = soup.find("div", class_="side_categories")
    c_list = main_div.find_all('ul')[1].find_all("li")
    categories = list(map(lambda c: c.text.strip(), c_list))
    return categories 

def get_books(categories):
    z = 2
    for x in categories:
        url = f"https://books.toscrape.com/catalogue/category/books/{x.lower().replace(' ', '-')}_{z}/index.html"
        categoryss = requests.get(url).content
        soup = BeautifulSoup(categoryss, "html.parser")
        main_ol = soup.find("ol", class_ = "row")
        all_list = main_ol.find_all("li")
        books = []

        z = z + 1
        for c in all_list:
            BASE_URL = "https://books.toscrape.com/"
            book  = {}
            book['title'] = c.find("img").get("alt")
            book['price'] = c.find("div", class_="product_price").find("p").text
            book['image_url'] = BASE_URL + c.find('img')['src'].replace('../', '')
            book['book_url'] = BASE_URL + "catalogue/" + c.select_one('h3 a')['href'].replace('../../../', '')
            books.append(book)

        with open("books/"+x+".json", "w+") as f:
            json.dump(books, f, indent=4)


categories = get_categories()
get_books(categories)

