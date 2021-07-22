import re
import json
import urllib.request
from bs4 import BeautifulSoup
import requests
from requests import Session


giga_url = 'https://www.gigab2b.com/index.php?route=product/product&product_id='
giga_headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.gigab2b.com/'
}


def download_product(id):
    response = requests.get(giga_url + id, headers=giga_headers)
    content = response.content
    with open(id + '.html', 'wb') as f:
        f.write(content)


product_ids = []
with open('list.txt') as f:
    for line in f.readlines():
        product_ids.append(line.strip())

for id in product_ids:
    try:
        download_product(id)
    except Exception as e:
        print(e)
