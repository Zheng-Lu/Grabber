import random

from selenium import webdriver
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

pro = ['172.104.60.128',
    '15.161.145.56',
    '213.137.240.243',
    "106.14.63.8",
    "54.93.222.189",
    "187.19.207.195",
    "46.101.218.6",
    "111.1.36.132",
    "106.75.236.60",
    "196.38.150.104",
    "104.238.195.10",
    "95.179.158.20"]

proxies = {
  "http": random.choice(pro)
}

headers = {
        'cookies': r'datr=yF3OX00R3Q9QQI3t2ncMcCzd; sb=N6bPXx4TxMATSE2z2Es7DfiJ; c_user=100022895093344; dpr=1.100000023841858; xs=6%3AfdfK3NsCrmtX-g%3A2%3A1619512889%3A-1%3A8701%3A%3AAcUlBiLEmTZGlRBnl9PLRXfj5MdObGUP3SGyVNwKpA; fr=1PFn62W1XOXeFE0ZL.AWXtlAC3AnPisPsX6P-SMx82wMU.Bg7aGY.sz.GDu.0.0.Bg7aGY.; spin=r.1004113928_b.trunk_t.1626335699_s.1_v.2_',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
    }

path = r"C:\Users\Lenovo\Desktop\Flash Deals - Shop Cheap Flash Deals from China Flash Deals Suppliers at cryptographic Official Store on Aliexpress.com - (2021_7_16 下午7_53_36).html"
html = 'https://cryptographic.aliexpress.com/store/group/Flash-Deals/619765_512731262.html'
login_page ='https://login.aliexpress.com/?from=sm&return_url=https%3A%2F%2Fcryptographic.aliexpress.com%2Fstore%2Fgroup%2FFlash-Deals%2F619765_512731262.html%3Fspm%3Da2g0o.store_pc_groupList.0.0.596a5cc4e8wnb6&uuid=689dbedbc6fd5c25a11d52c7c2784ed1'
htmlfile = open(path, 'r', encoding='utf-8')
htmlhandle = htmlfile.read()

aliExpress = pd.read_excel("C://Users//Lenovo//Desktop//AliURL.xlsx", usecols=['url'])
df = pd.DataFrame(aliExpress)

urls = []
# for row in df.iterrows():
#     row[1].values
#     urls.append(list(row[1]))

for row in df.iterrows():
    urls.append(row[1].to_string().replace("url    ",''))


# browser = webdriver.Chrome()
# browser.maximize_window()  # 最大化窗口
# wait = WebDriverWait(browser, 10) # 等待加载10s
#
# def login():
#     browser.get('https://www.gigab2b.com/index.php?route=account/login')
#     input = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//input[@id="input-email"]')))
#     input.send_keys('demo@buyer.com')
#     input = wait.until(EC.presence_of_element_located(
#         (By.XPATH, '//input[@id="input-password"]')))
#     input.send_keys('0325#Test@BB')
#     submit = wait.until(EC.element_to_be_clickable(
#         (By.XPATH, '//input[3]')))
#     submit.click()  # 点击登录按钮

def scrapeData(url):
    # Download the page using requests
    r = requests.get(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    #soup = BeautifulSoup(htmlhandle, 'html.parser')
    data = soup.findAll('span',{'class':'product-price-value'})
    #title = soup.find(id='price_total').get_text().strip()
    return data

price = []

for url in urls:
    print(url)
    price.append(scrapeData(url))

print(price)


#print(scrapeData(html))

# r = requests.get(login_page, headers=headers,proxies=proxies)
# soup = BeautifulSoup(r.content, features="lxml")
# print(soup.findAll('fm-login-id'))