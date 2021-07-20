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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import numpy as np
import sys
import io

pd.set_option('max_colwidth',100)

browser = webdriver.Chrome()
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10) # 等待加载10s

#GigaCloud 主页
home_page ='https://www.gigab2b.com/index.php?route=common/home'

#文件路径
# path1 = r"C:\Users\Lenovo\Desktop\ProductUpload\TOPMAX.xlsx"
path1 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐TOPMAX.csv"
path2 = r"C:\Users\Lenovo\Desktop\ProductUpload\U-Style.xlsx"
path3 = r"C:\Users\Lenovo\Desktop\ProductUpload\Oris Fur..xlsx"
path4 = r"C:\Users\Lenovo\Desktop\ProductUpload\TREXM.xlsx"
path5 = r"C:\Users\Lenovo\Desktop\ProductUpload\Go Store.xlsx"
path6 = r"C:\Users\Lenovo\Desktop\ProductUpload\WM Store.xlsx"

df1 = pd.read_csv(path1,encoding='gbk')
# df2 = pd.read_excel(path2)
# df3 = pd.read_excel(path3)
# df4 = pd.read_excel(path4)
# df5 = pd.read_excel(path5)
# df6 = pd.read_excel(path6)

data1 = pd.DataFrame(df1)
# data2 = pd.DataFrame(df2)
# data3 = pd.DataFrame(df3)
# data4 = pd.DataFrame(df4)
# data5 = pd.DataFrame(df5)
# data6 = pd.DataFrame(df6)

urls1 = data1['产品链接']
# urls2 = data2['url']
# urls3 = data3['url']
# urls4 = data4['url']
# urls5 = data5['url']
# urls6 = data6['url']

#print(urls1)
# print(urls2)
# print(urls3)
# print(urls4)
# print(urls5.fillna(value=str(0)))
#print(urls6)

#模拟登录
def login():
    browser.get('https://www.gigab2b.com/index.php?route=account/login')
    # input = wait.until(EC.presence_of_element_located(
    #     (By.XPATH, '//input[@id="input-email"]')))
    browser.find_element_by_xpath('//*[(@id = "input-email")]').send_keys('demo@buyer.com')
    browser.find_element_by_xpath('//*[(@id = "input-password")]').send_keys('0325#Test@BB',Keys.ENTER)
    # input = wait.until(EC.presence_of_element_located(
    #     (By.XPATH, '//input[@id="input-password"]')))
    # input.send_keys('0325#Test@BB')
    # submit = wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, '//input[3]')))
    # submit.click()  # 点击登录按钮
    time.sleep(10)  # 等待cookie加载完成
    cookies = browser.get_cookies()
    return cookies


headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                 'application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'referer': 'https://www.gigab2b.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
    }


cookies = login()
s = requests.Session()
c = requests.cookies.RequestsCookieJar()
for item in cookies:
    c.set(item["name"],item["value"])
print(c)
s.cookies.update(c)


# TotalCost1=[]
# TotalCost2=[]
# TotalCost3=[]
# TotalCost4=[]
# TotalCost5=[]
# TotalCost6=[]
# Price1=[]
# Price2=[]
# Price3=[]
# Price4=[]
# Price5=[]
# Price6=[]

Desc1=[]
Desc2=[]
Desc3=[]
Desc4=[]
Desc5=[]
Desc6=[]

Pic=[]
DetailPic1=[]
DetailPic2=[]
DetailPic3=[]
DetailPic4=[]


def scrapeTotalCost(url):
    # Download the page using requests
    # r = requests.post(url, headers=headers)
    r = s.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    # total_cost = soup.find(id='price_unit').get_text().strip()
    total_cost = soup.find(id='price_unit').get_text().strip()
    return total_cost

def scrapePrice(url):
    # Download the page using requests
    # r = requests.post(url, headers=headers)
    r = s.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    price = soup.find(id='price_price_value').get_text().strip().replace("/Unit","").strip()
    #price = soup.find(id='priceTypeDefault').get_text()
    return price

