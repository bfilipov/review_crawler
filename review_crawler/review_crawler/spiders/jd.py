# -*- coding: utf-8 -*-
import scrapy
from review_crawler.items import ProductItem, ReviewItem
from scrapy.loader import ItemLoader

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    start_urls = [
        'https://list.jd.com/list.html?cat=670,671,2694&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0/']

    def parse(self, response):
        meta = response.meta
        meta.update({'list_page': response.url})
        listing_page_items = response.css('.gl-item')
        for item in listing_page_items:
            url = item.css('.p-img a::attr(href)').get()
            yield response.follow(url, callback=self.parse_product, meta=meta)
        next_page = response.css('.pn-next::attr(href)').get()
        if next_page:
            yield response.follow(response.urljoin(next_page), callback=self.parse, meta=meta)

    def parse_product(self, response):
        meta = response.meta
        loader = ItemLoader(ProductItem(), selector=response)
        import ipdb
        ipdb.set_trace()

    def parse_review(self, response):
        # get summary of comments (GET METHOD)
        # https://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId=100002716279
        import ipdb
        ipdb.set_trace()