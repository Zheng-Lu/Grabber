from scrapy import Spider, Request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
from lxml.html import fromstring
from urllib.parse import urlencode
from urllib.parse import urljoin
import scrapy
import re
import requests
import json
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

pd.set_option('max_colwidth', 100)

start = time.time()

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36',
}


def getSoup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def getProducts(soup):

    # retrieving the list of product titles
    try:
        titles = soup.findAll('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
        title = []
        for t in titles:
            title.append(t.get_text())

    except AttributeError:
        title.append('N/A')

    # retrieving the list of product prices
    try:
        prices = soup.findAll('span', attrs={'class': 'a-offscreen'})
        price = []
        for p in prices:
            price.append(p.get_text())
    except AttributeError:
        price.append('N/A')



    # retrieving the list of the urls of product cover pictures
    try:
        pics = soup.findAll('img', attrs={'class': 's-image'})
        pic = []
        for p in pics:
            pic.append(p.get('src'))
    except AttributeError:
        pic.append('N/A')

    # retrieving the list of the urls of product
    try:
        urls = soup.findAll('a', attrs={'class': 'a-link-normal a-text-normal'})
        url = []
        for u in urls:
            url.append(u.get('href'))
    except AttributeError:
        url.append('N/A')

    data = {
        'Title': title,
        'Price': price,
        'Pic URL': pic,
        'Prodcut URL': url
    }

    return data


end = time.time()
print('Time taken: ' + str(round(end - start, 2)) + 's')
