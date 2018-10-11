# Crawler v1
from bs4 import BeautifulSoup as bs

import urllib

url = "http://www.google.com"
data = urllib.request.urlopen(url)
html = ""
for line in data.readlines():
    html += line.__str__()

print(html)

