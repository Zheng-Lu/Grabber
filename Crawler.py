import csv
import os
import random
import time
import urllib
from urllib import parse

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

pro = ['110.73.11.111:8123', '110.73.35.108:8123', '61.135.217.7:80']

url = "https://myip.ms/ajax_table/sites/2/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1"

proxies = {
  "http": random.choice(pro)
}

formdata = {
    "getpage": "yes",
    "lang": "en"
}

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '19',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'PHPSESSID=a7fh0m81ipb71pc1tr4uah9jb6; s2_uLang=en; s2_theme_ui=red;'
              's2_csrf_cookie_name=efc0361f41aba9638473c064187b0a4b; '
              's2_uGoo=d7baba5a1a9d9b1e3385251721b3f521246ed091; '
              's2_csrf_cookie_name=efc0361f41aba9638473c064187b0a4b; sw=82.5; sh=129.8',
    'Host': 'myip.ms',
    'Origin': 'https://myip.ms',
    'Referer': 'https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
    'sec-ch-ua-mobile': '?0',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/91.0.4472.77 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

html = requests.post(url, data=formdata, headers=headers, proxies=proxies)
print(html.text)

data = parse.urlencode(formdata).encode(encoding='UTF8')
request = urllib.request.Request(url, data=data, headers=headers)

# 返回结果
response = urllib.request.urlopen(request).read()
s = response.decode('utf-8', 'ignore')


class LoopOver(Exception):
    def __init__(self, *args, **kwargs):
        pass


