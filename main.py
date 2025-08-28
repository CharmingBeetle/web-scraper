import httpx 
from selectolax.parser import HTMLParser

# web scraper tutorial
def get_html(base_url, page_num):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
        }

    response = httpx.get(base_url + "/catalogue/page-" + str(page_num) + ".html", headers=headers, follow_redirects=True) 
    # print(response.status_code)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.Page limit exceeded")
        return False #returns false if page limit exceeded
    # print(response.text) #text of url request
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
   
    # book_list = []
    
    # loop through books and print title
    for book in books: 
        # print(book.css_first("h3 > a").text())

        #create item dictionary
        item = {
            "name": extract_text(book, "h3 > a"),
            "price": extract_text(book, "p.price_color"),
            "rating": extract_rating(book, "p.star-rating"),
            "url": extract_text(book, "h3 > a", "href")
        }
        # print(item)
    #     book_list.append(item)
    # return book_list # returns list of dictionaries for use later
        yield item #gives generator object to main function 

def main():
    base_url = "https://books.toscrape.com"
    for i in range(50, 100): 
        print(i)
        html = get_html(base_url, i)
        if html is False:
            break
        book_data = parse_page(html)
        for item in book_data:
            print(item) #print each item in book_data one by one

if __name__ == "__main__":
    main()