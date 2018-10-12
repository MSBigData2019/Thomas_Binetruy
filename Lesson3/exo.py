from bs4 import BeautifulSoup
import urllib
import requests

def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    page = requests.get(url)
    return page.text

url1 = "https://www.darty.com/nav/extra/list?p=200&s=def&cat=26055&m="
url2 = "&o="
def parse_page(page_number, brand):
    url = url1 + brand + url2
    html = get_html(url + str(page_number))
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.select(".darty_prix")
    result = [r.text.replace("€", "").replace(",", ".").replace("*", "").replace("\xa0", "") for r in result]

    return [float(r) for r in result]

def get_avg_price(models):
    pages = [0,200]
    result = []
    for m in models:
        prices = []
        for p in pages:
            prices += parse_page(p, m)

        result.append(sum(prices) / len(prices))

    return result


print(get_avg_price(["ACER", "DELL"]))