class Spider:
    def __init__(self):
        # csv储存
        self.path = '.'
        self.csvfilename = 'datas.csv'

        options = webdriver.ChromeOptions()

        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 20)

        # 链接
        self.listurl = 'https://myip.ms/ajax_table/sites/2/ipID/23.227.38.0/ipIDii/23.227.38.255/sort/6/asc/1'

        self.host = 'https://myip.ms'

        self.tempalte = '''
<p>
    {}
</p>
<table border="5">
    <thead class="tableFloatingHeaderOriginal">
        <tr valign="middle">
            <th class="nobackgroundimage" align="center" style="width: 32px;">
                No
            </th>
            <th colfirst="ip_owners" align="center" title-orig="Hosting Company" class="header" style="width: 163px;">
                Hosting Company</th>

            <th align="center" title-orig="Website/s" class="header" style="width: 114px;">
                Website/s</th>
            <th align="center" title-orig="Total Websites use this company IPs" class="header headerSortUp"
                style="width: 92px;">
                Total Websites use this company IPs</th>
            <th align="center" title-orig="TOP Websites use this company IPs" class="header" style="width: 77px;">
                TOP Websites use this company IPs</th>
            <th align="center" title-orig="Diagram" class="header" style="width: 38px;">
                Record Update Time</th>
        </tr>
    </thead>
    <tbody>
        {}
    </tbody>
</table>

        '''

        self.tempalte_page = '''
<table border="5">
    <thead class="tableFloatingHeaderOriginal">
        <tr valign="middle">
            <th class="nobackgroundimage" align="center" style="width: 44px;"><div class="edit-icon-tmp normal ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" title-orig="View Table in Full-screen Mode" style="position: absolute; z-index: 1001; left: 5px; top: 568.6px; display: none;"><span class="ui-button-icon-primary ui-icon ui-icon-arrow-4-diag"></span><span class="ui-button-text">Full-screen Mode</span></div><div class="edit-icon-tmp normal ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" title-orig="View Table in Full-screen Mode" style="position: absolute; z-index: 1001; left: 5px; top: 568.6px; display: none;"><span class="ui-button-icon-primary ui-icon ui-icon-arrow-4-diag"></span><span class="ui-button-text">Full-screen Mode</span></div><div class="edit-icon-tmp normal ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" title-orig="View Table in Full-screen Mode" style="position: absolute; z-index: 1001; left: 5px; top: 568.6px; display: none;"><span class="ui-button-icon-primary ui-icon ui-icon-arrow-4-diag"></span><span class="ui-button-text">Full-screen Mode</span></div><div class="edit-icon-tmp normal ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" title-orig="View Table in Full-screen Mode" style="position: absolute; z-index: 1001; left: 5px; top: 568.6px; display: none;"><span class="ui-button-icon-primary ui-icon ui-icon-arrow-4-diag"></span><span class="ui-button-text">Full-screen Mode</span></div><div class="edit-icon-tmp normal ui-button ui-widget ui-state-default ui-corner-all ui-button-text-icon-primary" role="button" title-orig="View Table in Full-screen Mode" style="position: absolute; z-index: 1001; left: 5px; top: 568.6px; display: none;"><span class="ui-button-icon-primary ui-icon ui-icon-arrow-4-diag"></span><span class="ui-button-text">Full-screen Mode</span></div>No</th>
            <th colfirst="sites" align="center" title-orig="Web Site" class="header" style="width: 153px;">
            Web Site</th>
            <th align="center" title-orig="Website IP Address" class="header" style="width: 144px;">
            Website IP Address</th>
            <th align="center" title-orig="Web Hosting Company / IP Owner" class="header" style="width: 178px;">
                Website IPV6 Address</th>
            <th align="center" title-orig="Web Hosting / Server IP Location" class="header" style="width: 134px;">
                World Site Popular</th>
            <th align="center" title-orig="Web Hosting City" class="header" style="width: 105px;">
                World Site Popular Rating</th>
            <th align="center" title-orig="World Site Popular Rating" class="header headerSortDown" style="width: 86px;">
            DNS Records</th>
            <th align="center" title-orig="Diagram" class="header" style="width: 38px;">
            Record Update Time</th>
            </tr>
    </thead>
    <tbody>
        {}
    </tbody>
</table>
                '''

    def turn2filename(self, dst):
        d = dst.replace("\\", "").replace("/", "").replace(":", "").replace("*", "").replace(
            "?", "").replace("\"", "").replace("<", "").replace(">", "").replace(
            "|", "")
        return d

    def run(self):
        strat = time.time()

        self.get_input()
        # 71
        for c, cid in self.datas[115:116]:
            print('>>> ', c, self.listurl.format(cid))

            for item_index, item in enumerate(self.parse_list(self.get_list(self.listurl.format(cid)))):
                if item[1] == '- No Records Found -':
                    item[0] = c
                if c in ['British Indian Ocean Territory', 'Brunei', 'Bulgaria']:
                    self.save_data(item=item, filename=self.turn2filename(c) + '.csv')
                else:
                    self.save_data(item=item, filename='data.csv')
            time.sleep(0)

            end = time.time()

            self.runtime = end - strat
            print('用时{}'.format(self.runtime))

        end = time.time()

        self.runtime = end - strat

    def get_input(self):
        with open(self.inputfilename, 'r', encoding='utf_8') as f:
            reader = csv.reader(f)
            self.datas = [i for i in list(reader) if i]

    def mkurl(self, kw):
        for i in range(0, 1):
            yield self.listurl.format(kw, i * 10)

    def get_list(self, url):
        while True:
            try:
                self.browser.get(url)
                try:
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="sites_tbl" or @id ="web_hosting_tbl"]')))
                except Exception:
                    if 'a Robot' in self.browser.find_element_by_xpath('/html/body/div[2]/div/div/div/center').text:
                        self.browser.find_element_by_xpath(
                            '//*[@id="captcha_submit"]').click()
                        time.sleep(1)
                        raise Exception
                return self.browser
            except Exception as error:
                print('error >>> ', error)
                if self.browser.current_url != url:
                    self.browser.quit()
                    self.browser = webdriver.Chrome()
                    self.wait = WebDriverWait(self.browser, 20)
                    time.sleep(1)
                pass

    def parse_list(self, response):
        html = etree.HTML(response.page_source)

        def pop(attr): return attr[0].strip().replace(
            '\n', '').replace('  ', '') if attr else ''

        for tr in html.xpath('//*[@id="web_hosting_tbl"]/tbody/tr[not(contains(@class,"expand"))]'):
            No = tr.xpath('./td[1]/text()')[0].strip()

            Hosting_Company = pop(tr.xpath('./td[2]/a/text()'))

            page_url = pop(tr.xpath('./td[2]/a/@href'))

            country_name = pop(tr.xpath('./td[3]/a/text()'))

            Website = pop(tr.xpath('./td[4]/a/text()'))

            Total_Websites_use_this_company_IPs = pop(
                tr.xpath('./td[5]/a/text()'))

            TOP_Websites_use_this_company_IPs = pop(
                tr.xpath('./td[6]/a/text()'))

            record_update_time = pop(
                tr.xpath('./td[7]/text()'))

            yield [country_name, No, Hosting_Company, Website, Total_Websites_use_this_company_IPs,
                   TOP_Websites_use_this_company_IPs, record_update_time, self.host + page_url]

    def get_page(self, url):
        while True:
            try:
                self.browser.get(url)
                try:
                    self.wait.until(EC.presence_of_element_located(
                        (By.XPATH, '//*[@id="sites_tbl" or @id ="web_hosting_tbl"]')))
                except Exception as error:
                    print('//*[@id="sites_tbl" or @id ="web_hosting_tbl"] error', error)

                    if 'a Robot' in self.browser.find_element_by_xpath('/html/body/div[2]/div/div/div/center').text:
                        self.browser.find_element_by_xpath(
                            '//*[@id="captcha_submit"]').click()
                        time.sleep(5)
                        raise Exception
                return self.browser
            except Exception as error:
                print('error >>> ', error)
                if self.browser.current_url != url:
                    self.browser.quit()
                    self.browser = webdriver.Chrome()
                    self.wait = WebDriverWait(self.browser, 20)
                    time.sleep(100)
                pass

    def parse_page(self, response):
        text = response.page_source

        html = etree.HTML(text)

        def pop(attr):
            return attr[0].strip().replace(
                '\n', '').replace('  ', '') if attr else ''

        l = len(html.xpath(
            '//*[@id="sites_tbl" or @id ="web_hosting_tbl"]/tbody/tr[not(contains(@class,"expand"))]'))
        print('len is ', l)
        try:
            for i in range(1, l + 1):
                tr = html.xpath(
                    '//*[@id="sites_tbl" or @id ="web_hosting_tbl"]/tbody/tr[not(contains(@class,"expand"))][{}]'.format(
                        i))[0]
                tre = html.xpath(
                    '//*[@id="sites_tbl" or @id ="web_hosting_tbl"]/tbody/tr[contains(@class,"expand")][{}]'.format(i))[
                    0]

                No = pop(tr.xpath('./td[1]/text()'))
                web_site = pop(tr.xpath('./td[2]/a/text()'))
                web_site_ip_address = pop(tr.xpath('./td[3]/a/text()'))

                # tre
                web_site_ipv6_address = pop(
                    tre.xpath(
                        './td[1]/div[@class="stitle"]/b[contains(text(),"IPv6")]/../following-sibling::*[1]//a/text()'))

                # tre
                website_popularity = pop(
                    tre.xpath('./td[1]/div/span[@class="bold arial grey"]/text()'))

                website_popularity_rating = pop(
                    tr.xpath('./td[7]/span/text()'))

                # tre
                dns_records = '\n'.join(
                    [i for i in tre.xpath(
                        './td[1]/div[@class="stitle"]/b[contains(text(),"DNS")]/../following-sibling::*[1]//a/text()')])
                # tre
                record_update_time = pop(
                    tre.xpath(
                        './td[1]/div[@class="stitle"]/b[contains(text(),"Record Update Time")]/../following-sibling::div/text()'))

                yield [No, web_site, web_site_ip_address, web_site_ipv6_address, website_popularity,
                       website_popularity_rating, dns_records, record_update_time]
        except IndexError:
            raise LoopOver
        if l < 50:
            with open('error.html', 'w', encoding='utf-8') as f:
                f.write(text)
            raise LoopOver

    def save_data(self, filename=None, path=None, item=None):
        if not filename:
            filename = self.csvfilename
        if not path:
            path = self.path
        with open('{}/{}'.format(path, filename), 'a', encoding='utf_8', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(item)


    def save_html_list(self, country, items, filename=None, path=None):
        tr = ''
        for item in items:
            t = ''
            for index, it in enumerate(item):
                if index == 1:
                    td = '<td><a href="./data/{}-{}.html">{}</a></td>'.format(
                        country, it.replace("\\", "").replace("/", "").replace(":", "").replace("*", "").replace("?",
                                                                                                                 "").replace(
                            "\"", "").replace("<", "").replace(">", "").replace("|", ""), it)
                else:
                    td = '<td>{}</td>'.format(it)
                t += td
            tr += '<tr>' + t + '</tr>'
        with open('main.html', 'a', encoding='utf-8') as f:
            f.write(self.tempalte.format(country, tr))

    def save_html_page(self, country, items, filename=None, path=None, it=None):
        if not os.path.exists(path):
            os.mkdir(path)
        tr = ''
        for index, item in enumerate(items):
            t = ''
            for it in item:
                td = '<td>{}</td>'.format(it)
                t += td
            tr += '<tr>' + t + '</tr>'
        with open('./{}/{}'.format(path, filename), 'w', encoding='utf-8') as f:
            f.write(self.tempalte_page.format(tr))

    @property
    def time(self):
        return '总共用时：{}秒'.format(self.runtime)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    print(spider.time)  # 运行总时间