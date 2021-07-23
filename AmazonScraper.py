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
import random
from itertools import cycle
from collections import OrderedDict

pd.set_option('max_colwidth', 100)

start = time.time()

headers = {
    'authority': 'www.amazon.com',
    'cache-control': 'max-age=0',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en',
    'cookie': 'session-id=136-3434355-8443447; session-id-time=2082787201l; i18n-prefs=USD; ubid-main=130-5400322-5004345; session-token=lbUCMi0x35HwJMg5rq/1EoWij4QWanmPiN7wRT63SgmNFJH5SK7Z17tmhhdBp2olEERr/3zH7BwsZr1tIuJuIB73sWH2QHEVJoeXEcSLw0Ny0lNeHNHx2VpaqYAs61s0DM3Mf/bhTP80s6Bp7IOUAQ9mfrEnVbNMmKa/I5p8xNrVOui7rsxYCXTSgWA9Jw3B; skin=noskin; csm-hit=tb:YXV8HKAP79ZW3NS5WF2X+s-DEQJF2CSWSHZ8JZYFFWV^|1627005070626&t:1627005070626&adb:adblk_no',
}

# response = requests.get('https://www.amazon.com/', headers=headers)

f = open(r"C:\Users\Lenovo\Desktop\ProxiesPool\ProxiesPool(SOCKS4).txt",'r', encoding='utf-8')
proxies = f.read().split("\n")

for i in range(len(proxies)):
    proxies[i] = 'socks4://' + proxies[i]

proxies_pool = cycle(proxies)
print(proxies_pool)

"""
Proxies Testing 
"""

url = 'https://httpbin.org/ip'
for i in range(len(proxies)):
    # Get a proxy from the pool
    proxy = next(proxies_pool)
    print("Request #%d" % i)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
        print(response.json())
    except:
        print("Skipping. Connnection error")

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

url = 'https://httpbin.org/headers'
for i in range(0, 4):
    # Pick a random user agent
    user_agent = random.choice(user_agent_list)
    # Set the headers
    headers = {'User-Agent': user_agent}
    # Make the request
    response = requests.get(url, headers=headers)
    print("Request #%d\nUser-Agent Sent:%s\n\nHeaders Recevied by HTTPBin:" % (i, user_agent))
    print(response.json())
    print("-------------------")

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
