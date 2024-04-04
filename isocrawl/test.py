import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy import signals
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
import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher

class AdvancedFindingSpider(scrapy.Spider):
    name = 'advanced_finding'
    start_urls = ['https://www.iso.org/advanced-search/x/']

    def __init__(self):
        self.service = Service('path_to_chromedriver')  # Replace 'path_to_chromedriver' with the path to your chromedriver executable
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.standard_links = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(AdvancedFindingSpider, cls).from_crawler(crawler, *args, **kwargs)
        dispatcher.connect(spider.spider_closed, signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.driver.quit()

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        
        abstract_key = self.driver.find_element(By.ID, 'formKeyword')
        abstract_key.send_keys(input('Nhập tiêu đề của chuẩn : '))
        
        from_stage_form = self.driver.find_element(By.ID, 'formStageFrom')
        from_stage_form.send_keys(input('Please enter the Form Stage from(yyyy-mm-dd) :'))
        
        desired_y_position = 1000
        script = f"window.scrollTo(0, {desired_y_position});"
        self.driver.execute_script(script)
        time.sleep(5)
        
        question = input('Bạn có muốn giới hạn thời gian của chuẩn: Yes or No ')
        
        if question == 'Yes':
            form_stage_to = self.driver.find_element(By.ID,'formStageTo')
            form_stage_to.send_keys(input('Please enter the Form Stage To(yyyy-mm-dd) :'))
        else: 
            self.driver.find_element(By.XPATH, "/html/body/main/div[1]/section[2]/div/div/div[1]/form/div/div[2]/div/button[2]").click()
            time.sleep(4)
            
        num = int(input('Nhập số lượng chuẩn cần tìm: '))

        while len(self.standard_links) != num:
            html = self.driver.page_source
            response_obj = HtmlResponse(url=self.driver.current_url, body=html, encoding='utf-8')
            sel = Selector(response=response_obj)
            div_get_link = sel.xpath('//*[@id="search-results"]')
            a_tag_link = div_get_link.xpath('.//h5/a/@href').extract()
            self.standard_links.extend(a_tag_link)
            
            desired_y_position += 2500
            script = f"window.scrollTo(0, {desired_y_position});"
            self.driver.execute_script(script)
            time.sleep(3)

            index += 1
            link_text = str(index + 1)
            next_page = self.driver.find_element(By.XPATH, f"//a[@class='page-link ng-binding' and text()='{link_text}']")
            next_page.click()

        for link in self.standard_links:
            yield {
                'standard_link': link
            }

    def get_standard_links(self):
        return self.standard_links

if __name__ == "__main__":
    process = CrawlerRunner()
    process.crawl(AdvancedFindingSpider)
    process.start()
