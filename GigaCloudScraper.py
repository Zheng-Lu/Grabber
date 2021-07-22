import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import pandas as pd
from requests import Session
from multiprocessing import Pool

upload_url = "https://adm.mixshop.world/product/add"
upload_headers = {
    'accept': '*/*',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJtYWNybyIsImNyZWF0ZWQiOjE2MjY3ODIyNTc2NzQsImV4cCI6MTYyNzM4NzA1N30.shFI1w66O6cQJkoMhRvt-vgSUZXs-xit45kcp_JhSathx7-pT_mFAWBhBO9wCO7NoPPY23IPQdFDVGsBJAVbiQ',
    'Content-Type': 'application/json',
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'referer': 'https://www.gigab2b.com/'
}

# The file that contains a list of urls
file = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐TOPMAX.csv"
file_type = file.split(".")[1]
if file_type == "csv":
    try:
        urls = pd.DataFrame(pd.read_csv(file))['产品链接']
    except UnicodeError:
        print("尝试使用 encoding='gbk' ")

elif file_type in ["xlsx", "xls"]:
    urls = pd.DataFrame(pd.read_excel(file))['产品链接']

def get_id(urls):
    ids = []
    for url in urls:
        ids.append(url.split("id=")[1])
    return ids

print(get_id(urls))

def download_product(id):
    url = 'https://www.gigab2b.com/index.php?route=product/product&product_id=' + id
    """
    req = urllib.request.Request(
        url,
        data=None,
        headers=headers
    )
    response = urllib.request.urlopen(req)
    content = response.read()
    """
    response = requests.get(url, headers=headers)
    content = response.content
    print(content)
    with open(id + '.html', 'wb') as f:
        f.write(content)




def download_imgs(id, imgs):
    img_i = 1
    for img in imgs:
        urllib.request.urlretrieve(img, id + '_' + str(img_i) + ".jpg")
        img_i += 1


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


def scrape_product(id):
    html = ''
    with open(id + '.html') as f:
        for line in f.readlines():
            html += line.strip()
    soup = BeautifulSoup(html, features="lxml")
    title = soup.find('title').string
    desc = soup.find("div", {"id": "tabDescription"})
    price = get_price(html)
    imgs = get_img_urls(soup)
    cost = soup.find(id='price_unit').get_text().strip()
    upload(id, title, desc, price, imgs, cost)

    # upload(id, name, desc, price, imgs)


def upload(id, title, desc, price, imgs, cost):
    data = {
        "productNo": id,
        "pic": imgs[0],
        "cost": cost,
        "price": price,
        "currencyCode": "USD",
        "albumPics": imgs[1:],
        "categoryName": "Furniture",
        "title": title,
        "desc": desc,
        "keyword": "",
        "name": title,
        "regionCode": "US",
        "source": "gigab2b",

    }
    print(data)
    # resp = requests.post(upload_url, headers=upload_headers, data=data)
    # print(resp)


# product_ids = ['351733']

"""
for id in product_ids:
    download_product(id)

"""
# for id in product_ids:
#     scrape_product(id)
