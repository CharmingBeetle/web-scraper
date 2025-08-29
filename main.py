import httpx 
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import dataclass, asdict

@dataclass
class Item:
    title: str | None
    price: str | None
    rating: str | None
    stock: str | None  
    description: str | None

# web scraper tutorial
def get_html(url, **kwargs): #keyword arguments is a dictionary
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }
    
    if kwargs.get("page_num"):
        page_url = f"{url}/catalogue/page-{kwargs.get('page_num')}.html"
        response = httpx.get(page_url, headers=headers, follow_redirects=True)  
        print(response.status_code)
    else: 
        response = httpx.get(url, headers=headers, follow_redirects=True)  

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.Page limit exceeded")
        return False #returns false if page limit exceeded
    html = HTMLParser(response.text) # query this to find data you want
    return html

# function to extract text, if no text, return none
def extract_text(html, selector, attribute=None):
    try:
        if attribute: 
            return html.css_first(selector).attributes[attribute]
        else:
            return html.css_first(selector).text()
    except AttributeError:
        return None

# function to get rating class
def extract_rating(html, selector):
    try:
        element = html.css_first(selector)
        class_attr = element.attributes.get('class')
        # print(class_attr, ">>>>>CLASS ATTR")
        
        if len(class_attr.split()) == 2: 
            return class_attr.split()[1]
        else:
            return None
    except AttributeError:
        return None

def extract_stock(html, selector):
    try:
        element = html.css_first(selector)
        if element:
            stock_text = element.text()
            start = stock_text.find("(") + 1 #position of number start
            end = stock_text.find(" available") #position of number end
            if start > 0 and end > start: 
                return stock_text[start:end] #value of number position
            return stock_text
        return None
    except AttributeError:
        return None

def parse_results_page(html):
    books = html.css("article.product_pod") #target all books
    
    # loop through books and print urls
    for book in books: 
        yield urljoin("https://books.toscrape.com/catalogue/", book.css_first("h3 > a").attributes["href"])

def parse_book_page(html: HTMLParser):
    new_book = Item(
        title=extract_text(html, "h1"),
        price=extract_text(html, "p.price_color"),
        rating=extract_rating(html, "p.star-rating"),
        stock=extract_stock(html, "p.instock.availability"),
        description=extract_text(html, "div#product_description ~ p")
    )
    return new_book

def main():
    books = []
    base_url = "https://books.toscrape.com"
    for i in range(2, 3):
        print(f"Getting urls from page {i}")
        html = get_html(base_url, page_num=i)
        if html is False:
            break
        book_urls = parse_results_page(html)
        for url in book_urls:
            print(url)
            html = get_html(url)
            books.append(parse_book_page(html))
            time.sleep(0.5)

    for book in books:
        print(asdict(book))

if __name__ == "__main__":
    main()