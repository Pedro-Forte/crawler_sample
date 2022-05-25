import scrapy


class BasicInfoSpider(scrapy.Spider):
    name = 'basic_info'
    allowed_domains = ['www.cialdnb.com']
    start_urls = ['http://www.cialdnb.com/']

    def parse(self, response):
        pass
