from selenium import webdriver
import requests
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import urllib.parse
from urllib.parse import quote,unquote

start = time.time()

pd.set_option('max_colwidth',100)

browser = webdriver.Chrome()
browser.maximize_window()  # 最大化窗口
wait = WebDriverWait(browser, 10) # 等待加载10s

#GigaCloud 主页
home_page ='https://www.gigab2b.com/index.php?route=common/home'

#文件路径
# path1 = r"C:\Users\Lenovo\Desktop\ProductUpload\TOPMAX.xlsx"
path1 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐TOPMAX.csv"
path2 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐U-Style.csv"
path3 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐Oris Fur..csv"
path4 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐TREXM.csv"
path5 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐GO Store.csv"
path6 = r"C:\Users\Lenovo\Desktop\Furniture\美国站每周产品推荐WM Store.csv"

#df1 = pd.read_csv(path1,encoding='gbk')
# df2 = pd.read_csv(path2)
# df3 = pd.read_csv(path3, encoding='gbk')
# df4 = pd.read_csv(path4, encoding='gbk')
df5 = pd.read_csv(path5)
# df6 = pd.read_csv(path6)

#data1 = pd.DataFrame(df1)
# data2 = pd.DataFrame(df2)
# data3 = pd.DataFrame(df3)
# data4 = pd.DataFrame(df4)
data5 = pd.DataFrame(df5)
# data6 = pd.DataFrame(df6)

# urls1 = data1['产品链接']
# urls2 = data2['产品链接']
# urls3 = data3['产品链接']
# urls4 = data4['产品链接']
urls5 = data5['产品链接']
# urls6 = data6['产品链接']



#模拟登录
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

createVar = locals()
maVarList = []
for i in range(4):
    createVar['DetailPic'+str(i)] = []
    maVarList.append(createVar['DetailPic'+str(i)])

Pic=[]
DetailPic1=[]
DetailPic2=[]
DetailPic3=[]
DetailPic4=[]
DetailPic5=[]

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
    return desc

def scrapeImgURL(url):
    # Download the page using requests
    r = s.post(url, headers=headers)
    # create the object that will contain all the info in the url
    soup = BeautifulSoup(r.content, features="lxml")
    Img = soup.find_all('img')
    pics=[]
    for i in range(8,14):
        pics.append(Img[i].get('src'))
    return pics



for url in urls5:
    print(scrapeImgURL(url))
    Pic.append(scrapeImgURL(url)[0])
    DetailPic1.append(scrapeImgURL(url)[1])
    DetailPic2.append(scrapeImgURL(url)[2])
    DetailPic3.append(scrapeImgURL(url)[3])
    DetailPic4.append(scrapeImgURL(url)[4])
    DetailPic5.append(scrapeImgURL(url)[4])
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
df5['pic']=Pic
df5['detailPic1']=DetailPic1
df5['detailPic2']=DetailPic2
df5['detailPic3']=DetailPic3
df5['detailPic4']=DetailPic4
df5['detailPic5']=DetailPic5
df5.to_excel(r"C:\Users\Lenovo\Desktop\Go Store.xlsx", index=False)

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

end = time.time()
print(end-start)




