# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CialdnbItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    logo = scrapy.Field()
    phones = scrapy.Field()
    website = scrapy.Field()
