import json
import random
import time
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Request
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
# Quản lý proxy
class RotateProxyMiddleware:
    def __init__(self, proxy_list):
        self.proxies = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('ROTATE_PROXY_ENABLED'):
            raise NotConfigured
        proxy_list = [
            'http://vip3.4gre.net:80',
            # Thêm proxy khác nếu cần
        ]
        return cls(proxy_list)

    def process_request(self, request, spider):
        # Chọn một proxy từ danh sách và cấu hình request để sử dụng nó
        proxy = random.choice(self.proxies)
        request.meta['proxy'] = proxy

# Hàm crawl API
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

# Hàm tìm kiếm nâng cao
def advanced_finding():
    # Tạo các yêu cầu Scrapy để tìm kiếm nâng cao
    # Sau đó, trả về danh sách liên kết được tìm thấy
    # Để đơn giản, chúng ta có thể trả về một danh sách trống ở đây
    return []

# Spider để thu thập dữ liệu từ các liên kết
class LinkSpider(scrapy.Spider):
    name = 'link_spider'
    start_urls = []

    def __init__(self, links=[], *args, **kwargs):
        super(LinkSpider, self).__init__(*args, **kwargs)
        self.start_urls = links

    def parse(self, response):
        # Xử lý các yêu cầu và phân tích cú pháp ở đây
        pass

# Hỏi loại tìm kiếm
def type_of_finding():
    ask =int(input('Chọn loại tìm kiếm, ấn 1 để tìm kiếm nâng cao, 2 để tìm kiếm thông thường: '))
    return ask

if __name__ == "__main__":
    # Khởi tạo một quy trình crawler
    choosen = type_of_finding()
    if choosen == 1:
        links = advanced_finding()
    else:
        links = crawl_api()

    process = CrawlerProcess(settings={
        'DOWNLOAD_DELAY': 5,  # Điều chỉnh độ trễ nếu cần (tính bằng giây)
        'CONCURRENT_REQUESTS': 5,  # Điều chỉnh số lượng yêu cầu đồng thời nếu cần
        'ROBOTSTXT_OBEY': False,  # Bỏ qua file robots.txt
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'DOWNLOADER_MIDDLEWARES': {
            'your_project_name.middlewares.RotateProxyMiddleware': 610,
        },
    })

    # Thêm spider vào quy trình
    process.crawl(LinkSpider, links=links)

    # Bắt đầu quy trình crawler
    process.start()
