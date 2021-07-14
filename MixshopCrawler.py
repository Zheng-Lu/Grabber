import requests
import json
import pandas as pd
import csv
import urllib.request as request
from urllib.request import Request, urlopen

url = 'https://adm.mixshop.world/distributor/product/list?pageNum=1&pageSize=100'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'}

### get data ###
r = requests.get(url)
content = json.loads(r.text)

### process data ###

# name = []
# pic = []
# price = []
# id = []
df = pd.DataFrame(columns=['Name(Mixshop)', 'Pictures(Mixshop)', 'Price(Mixshop)', 'ID(Mixshop)'])
for i in range(len(content['data']['list'])):
    df.loc[i + 1] = [content['data']['list'][i]['name'], content['data']['list'][i]['pic'],
                     content['data']['list'][i]['price'], content['data']['list'][i]['id']]
    # name.append(content['data']['list'][i]['name'])
    # pic.append(content['data']['list'][i]['pic'])
    # price.append(content['data']['list'][i]['price'])
    # id.append(content['data']['list'][i]['id'])
df.to_csv('C://Users//Lenovo//Desktop//Mixshop&Amazon.csv',index=0,encoding='utf-8-sig')
