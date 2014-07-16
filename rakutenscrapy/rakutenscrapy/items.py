# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RakutenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()

class RakutenItemDetail(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    jan = scrapy.Field()
    genre = scrapy.Field()
    description = scrapy.Field()
    maker = scrapy.Field()
    review = scrapy.Field()
    review_count = scrapy.Field()

class RakutenItemReview(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    genre = scrapy.Field()
    review = scrapy.Field()


