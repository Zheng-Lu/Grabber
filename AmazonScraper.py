import json

import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
import random
from itertools import cycle

from selectorlib import Extractor
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

pd.set_option('max_colwidth', 100)

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
    'authority': 'www.amazon.com',
    'cache-control': 'max-age=0',
    'rtt': '50',
    'downlink': '10',
    'ect': '4g',
    'sec-ch-ua': '^\\^',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': user_agent,
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

f = open(r"C:\Users\Lenovo\Desktop\ProxiesPool\ProxiesPool(socks4).txt",'r', encoding='utf-8')
proxies = f.read().split("\n")

for i in range(len(proxies)):
    proxies[i] = 'socks4://' + proxies[i]
    # print(proxies[i])

proxies_pool = cycle(proxies)
proxy = next(proxies_pool) # Get a proxy from the pool

"""
Proxies Testing 
"""

# url = 'https://httpbin.org/ip'
# for i in range(len(proxies)):
#
#     print("Request #%d" % i)
#     try:
#         response = requests.get(url, proxies={"http": proxy, "https": proxy})
#         print(response.json())
#     except:
#         print("Skipping. Connnection error")

"""
Headers Testing 
"""

# url = 'https://httpbin.org/headers'
# for i in range(0, 4):
#
#     # Make the request
#     response = requests.get(url, headers=headers)
#     print("Request #%d\nUser-Agent Sent:%s\n\nHeaders Recevied by HTTPBin:" % (i, user_agent))
#     print(response.json())
#     print("-------------------")

def search_amazon(item):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get('https://www.amazon.com')
    driver.find_element_by_id('twotabsearchtextbox').send_keys(item)
    driver.find_element_by_id("nav-search-submit-text").click()

    driver.implicitly_wait(5)

    try:
        num_page = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[6]')
    except NoSuchElementException:
        num_page = driver.find_element_by_class_name('a-last').click()

    driver.implicitly_wait(3)

    url_list = []

    for i in range(int(num_page.text)):
        page_ = i + 1
        url_list.append(driver.current_url)
        driver.implicitly_wait(4)
        driver.find_element_by_class_name('a-last').click()
        print("Page " + str(page_) + " grabbed")

    driver.quit()

    with open('search_results_urls.txt', 'w') as filehandle:
        for result_page in url_list:
            filehandle.write(f'{result_page}\n')

    print("------------------------DONE------------------------")

def getProducts(url):
    s = requests.Session()
    time.sleep(3)
    try:
        r = s.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
    except:
        print("Skipping. Connnection error")

    soup = BeautifulSoup(r.content, features="lxml")

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
            url.append('https://www.amazon.com'+u.get('href'))
    except AttributeError:
        url.append('N/A')

    data = {
        'Title': title,
        'Price': price,
        'Pic URL': pic,
        'Prodcut URL': url
    }

    return data

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('selector.yml')

def download_product(url):
    print(f"Downloading {url}")
    response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})
    if response.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in response.text:
            print(f"Page {url} was blocked by Amazon. Please try using better proxies\n")
        else:
            print(f"Page {url} must have been blocked by Amazon as the status code was {response.status_code}" )
        return None

    # content = response.content
    # with open(r'C:\Users\Lenovo\Desktop\html\Amazon.html', 'wb') as f:
    #     f.write(content)

    return e.extract(response.text)

def find_captcha(url):
    response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy})



# URL = 'https://www.amazon.com/s?k=100+Watt+Portable+Solar+Panels%2C+Foldable+Solar+Panel+Charger%2C+Compatible+with+Solar+Power+Stations%2FPhones%2Flaptops%2FTablet+Computers%2C+Suitable+for+Family+Camping%2FTravel%2FHiking+Various+Outdoor+Activities&ref=nb_sb_noss'
# df = pd.DataFrame.from_dict(getProducts(URL))
# print(df)
# print(getProducts(URL))
# search_amazon('100 Watt Portable Solar Panels, Foldable Solar Panel Charger, Compatible with Solar Power Stations/Phones/laptops/Tablet Computers, Suitable for Family Camping/Travel/Hiking Various Outdoor Activities')

with open("search_results_urls.txt",'r') as urllist:
    for url in urllist.read().splitlines():
        # data = download_product(url)
        # print(data)
        print(getProducts(url))


end = time.time()
print('Time taken: ' + str(round(end - start, 2)) + 's')
