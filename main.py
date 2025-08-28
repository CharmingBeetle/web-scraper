import httpx 
from selectolax.parser import HTMLParser

# web scraper tutorial

url = "https://books.toscrape.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"}

response = httpx.get(url, headers=headers) 
# print(response.text) #text of url request

html = HTMLParser(response.text) # query this to find data you want

# print(html.css_first("title").text()) #finds first css selector matching title

books = html.css("article.product_pod") #target all books
# print(books)

# loop through books and print title
for book in books: 
    # print(book.css_first("h3 > a").text())

  #create item dictionary
    item = {
        "name": html.css_first("h3 > a").text(),
        "price": html.css_first("p.price_color").text(),
        "rating": html.css_first("p.star-rating").text(),
        "url": html.css_first("h3 > a").attributes["href"]
    }
    print(item)