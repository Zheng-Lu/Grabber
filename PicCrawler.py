import requests
import json
import pandas as pd
import urllib
import urllib.request
import csv
import os

path = 'D://picSearch'
url = 'https://adm.mixshop.world/distributor/product/list?pageNum=1&pageSize=100'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'}

### get data ###
r = requests.get(url)
content = json.loads(r.text)

# datas = pd.read_csv('C://Users//Lenovo//Desktop//Mixshop&Amazon.csv',usecols=['Pictures(Mixshop)'],nrows=100)
# print(datas)

# with open('C://Users//Lenovo//Desktop//Mixshop&Amazon.csv','r') as f:
#     reader = csv.reader(f)
#     column = [row[1] for row in reader]
#     print(column)


pic = []
#df = pd.DataFrame(columns=['pic'])
for i in range(len(content['data']['list'])):
    pic.append(content['data']['list'][i]['pic'])
    #df.loc[i + 1] = [ content['data']['list'][i]['pic']]
#df.to_csv('C://Users//Lenovo//Desktop//mixshop_pic.csv',index=0,encoding='utf-8-sig')

# print(len(pic))


# if os.path.exists(path):
#     print(True)
# else:
#     print(False)


#for i in range(len(pic)):
#     dir = os

# for i in range(5):
#     urllib.request.urlretrieve(pic[i], str(i)+".jpg")

