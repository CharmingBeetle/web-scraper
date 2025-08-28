import httpx 
from selectolax.parser import HTMLParser

# web scraper tutorial

url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}

response = httpx.get(url, headers=headers) 
# print(response.text) #text of url request

html = HTMLParser(response.text) # query this to find data you want

# print(html.css_first("title").text()) #finds first css selector matching title

# function to extract text, if no text, return none
def extract_text(html, selector, attribute=None):
    try:
        if attribute: 
            return html.css_first(selector).attributes[attribute]
        else:
            return html.css_first(selector).text()
    except AttributeError:
        return None
books = html.css("article.product_pod") #target all books
# print(books)

# loop through books and print title
for book in books: 
    # print(book.css_first("h3 > a").text())

  #create item dictionary
    item = {
        "name": extract_text(book, "h3 > a"),
        "price": extract_text(book, "p.price_color"),
        "rating": extract_text(book, "p.star-rating"),
        "url": extract_text(book, "h3 > a", "href")
    }
    print(item)