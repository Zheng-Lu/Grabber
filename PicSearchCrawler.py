import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from multiprocessing import Pool, cpu_count

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
            "a.iOGqzf.H4qWMc.aXIg1b[href='about\:invalid\#zClosurez'][onclick='google\.qb\.ti\(true\)\;return\ false']")
        upload_img_option.click()

        # Upload file from given file path
        condition_3 = EC.visibility_of_element_located(
            (By.ID, 'awyMjb'))
        WebDriverWait(self.driver, timeout=10, poll_frequency=0.5).until(condition_3)
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

    # regex of target url :
    def scrape_target(self, content):
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


searcher = GooglePicSearcher()
content = searcher.upload_img_file(r"C:\Users\Lenovo\Desktop\pics\326992_1.jpg")
print(searcher.scrape_target(content))
