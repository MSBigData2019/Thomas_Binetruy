# -*- coding: utf-8 -*-
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

    sales_stats = []
    indexes = [2, 3, 4]
    for i in indexes:
        string = last_quarter_sales.find_all("td")[i].text
        sales_stats.append(float(string.replace(",", "")))

    return sales_stats

def get_stock_price(soup):
    # div = document.querySelectorAll(".moduleBody")[0]
    # span = div.querySelectorAll(".valueContent")[0]
    # price_str = div.querySelectorAll("span")[0]
    # change_str = div.querySelectorAll("span")[1]
    div = soup.find_all(class_="moduleBody")[0]
    span = div.find_all(class_="valueContent")[0]

    price_str = span.find_all("span")[0].text

    price_str = price_str[price_str.find("€") + 1:]
    change_str = span.find_all("span")[1].find_all("span")[0].text

    lower_bound = change_str.find("(") + 1
    upper_bound = change_str.find(")") - 1
    change_str = change_str[lower_bound:upper_bound]

    price = float(price_str)
    change = float(change_str)

    return [price, change]

def get_instit_owned_shares(soup):
    # document.querySelectorAll(".dataTable > .dataSmall")[2].querySelectorAll("td:nth-of-type(2)")[0]
    query1 =  ".dataTable > .dataSmall"
    query2 = "td:nth-of-type(2)"
    r1 = soup.select(query1)[2]
    r2 = r1.select(query2)[0]
    return float(r2.text[:-1])

def get_dividends(soup):
    q1 = soup.select(".module")[4]
    q2 = q1.select(".dataTable")[0]
    q3 = q2.select("tr:nth-of-type(2)")[0]
    q4 = q3.select('td')[1:]
    return [float(td.text) for td in q4]


url = "https://www.reuters.com/finance/stocks/financial-highlights/LVMH.PA"
class Tests(unittest.TestCase):
    soup = BeautifulSoup(get_html(url), 'html.parser')

    def test_last_quarter_sales(self, mean, high, low):
        answer = [mean, high, low]
        result = get_sales(self.soup)
        for i in range(0, len(answer)):
            self.assertEqual(answer[i], result[i])

    def test_stock_price(self, current_price, current_change):
        answer = [current_price, current_change]
        result = get_stock_price(self.soup)
        for i in range(0, len(answer)):
            self.assertEqual(answer[i], result[i])

    def test_instit(self, answer):
        result = get_instit_owned_shares(self.soup)
        self.assertEqual(result, answer)


    def test_dividend_yield(self, company, industry, sector):
        answer = [company, industry, sector]
        result = get_dividends(self.soup)
        for i in range(0, len(answer)):
            self.assertEqual(answer[i], result[i])

Tests().test_last_quarter_sales(13667.7, 13769.0, 13575)
Tests().test_stock_price(-3.35, -1.26)
Tests().test_instit(20.57)
Tests().test_dividend_yield(1.92, 1.70, 2.6)
