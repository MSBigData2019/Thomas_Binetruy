from bs4 import BeautifulSoup
import urllib
import requests
import json
import pandas as np

def get_html(url):
    page = requests.get(url)
    return page.text


def get_city_coords(url):
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    lines = soup.select("table.V2 > tr")[1:51]
    coords = [(l.select("td:nth-of-type(2)")[0].text, float(l.select("td:nth-of-type(4)")[0].text), float(l.select("td:nth-of-type(5)")[0].text)) for l in lines]
    return coords

import math
def create_matrix(coords):
    result = []
    for c1 in coords:
        line = []
        for c2 in coords:
            line.append(math.sqrt((c1[1] - c2[1])**2 + (c1[2] - c2[2])**2))

        result.append(line)
    return result

url = "http://www.tageo.com/index-e-fr-cities-FR.htm"
coords = get_city_coords(url)
result = create_matrix(coords)

df = np.DataFrame(result)
df.columns = [c[0] for c in coords]
df.index = [c[0] for c in coords]
print(df)
