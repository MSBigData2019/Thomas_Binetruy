# Crawler v1
import unittest
from bs4 import BeautifulSoup

import urllib

def get_html(url):
    data = urllib.request.urlopen(url)
    html = ""
    for line in data.readlines():
        html += line.__str__()
    return html

def get_sales(soup):
    # st = document.querySelectorAll(".module:nth-of-type(2)")
    sales_table = soup.find_all(class_="module")[2]

    # lqs = st.querySelectorAll("tr:nth-of-type(3)")[0]
    last_quarter_sales = sales_table.find_all("tr")[2]

    # sm = st.querySelectorAll("td:nth-of-type(3)")[0]
    str_sales_mean = last_quarter_sales.find_all("td")[2].text
    str_sales_high = last_quarter_sales.find_all("td")[3].text
    str_sales_low = last_quarter_sales.find_all("td")[4].text

    # Reuters uses string as thousands' delimiter
    # which cannot be parsed by float()
    sales_mean = float(str_sales_mean.replace(",", ""))
    sales_high = float(str_sales_high.replace(",", ""))
    sales_low = float(str_sales_low.replace(",", ""))

    return [sales_mean, sales_high, sales_low]



url = "https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA"
class Tests(unittest.TestCase):
    soup = BeautifulSoup(get_html(url), 'html.parser')

    def test_last_quarter_sales(self):
        answer = [13667.7, 13769.0, 13575.0]
        result = get_sales(self.soup)
        for i in range(0, len(answer)):
            self.assertEqual(answer[i], result[i])

Tests().test_last_quarter_sales()
