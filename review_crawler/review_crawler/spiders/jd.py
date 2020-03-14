# -*- coding: utf-8 -*-
import scrapy
from review_crawler.items import ReviewCrawlerItem
from scrapy.loader import ItemLoader

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = [
        'https://list.jd.com/list.html?cat=670,671,2694&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0/']

    def parse(self, response):
        listing_page_items = response.css('.gl-item')
        for item in listing_page_items:
            url = item.css('.p-img a::attr(href)').get()
            yield response.follow(url, callback=self.parse_product, meta=response.meta)
        next_page = response.css()
        yield response

    def parse_product(self, response):
        import ipdb
        ipdb.set_trace()

    def parse_review(self, response):
        import ipdb
        ipdb.set_trace()