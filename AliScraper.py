import random
from scrapy import Spider,Request

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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import sys
import io

pd.set_option('max_colwidth',100)

browser = webdriver.Chrome()
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10) # 等待加载10s

upload_url = "https://adm.mixshop.world/product/add"
upload_headers = {
    'accept': '*/*',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtYWNybyIsImNyZWF0ZWQiOjE2MjY3ODIyNTc2NzQsImV4cCI6MTYyNzM4NzA1N30.shFI1w66O6cQJkoMhRvt-vgSUZXs-xit45kcp_JhSathx7-pT_mFAWBhBO9wCO7NoPPY23IPQdFDVGsBJAVbiQ',
    'Content-Type': 'application/json',
}

AliExpress_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
    }

# path = r"C:\Users\Lenovo\Desktop\Flash Deals - Shop Cheap Flash Deals from China Flash Deals Suppliers at cryptographic Official Store on Aliexpress.com - (2021_7_16 下午7_53_36).html"
# html = 'https://cryptographic.aliexpress.com/store/group/Flash-Deals/619765_512731262.html'
#
# htmlfile = open(path, 'r', encoding='utf-8')
# htmlhandle = htmlfile.read()

# aliExpress = pd.read_excel("C://Users//Lenovo//Desktop//AliURL.xlsx", usecols=['url'])
# df = pd.DataFrame(aliExpress)

urls = []
# for row in df.iterrows():
#     row[1].values
#     urls.append(list(row[1]))

# for row in df.iterrows():
#     urls.append(row[1].to_string().replace("url    ",''))

def getCookies(url):
    browser.get(url)
    cookies = browser.get_cookies()
    c = requests.cookies.RequestsCookieJar()
    for item in cookies:
        c.set(item["name"], item["value"])
    return c

def getProductBySearch(url): #This url is not a specified url of a single product
    s = requests.Session()
    s.cookies.update(getCookies(url))
    r = s.post(url, headers=AliExpress_headers)
    soup = BeautifulSoup(r.content, features="lxml")

    product_url_list = soup.findAll(attrs={"class": "_9tla3"})
    product_url = []
    for p in product_url_list:
        product_url.append(p.get('href'))

    desc = soup.findAll('img',attrs={"class": "A3Q1M"})
    title = []
    cover_url = []
    for x in desc:
        title.append(x.get('alt'))
        cover_url.append(x.get('src'))

    prices = soup.findALL('div',attrs={"class":"_12A8D"})
    price = []
    for p in prices:
        price.append(p.get_text)

    store_name = soup.findALL('a', attrs={"class": "_21sU7"})
    store=[]
    for s in store_name:
        store.append(s.get_text())

    data = {
        'Product URL': product_url,
        'title': title,
        'price': price,
        'Cover URL': cover_url,
        'Store': store
    }

    return data

def getData(url):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, executable_path=r'D:\ChromeDriver\chromedriver.exe')
    driver.get(url)
    title = driver.find_element_by_css_selector('.product-title-text')
    price = driver.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "product-price-value", " " ))]')
    img_url = driver.find_element_by_xpath('//div/img').get_attribute('src')
    product_data = {
        'title': title.text,
        'price': price.text,
        'pic': img_url
    }
    driver.quit()
    return product_data



def start_requests(self):
    for url in urls:
        yield Request(url=url, callback=self.parse, meta={'use_selenium': True}, dont_filter=True)

def scrapeData(url):
    # Download the page using requests
    r = requests.get(url, headers=AliExpress_headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    #soup = BeautifulSoup(htmlhandle, 'html.parser')
    data = soup.findAll('span')
    #title = soup.find(id='price_total').get_text().strip()

    return data




#print(scrapeData(html))

# r = requests.get(login_page, headers=headers,proxies=proxies)
# soup = BeautifulSoup(r.content, features="lxml")
# print(soup.findAll('fm-login-id'))