import httpx 
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin

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

def parse_page(html):
    books = html.css("article.product_pod") #target all books
    
    # loop through books and print urls
    for book in books: 
        yield urljoin("https://books.toscrape.com/catalogue/", book.css_first("h3 > a").attributes["href"])


def main():
    base_url = "https://books.toscrape.com"
    for i in range(2, 3): #pages 1 and 2
        print(f"Getting urls from page {i}")
        html = get_html(base_url, page_num=i)
        if html is False:
            break
        book_urls = parse_page(html)
        for url in book_urls:
            print(url)
            html = get_html(url)
            print(html.css_first("title").text())
            time.sleep(1)

if __name__ == "__main__":
    main()