# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class ProductItem(scrapy.Item):
    title = scrapy.Field(output_processor=Join())
    article_id = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    list_page = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    stock = scrapy.Field(output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=Join())
    vendor_id = scrapy.Field(output_processor=TakeFirst())


class ReviewItem(scrapy.Item):
    product_id = scrapy.Field(output_processor=TakeFirst())
    product_url = scrapy.Field(output_processor=TakeFirst())
    review_text = scrapy.Field(output_processor=TakeFirst())
    review_id = scrapy.Field(output_processor=TakeFirst())
    guid = scrapy.Field(output_processor=TakeFirst())
    images_count = scrapy.Field(output_processor=TakeFirst())
    creation_time = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field()
    reviewer = scrapy.Field(output_processor=TakeFirst())
    product_color = scrapy.Field(output_processor=TakeFirst())
    product_sales = scrapy.Field(output_processor=TakeFirst())
    product_size = scrapy.Field(output_processor=TakeFirst())
    videos = scrapy.Field()
    reply_count = scrapy.Field(output_processor=TakeFirst())
    reply_count_2 = scrapy.Field(output_processor=TakeFirst())
    review_score = scrapy.Field(output_processor=TakeFirst())
    useful_vote_count = scrapy.Field(output_processor=TakeFirst())


class QAItem(scrapy.Item):
    pass