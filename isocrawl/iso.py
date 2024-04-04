import multiprocessing
import subprocess
import json
from time import sleep
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
import scrapy
from scrapy.crawler import CrawlerProcess
import requests
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.exceptions import NotConfigured
import random
import tkinter as tk


#quản lý proxy
class RotateProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxies = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ROTATE_PROXY_ENABLED'):
            raise NotConfigured
        proxy_list = [
            # Danh sách các proxy
            # 'http://proxy1:port1',
            'http://vip3.4gre.net:80',
            # Thêm proxy khác nếu cần
        ]
        return cls(proxy_list)

    def process_request(self, request, spider):
        # Chọn một proxy từ danh sách và cấu hình request để sử dụng nó
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy

def crawl_api():
    number_links = int(input('Enter the number of links needed: '))
    URL = "https://jcl49wv5ar-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.22.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.64.3)%3B%20JS%20Helper%20(3.16.2)&x-algolia-api-key=MzcxYjJlODU3ZmEwYmRhZTc0NTZlODNlZmUwYzVjNDRiZDEzMzRjMjYwNTAwODU3YmIzNjEwZmNjNDFlOTBjYXJlc3RyaWN0SW5kaWNlcz1QUk9EX2lzb29yZ19lbiUyQ1BST0RfaXNvb3JnX2VuX2F1dG9jb21wbGV0ZQ%3D%3D&x-algolia-application-id=JCL49WV5AR"

    data = []
    page = 0
    links=[]
    check=True 
    while True :
        json_data = {
            "requests": [
                {
                    "indexName": "PROD_isoorg_en",
                    "params": f"clickAnalytics=true&facetFilters=%5B%5B%22facet%3Astandard%22%5D%5D&facets=%5B%22facet%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&maxValuesPerFacet=10&page={page}&query=iec&tagFilters=&userToken=anonymous-091345c9-5a26-40a9-b501-3bcf5177ba7d"
                }
            ]
        }
        r = requests.post(url=URL, json=json_data)

        # extracting data in json format
        data = r.json()['results'][0]['hits']
        for i in data:
            links.append("https://www.iso.org/"+ i['seoURL'])
            if len(links) == number_links:
                check= False 
                break
        if check == False :
            break
    return links
# Example usage:
# crawled_data = crawl_api()
# print(crawled_data)

#hàm tìm kiếm nâng cao


