# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=Join)
    article_id = scrapy.Field(output_processor=TakeFirst)
    images = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst)
    list_page = scrapy.Field(output_processor=TakeFirst)
    price = scrapy.Field(output_processor=TakeFirst)
    stock = scrapy.Field(output_processor=TakeFirst)
    currency = scrapy.Field(output_processor=TakeFirst)
    description = scrapy.Field(output_processor=Join)
    vendor_id = scrapy.Field(output_processor=TakeFirst)


class ReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass