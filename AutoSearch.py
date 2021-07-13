import requests
import scrapy
from urllib.parse import urlencode
from urllib.parse import urljoin
import re
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import time

API = '64eac66e9d127d0cbbe7b187119a820f'

amazon_url = 'https://www.amazon.com/'
mixshop_url = 'https://adm.mixshop.world/distributor/product/list?pageNum=1&pageSize=2090'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.124 Safari/537.36'}

### get data ###
r = requests.get(mixshop_url)
content = json.loads(r.text)

### process data ###
keywords = []
for i in range(len(content['data']['list'])):
    keywords.append(content['data']['list'][i]['name'])
#print(keywords)

def get_url(url):
    payload = {'api_key': API, 'url': url, 'country_code': 'us'}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
    return proxy_url

# def search_amazon(item):
#     driver = webdriver.Chrome(ChromeDriverManager().install())
#     driver.get(amazon_url)
#     search_box = driver.find_element_by_id('twotabsearchtextbox').send_keys(item)
#     search_button = driver.find_element_by_id("nav-search-submit-button").click()



class AmazonSpider(scrapy.Spider):
    name = 'amazon'

    def start_requests(self):
        for keyword in keywords:
            url = 'https://www.amazon.com/s?' + urlencode({'k': keywords})
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)

    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(url=get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})

        next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        if next_page:
            url = urljoin("https://www.amazon.com", next_page)
            yield scrapy.Request(url=get_url(url), callback=self.parse_keyword_response)


    def parse_product_page(self, response):
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        image = re.search('"large":"(.*?)"', response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()

        if not price:
            price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
                    response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()

        temp = response.xpath('//*[@id="twister"]')
        sizes = []
        colors = []
        if temp:
            s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
            json_acceptable = s.replace("'", "\"")
            di = json.loads(json_acceptable)
            sizes = di.get('size_name', [])
            colors = di.get('color_name', [])

        bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        seller_rank = response.xpath(
            '//*[text()="Amazon Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        yield {'asin': asin, 'Title': title, 'MainImage': image, 'Rating': rating, 'NumberOfReviews': number_of_reviews,
               'Price': price, 'AvailableSizes': sizes, 'AvailableColors': colors, 'BulletPoints': bullet_points,
               'SellerRank': seller_rank}