def scrapeDesc(url):
    # Download the page using requests
    r = s.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    Desc = soup.select('p[style="font-size\:\ 20px\;margin\:\ 0\;overflow\:\ hidden\;text-overflow\:\ ellipsis\;"]')
    for i in Desc:
        desc=i.get_text()
    # price = soup.find(id='priceTypeDefault').get_text()
    return desc

def scrapeImgURL(url):
    # Download the page using requests
    r = s.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    # Desc = soup.select('img[title="font-size\:\ 20px\;margin\:\ 0\;overflow\:\ hidden\;text-overflow\:\ ellipsis\;"]')
    # Img = soup.select('img[title="'+str(scrapeDesc(url))+'"]')
    Img = soup.find_all('img')
    # for i in Img:
    #     img = i.get_text
    # price = soup.find(id='priceTypeDefault').get_text()
    pic = Img[8].get('src') # pic:8  detailpics:10 11 12 13
    detailPic1 = Img[10].get('src')
    detailPic2 = Img[11].get('src')
    detailPic3 = Img[12].get('src')
    detailPic4 = Img[13].get('src')
    return pic, detailPic1, detailPic2, detailPic3, detailPic4



for url in urls1:
    print(scrapeImgURL(url))
    Pic.append(scrapeImgURL(url)[0])
    DetailPic1.append(scrapeImgURL(url)[1])
    DetailPic2.append(scrapeImgURL(url)[2])
    DetailPic3.append(scrapeImgURL(url)[3])
    DetailPic4.append(scrapeImgURL(url)[4])

#     Desc1.append(scrapeDesc(url))
#    TotalCost1.append(scrapeTotalCost(url))
#    Price1.append(scrapePrice(url))
#
# for url in urls2:
#     Desc2.append(scrapeDesc(url))
#    TotalCost2.append(scrapeTotalCost(url))
#    Price2.append(scrapePrice(url))

# for url in urls3:
#     Desc3.append(scrapeDesc(url))
#    TotalCost3.append(scrapeTotalCost(url))
#    Price3.append(scrapePrice(url))

# for url in urls4:
#     Desc4.append(scrapeDesc(url))
#     TotalCost4.append(scrapeTotalCost(url))
#     Price4.append(scrapePrice(url))

# for url in urls5:
#     Desc5.append(scrapeDesc(url))
#    TotalCost5.append(scrapeTotalCost(url))
#    Price5.append(scrapePrice(url))

# for url in urls6:
#     Desc6.append(scrapeDesc(url))
#    TotalCost6.append(scrapeTotalCost(url))
#    Price6.append(scrapePrice(url))


#def create_csv():
# print(TotalCost)
# print(Price)



# df1["单价"]=Price1
# df1["总花费"]=TotalCost1
# df1['desc']=Desc1
df1['pic']=Pic
df1['detailPic1']=DetailPic1
df1['detailPic2']=DetailPic2
df1['detailPic3']=DetailPic3
df1['detailPic4']=DetailPic4
df1.to_excel(r"C:\Users\Lenovo\Desktop\TOPMAX.xlsx", index=False)

# df2["单价"]=Price2
# df2["总花费"]=TotalCost2
# df2['desc']=Desc2
# df2.to_csv(r"C:\Users\Lenovo\Desktop\U-Style.xlsx",  index=False)

# df3["单价"]=Price3
# df3["总花费"]=TotalCost3
# df3['desc']=Desc3
# df3.to_csv(r"C:\Users\Lenovo\Desktop\Oris Fur..xlsx",  index=False)

# df4["单价"]=Price4
# df4["总花费"]=TotalCost4
# df4['desc']=Desc4
# df4.to_csv(r"C:\Users\Lenovo\Desktop\TREXM.xlsx",  index=False)

# df5["单价"]=Price5
# df5["总花费"]=TotalCost5
# df5['desc']=Desc5
# df5.to_csv(r"C:\Users\Lenovo\Desktop\GO Store.xlsx",  index=False)


# df6["单价"]=Price6
# df6["总花费"]=TotalCost6
# df6['desc']=Desc6
# df6.to_csv(r"C:\Users\Lenovo\Desktop\WM Store.xlsx",  index=False)






