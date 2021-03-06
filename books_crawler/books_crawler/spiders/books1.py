from scrapy import Spider
from selenium import webdriver
from scrapy.selector import Selector
from scrapy.http import Request
from time import sleep
from selenium.common.exceptions import NosuchElementException

class Books1Spider(Spider):
    name = 'books1'
    allowed_domains = ['books.toscrape.com']
    
    def start_requests(self):
        self.driver = webdriver.Chrome('path')
        self.driver.get('site')
        sel = Selector(text=self.driver.page_source)
        books =  sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)
        
        while True:
            try:
                next_page = self.driver.find_element_by_xpath('//a[text()="next"]').click()
                sleep(3)
                self.logger.info('Sleeping for 3 seconds')
                next_page.click()
                sel = Selector(text=self.driver.page_source)
                books =  sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)
                
            except NoSuchElementException:
                self.logger.info('No more pages to load.')
                self.driver.quit()
                break
            
                
    def parse_book():
        pass
