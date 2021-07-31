import re
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import requests

start = time.time()

pd.set_option('max_colwidth',100)

browser = webdriver.Chrome()
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10) # 等待加载10s

def login():
    browser.get('https://www.gigab2b.com/index.php?route=account/login')
    browser.find_element_by_xpath('//*[(@id = "input-email")]').send_keys('demo@buyer.com')
    browser.find_element_by_xpath('//*[(@id = "input-password")]').send_keys('0325#Test@BB',Keys.ENTER)
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

def get_desc(soup):
    Desc = soup.select('p[style="font-size\:\ 20px\;margin\:\ 0\;overflow\:\ hidden\;text-overflow\:\ ellipsis\;"]')
    desc = ""
    for i in Desc:
        desc=i.get_text()
    return desc

def get_img_urls(soup):
    Img = soup.find_all('img')
    res = []
    for i in range(10, 15):
        src = Img[i].get('src')
        x = src.split('?')[0]
        res.append(x)
    return res

def get_price(data):
    return re.search('onlyPriceString = "(.*)"', '    var onlyPriceString = "$150.00";;').group(1)

def download_product(id):
    url = 'https://www.gigab2b.com/index.php?route=product/product&product_id=' + id
    content = s.post(url, headers=headers)
    with open("C://Users//Lenovo//Desktop//html//"+str(id) + '.html', 'wb') as f:
        f.write(content.content)
        f.close()

def scrape_product(id):
    html = ''
    url = ''
    with open("C://Users//Lenovo//Desktop//html//"+str(id) + '.html', encoding='gb18030', errors='ignore') as f:
        for line in f.readlines():
            html += line.strip()
    soup = BeautifulSoup(html, features="lxml")
    print(get_desc(soup))
    print(get_price(html))
    img_i = 1
    for img in get_img_urls(soup):
        urllib.request.urlretrieve(img, "C://Users//Lenovo//Desktop//pics//"+id +'_' + str(img_i) + ".jpg")
        img_i += 1

product_ids = ['339428','339441','326992','327105','327058','327775','335291','332098']

for id in product_ids:
    pass
    download_product(id)

for id in product_ids:
    scrape_product(id)

end = time.time()
print(end-start)