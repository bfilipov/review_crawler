# -*- coding: utf-8 -*-
import json
import re
import scrapy
from review_crawler.items import ProductItem, ReviewItem
from scrapy.loader import ItemLoader

class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com', '3.cn']
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
        product_loader = ItemLoader(ProductItem(), selector=response)
        review_loader = ItemLoader(ReviewItem(), selector=response)
        url = response.url
        article_id = self.extract_id_from_url(url)
        if not article_id:
            return
        product_loader.add_value('article_id', article_id)
        product_loader.add_value('url', url)
        product_loader.add_value('list_page', meta.get('list_page', ''))
        product_loader.add_css('images', '.lh li img::attr(src)')
        product_loader.add_css('title', '.sku-name::text')
        product_loader.add_css('currency', '.p-price span::text')
        product_loader.add_css('description', '.parameter2.p-parameter-list *::text')
        vendor_id = self.get_vendor_id(response)
        product_loader.add_value('vendor_id', vendor_id)
        yield self.get_stock_and_price(product_loader)
        reveiw_url = 
        yield response.follow( callback=self.parse_review)

    def parse_review(self, response):
        # get summary of comments (GET METHOD)
        # https://club.jd.com/ProductPageService.aspx?method=GetCommentSummaryBySkuId&referenceId=100002716279
        import ipdb
        ipdb.set_trace()

    @staticmethod
    def extract_id_from_url(url):
        art_id = re.search(r'jd\.com\/(\d.*?)\.html', url, re.IGNORECASE).group(1)
        return art_id

    @staticmethod
    def get_vendor_id(response):
        body = response.css('script[charset=gbk]::text').get()
        match = re.search(r'venderId:\s?(.*?),', body, re.IGNORECASE)
        return match.group(1) if match else ''

    def get_stock_and_price(self, product_loader):
        art_id = product_loader.get_collected_values('article_id')[0]
        vendor_id = product_loader.get_collected_values('vendor_id')[0]
        cat_m = re.search(r'cat=(.*?)(&|$)', product_loader.get_collected_values('list_page')[0], re.IGNORECASE)
        cat = cat_m.group(1) if cat_m else None
        url = f'https://c0.3.cn/stock?skuId={art_id}&area=53283_53362_0_0&venderId={vendor_id}&buyNum=1' \
              f'&choseSuitSkuIds=&cat={cat}'
        if art_id and vendor_id and cat:
            return scrapy.Request(url, callback=self.parse_stock_and_price, meta={'product': product_loader})
        return product_loader.load_item()

    def parse_stock_and_price(self, response):
        product_loader = response.meta.get('product')
        dct = json.loads(response.text)
        price = dct.get('stock', {}).get('jdPrice', {}).get('p', '')
        product_loader.add_value('price', price)
        stock = dct.get('stock', {}).get('StockStateName', '')
        product_loader.add_value('stock', stock)
        return product_loader.load_item()
