from PIL import Image
from io import BytesIO
from CompareImageHistogram import compare_img_hist
import os
import random
from time import strftime
from time import gmtime
import re
import time
import pandas as pd
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from itertools import cycle
from multiprocessing import Pool, cpu_count
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

start = time.time()


user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

# Pick a random user agent
user_agent = random.choice(user_agent_list)

headers = {
    'user-agent': user_agent,
    'referer': 'https://www.google.com/',
}

f = open(r"C:\Users\Lenovo\Desktop\ProxiesPool\ProxiesPool(socks4).txt", 'r', encoding='utf-8')
proxies = f.read().split("\n")

for i in range(len(proxies)):
    proxies[i] = 'socks4://' + proxies[i]

proxies_pool = cycle(proxies)
proxy = next(proxies_pool)  # Get a proxy from the pool


def run():
    path = r"C:\Users\Lenovo\Desktop\pics"
    num_process = cpu_count()
    pool = Pool(num_process)
    result = partition(img_file_list(path), num_process)


def img_file_list(path):
    file_list = []
    file = os.listdir(path)
    for img in file:
        file_list.append(img)
    return file_list


def img_url_list(path):
    if path.split('.')[1] == 'xlsx':
        url_list = pd.read_excel(path)['img url'].tolist()
        return url_list

    elif path.split('.')[1] == 'csv':
        url_list = pd.read_csv(path)['img url'].tolist()
        return url_list

    elif path.split('.')[1] == 'txt':
        with open(path) as f:
            url_list = f.readlines()
        url_list = [x.strip() for x in url_list]
        return url_list


def partition(ls, size):
    num_per_list = len(ls) // size
    result = []
    if num_per_list * size == len(ls):
        for i in range(size):
            result.append(ls[num_per_list * i:num_per_list * (i + 1)])
    else:
        for i in range(size - 1):
            result.append(ls[num_per_list * i:num_per_list * (i + 1)])
        result.append(ls[num_per_list * (size - 1):])
    return result

#
# def getPrice(url):
#     r = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
#     soup = BeautifulSoup(r.content, features="lxml")
#     price = soup.find('span', attrs={'id': 'priceblock_ourprice'})
#     return price

def getImageByUrl():
    # ????????????url ??????????????????
    html = requests.get(url, verify=False)
    image = Image.open(BytesIO(html.content))
    return image

def getProduct(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=2)
    try:

        product = {
            'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
            'price': r.html.xpath('//*[@id="price_inside_buybox"]', first=True).text,
            'image': r.html.xpath('//*[@id="price_inside_buybox"]', first=True).text,
            'Product URL': url,
            'ASIN': url.split('/dp/')[1]
        }
        # print(product)
    except:
        product = {
            'title': r.html.xpath('//*[@id="productTitle"]', first=True).text,
            'price': 'item unavailable',
            'Product URL': url,
            'ASIN': url.split('/dp/')[1]
        }
        # print(product)
    return product


def scrape_target(content):
    urls = []
    result = []
    targets = re.findall(
        '(?:https?://)?(?:[a-zA-Z0-9\-]+\.)?(?:amazon|amzn){1}\.(?P<tld>[a-zA-Z\.]{2,})\/(gp/(?:product|offer-listing|customer-media/product-gallery)/|exec/obidos/tg/detail/-/|o/ASIN/|dp/|(?:[A-Za-z0-9\-]+)/dp/)?(?P<ASIN>[0-9A-Za-z]{10})',
        content)

    # Reform the targets into url list
    for target in targets:
        urls.append('https://www.amazon.com/' + target[1] + target[2])

    # Remove duplicates from the url list
    for url in urls:
        if url not in result:
            result.append(url)

    return result


def isSamePic(img1, img2):
    if compare_img_hist(img1, img2) > 0.8:
        return True
    else:
        return False


class GooglePicSearcher:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.option = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.get("https://www.google.com/imghp?hl=en")

        # Wait until the camera show up
        condition_1 = EC.visibility_of_element_located(
            (By.CLASS_NAME, "ZaFQO"))
        WebDriverWait(self.driver, timeout=20, poll_frequency=0.5).until(condition_1)

        # Click the camera icon
        image_button = self.driver.find_element_by_class_name("ZaFQO")
        image_button.send_keys(Keys.ENTER)

    def upload_img_file(self, file):
        # Choose upload image
        upload_img_option = self.driver.find_element_by_css_selector(
            "a.iOGqzf.H4qWMc.aXIg1b[onclick='google\.qb\.ti\(true\)\;return\ false']")
        upload_img_option.click()

        # Upload file from given file path
        input_ = self.driver.find_element_by_css_selector("input#awyMjb")
        input_.send_keys(file)

        return self.driver.page_source

    def upload_img_url(self, url):
        # Choose Paste image URL
        paste_img_option = self.driver.find_element_by_css_selector("span#cjyo4e.IyNJid.H4qWMc.aXIg1b")
        paste_img_option.click()

        input_ = self.driver.find_element_by_xpath('//*[(@id = "Ycyxxc")]')
        input_.send_keys(url)

        search_button = self.driver.find_element_by_id('RZJ9Ub')
        search_button.click()

        return self.driver.page_source


searcher = GooglePicSearcher()
#
# dict = {}
# folder = r"C:\Users\Lenovo\Desktop\pics"
# for filename in os.listdir(folder):
#     print(filename)
#     content = searcher.upload_img_file(r"C:\Users\Lenovo\Desktop\pics\{}".format(filename))
#     urls = searcher.scrape_target(content)
#     dict[filename] = urls
#     searcher.__init__()
#     print(dict)

if __name__ == '__main__':
    content = searcher.upload_img_file(r"C:\Users\Lenovo\Desktop\pics\326992_2.jpg")
    # content = searcher.upload_img_url("https://ec-m2c-cn.oss-cn-shenzhen.aliyuncs.com/yilian/images/2021/04/28/20210428112952_Goroo.jpg")
    urls = scrape_target(content)
    print(urls)
    product_details = []
    for url in urls:
        product_details.append(getProduct(url))
    print(product_details)

""""""""
end = time.time()
seconds = round(end - start, 2)
if seconds < 60:
    print('Time taken: ' + str(seconds) + 's')
else:
    print('Time taken: ' + strftime("%H:%M:%S", gmtime(seconds)))
