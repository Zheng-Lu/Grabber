import requests
import json
import pandas as pd
import csv
import urllib.request as request
from urllib.request import Request, urlopen

url = 'https://adm.mixshop.world/distributor/product/list?pageNum=1&pageSize=2090'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'}

### get data ###
r = requests.get(url)
content = json.loads(r.text)

### process data ###

name = []
pic = []
price = []
category = []
df = pd.DataFrame(columns=['name', 'pic', 'price', 'category'])
for i in range(len(content['data']['list'])):
    df.loc[i + 1] = [content['data']['list'][i]['name'], content['data']['list'][i]['pic'],
                     content['data']['list'][i]['price'], content['data']['list'][i]['productCategoryName']]
    name.append(content['data']['list'][i]['name'])
    pic.append(content['data']['list'][i]['pic'])
    price.append(content['data']['list'][i]['price'])
    category.append(content['data']['list'][i]['productCategoryName'])
df.to_csv('C://Users//Lenovo//Desktop//data.csv',index=0,encoding='utf-8-sig')

### 一为utf-8格式 ###
# for i in range(len(name)):
#     content['data']['list'][i]['name'].replace(u'\xa0 ', u' ')
#     content['data']['list'][i]['pic'].replace(u'\xa0 ', u' ')
#     # content['data']['list'][i]['price'].replace(u'\xa0 ', u' ')
#     content['data']['list'][i]['productCategoryName'].replace(u'\xa0 ', u' ')

# with open('C://Users//Lenovo//Desktop//data.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['name', 'pic', 'price', 'category'])
#     for i in range(len(name)):
#         writer.writerow([name[i].replace(u'\xa0 ', u''), pic[i].replace(u'\xa0 ', u''), price[i], category[i].replace(u'\xa0 ', u'')])


req = Request(url, headers=headers)
# web_byte = urlopen(req).read()
# webpage = web_byte.decode('utf-8')
# print(webpage)

# crawl_content = request.urlopen(url).read()
# print(crawl_content)
