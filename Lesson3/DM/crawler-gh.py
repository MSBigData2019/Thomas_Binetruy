# exo py

from bs4 import BeautifulSoup
import urllib
import requests
import json

def get_html(url):
    url += "?access_token=28a6b44efb37db97905de2665eb7473a073bc60a"
    page = requests.get(url)
    return page.text

def get_usernames(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.select(".entry-content > table")[0]
    trs = table.select("tr")
    links = [tr.select("td:nth-of-type(1) > a") for tr in trs]
    return [a[0].text for a in links if len(a) > 0]

def get_star_avgs():
    url = "https://gist.github.com/paulmillr/2657075"
    usernames = get_usernames(url)
    star_avgs = []

    for u in usernames:
        print(u)
        url = f"https://api.github.com/users/{u}/repos"
        repos = json.loads(get_html(url))
        stars = [r["stargazers_count"] for r in repos]
        avg = 0
        if(len(stars)):
            avg = sum(stars) / len(stars)
        star_avgs.append([u, avg])

    return star_avgs

def order_results(result):
    result.sort(key=lambda x: x[1], reverse=True)
    return 0

def print_result(result):
    for r in result:
        print(r[0], ": ", r[1])

result = get_star_avgs()
order_results(result)
print_result(result)