def advanced_finding():
    
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--force-device-scale-factor=0.5")
    driver = webdriver.Chrome(service=service, options=options) 
    
    driver.get('https://www.iso.org/advanced-search/x/')
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    #nhập tiêu đê của chuẩn
    abstractKey = driver.find_element(By.ID, 'formKeyword')
    abstractKey.send_keys(input('Nhập tiêu đề của chuẩn : '))
    #nhập thời gian chuẩn ra đời(từ năm-tháng-ngày đến năm-tháng-ngày)
    blank_area= driver.find_element(By.XPATH, '//body')
    fromStageform = driver.find_element(By.ID, 'formStageFrom')
    fromStageform.send_keys(input('Please enter the Form Stage from(yyyy-mm-dd) :'))
    blank_area.click()
    desired_y_position = 1000
    script = f"window.scrollTo(0, {desired_y_position});"
    driver.execute_script(script)
    time.sleep(5)
    ques= input('Bạn có muón giới hạn thời gian của chuẩn:  Yes or No ')
    
    #nếu có, nhập thời gian của chuẩn
    if ques=='Yes':
        blank_area.click()
        formStageTo= driver.find_element(By.ID,'formStageTo')
        formStageTo.send_keys(input('Please enter the Form Stage To(yyyy-mm-dd) :'))
    else : 
        driver.find_element(By.XPATH, "/html/body/main/div[1]/section[2]/div/div/div[1]/form/div/div[2]/div/button[2]").click()
        time.sleep(4)
        
    numb= int(input('Nhập số lượng chuẩn cần tìm: '))
    standard_link=[]
    index=1
    check = True
    desired_y_position = 2000
    
    for i in range(numb // 10):
    
        time.sleep(5)
        script = f"window.scrollTo(0, {desired_y_position});"
        driver.execute_script(script)
        
        div_get_link = driver.find_element(By.ID, 'search-results')
        a_tag_link = div_get_link.find_elements(By.CLASS_NAME, 'h5')
        
        # Lặp qua từng liên kết và thu thập vào mảng standard_link
        for link in a_tag_link:
            standard_link.append((link.find_element(By.TAG_NAME, 'a')).get_attribute("href"))
            if len(standard_link) == numb:
                break  # Nếu đã thu thập đủ số lượng liên kết cần tìm, thoát khỏi vòng lặp
        
        link_text = str(index + 1)
        link =driver.find_element(By.XPATH, f"//a[@class='page-link ng-binding' and text()='{link_text}']")
        link.click()
        # Cập nhật chỉ số trang
        index += 1
    return standard_link
    

    
#crawl  all pages of search results using API call
class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    output_file = 'data.json'
    custom_settings = {
        'DOWNLOAD_DELAY': 5,  # Adjust the delay as needed (in seconds)
        'CONCURRENT_REQUESTS': 5 # Adjust the number of concurrent requests as needed
    }

    def __init__(self, links=[], *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = links
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = {
            'url': response.url,
            'info': {}
        }



        self.get_nav_elements(data, response)
        self.get_price(data, response)
        self.get_description(data, response)
        yield from self.get_h4_element(data, response)

    def get_nav_elements(self, data, response):
        nav_elements = response.css('nav.heading-condensed.nav-relatives *::text').getall()
        data['info']['nav_elements'] = ''.join(nav_elements).strip()

    def get_price(self, data, response):
        price_element = response.css('li.price.order')
        if price_element:
            currency = price_element.css('span.currency::text').get()
            amount = price_element.css('span.amount::text').get()
            data['info']['price'] = {"currency": currency, "amount": amount}
        else:
            data['info']['price'] = "Không tìm thấy giá"

    def get_description(self, data, response):
        description_element = response.css('div[itemprop="description"]')
        if description_element:
            description = description_element.css('p::text').getall()
            data['info']['description'] = ' '.join(description).strip()
        else:
            data['info']['description'] = "Không tìm thấy mô tả"

    def get_h4_element(self, data, response):
        h4_elements = response.css('h4.h5.entry-title.entry-name')
        if h4_elements:
            for h4_element in h4_elements:
                link = h4_element.css('a::attr(href)').get()
                data_copy = data.copy()
                data_copy['info']['link'] = link
                yield scrapy.Request(url=link, callback=self.parse_additional_content, meta={'data': data_copy})
        else :
            data['info']['link']= "không có link"

    def parse_additional_content(self, response):
        data = response.meta.get('data', {})
        sts_standard_element = response.css('div.sts-standard')
        if sts_standard_element:
            additional_content = sts_standard_element.css('::text').getall()
            data['info']['additional_content'] = ' '.join(additional_content).strip()
        else:
            data['info']['additional_content'] = "Không tìm thấy nội dung bổ sung"
        self.save_data(data)

    def save_data(self, data):
        with open(self.output_file, 'a') as f:
            f.write(json.dumps(data, indent=4) + '\n')
            
#hỏi loại tìm kiếm 
def type_of_finding():
    ask =int(input('Chọn loại tìm kiếm, ấn 1 để tìm kiếm nâng cao, 2 để tìm kiếm thông thường: '))
    return ask

if __name__ == "__main__":
    # Khởi tạo một quy trình crawler
    choosen = type_of_finding()
    if choosen == 1:
        links = advanced_finding()
        
        
        
    else:
        crawl_api()
        links = crawl_api()
        
    
    process = CrawlerProcess()

    # Thêm spider vào quy trình
    process.crawl(LinkSpider, links=links)

    # Bắt đầu quy trình crawler
    process.start()
    