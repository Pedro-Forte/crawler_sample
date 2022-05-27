from scrapy.crawler import CrawlerProcess
from cialdnb.spiders.basic_info import BasicInfoSpider
import sys


process = CrawlerProcess(settings={
    "FEEDS": {
        "items.json": {"format": "json"},
    },
})

process.crawl(BasicInfoSpider, domain=sys.stdin.readlines())
process.start()
