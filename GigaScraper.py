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

headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                 'application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Cookie': r'OCSESSID=a6feb785ecf90513e87a96299e; country=USA; currency=USD; login_flag=1; is_partner=0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'referer': 'https://www.amazon.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
    }


browser = webdriver.Chrome()
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10) # 等待加载10s

home_page ='https://www.gigab2b.com/index.php?route=common/home'

path1 = r"C:\Users\Lenovo\Desktop\美国站每周产品推荐-0713\TOPMAX.xlsx"
path2 = r"C:\Users\Lenovo\Desktop\美国站每周产品推荐-0713\U-Style.xlsx"
path3 = r"C:\Users\Lenovo\Desktop\美国站每周产品推荐-0713\Oris Fur..xlsx"
path4 = r"C:\Users\Lenovo\Desktop\美国站每周产品推荐-0713\TREXM.xlsx"
path5 = r"C:\Users\Lenovo\Desktop\美国站每周产品推荐-0713\GO Store.xlsx"
path6 = r"C:\Users\Lenovo\Desktop\美国站每周产品推荐-0713\WM Store.xlsx"

df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)
df3 = pd.read_excel(path3)
df4= pd.read_excel(path4)
df5 = pd.read_excel(path5)
df6 = pd.read_excel(path6)

data1 = pd.DataFrame(df1)
data2 = pd.DataFrame(df2)
data3 = pd.DataFrame(df3)
data4 = pd.DataFrame(df4)
data5 = pd.DataFrame(df5)
data6 = pd.DataFrame(df6)

urls1 = data1['产品链接']
urls2 = data2['产品链接']
urls3 = data3['产品链接']
urls4 = data4['产品链接']
urls5 = data5['产品链接']
urls6 = data6['产品链接']

#print(urls1)
print(urls2)
print(urls3)
print(urls4)
print(urls5)
print(urls6)



def login():
    browser.get('https://www.gigab2b.com/index.php?route=account/login')
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@id="input-email"]')))
    input.send_keys('demo@buyer.com')
    input = wait.until(EC.presence_of_element_located(
        (By.XPATH, '//input[@id="input-password"]')))
    input.send_keys('0325#Test@BB')
    submit = wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//input[3]')))
    submit.click()  # 点击登录按钮

login()

# TotalCost1=[]
# TotalCost2=[]
# TotalCost3=[]
TotalCost4=[]
TotalCost5=[]
TotalCost6=[]
# Price1=[]
# Price2=[]
# Price3=[]
Price4=[]
Price5=[]
Price6=[]

def scrapeTotalCost(url):
    # Download the page using requests
    r = requests.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    total_cost = soup.find(id='price_total').get_text().strip()
    return total_cost

def scrapePrice(url):
    # Download the page using requests
    r = requests.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    price = soup.find(id='price_price_value').get_text().strip().replace("/Unit","").strip()
    return price

# for url in urls1:
#    TotalCost1.append(scrapeTotalCost(url))
#    Price1.append(scrapePrice(url))
#
# for url in urls2:
#    TotalCost2.append(scrapeTotalCost(url))
#    Price2.append(scrapePrice(url))

# for url in urls3:
#    TotalCost3.append(scrapeTotalCost(url))
#    Price3.append(scrapePrice(url))

# for url in urls4:
#    TotalCost4.append(scrapeTotalCost(url))
#    Price4.append(scrapePrice(url))
#
# for url in urls5:
#    TotalCost5.append(scrapeTotalCost(url))
#    Price5.append(scrapePrice(url))
#
for url in urls6:
   TotalCost6.append(scrapeTotalCost(url))
   Price6.append(scrapePrice(url))


#def create_csv():
# print(TotalCost)
# print(Price)



# df1["单价"]=Price1
# df1["总花费"]=TotalCost1
# df1.to_csv(r"C:\Users\Lenovo\Desktop\美国站每周产品推荐TOPMAX.csv",  index=False)

# df2["单价"]=Price2
# df2["总花费"]=TotalCost2
# df2.to_csv(r"C:\Users\Lenovo\Desktop\美国站每周产品推荐U-Style.csv",  index=False)

# df3["单价"]=Price3
# df3["总花费"]=TotalCost3
# df3.to_csv(r"C:\Users\Lenovo\Desktop\美国站每周产品推荐Oris Fur..csv",  index=False)

# df4["单价"]=Price4
# df4["总花费"]=TotalCost4
# df4.to_csv(r"C:\Users\Lenovo\Desktop\美国站每周产品推荐TREXM.csv",  index=False)

# df5["单价"]=Price5
# df5["总花费"]=TotalCost5
# df5.to_csv(r"C:\Users\Lenovo\Desktop\美国站每周产品推荐GO Store.csv",  index=False)


df6["单价"]=Price6
df6["总花费"]=TotalCost6
df6.to_csv(r"C:\Users\Lenovo\Desktop\美国站每周产品推荐WM Store.csv",  index=False)






