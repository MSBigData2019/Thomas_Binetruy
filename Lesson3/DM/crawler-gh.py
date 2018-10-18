# exo py

from bs4 import BeautifulSoup
import urllib
import requests

def get_html(url):
    headers = {'User-Agent':'Mozilla/5.0'}
    page = requests.get(url)
    return page.text



def get_usernames(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select(".entry-content > table")[0]
    trs = table.select("tr")
    links = [tr.select("td:nth-of-type(1) > a") for tr in trs]
    return [a[0].text for a in links if len(a) > 0]

url = "https://gist.github.com/paulmillr/2657075"
usernames = get_usernames(url)
print(usernames)
