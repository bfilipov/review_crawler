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
    comments_request_length = 10
    review_url = 'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment98&' \
                 'productId={0}&score=0&sortType=5&page={1}&pageSize={2}&isShadowSku=0&rid=0&fold=1'

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

        url = response.url
        article_id = self.extract_id_from_url(url)
        if not article_id:
            return
        product_loader.add_value('article_id', article_id)
        meta.update({'product_id': article_id})
        meta.update({'product_url': url})
        product_loader.add_value('url', url)
        product_loader.add_value('list_page', meta.get('list_page', ''))
        product_loader.add_css('images', '.lh li img::attr(src)')
        product_loader.add_css('title', '.sku-name::text')
        product_loader.add_css('currency', '.p-price span::text')
        product_loader.add_css('description', '.parameter2.p-parameter-list *::text')
        vendor_id = self.get_vendor_id(response)
        product_loader.add_value('vendor_id', vendor_id)
        yield self.get_stock_and_price(product_loader)
        yield response.follow(self.review_url.format(article_id, '0', self.comments_request_length),
                              callback=self.parse_review, meta=meta)

    def parse_review(self, response):
        meta = response.meta
        meta.setdefault('current_page', 0)
        body = re.search(r'fetchJSON_comment98\((.*)\);', response.text, re.IGNORECASE)
        dct = json.loads(body.group(1)) if body else {}
        comments = dct.get('comments', [])
        product_id = meta.get('product_id', '')
        product_url = meta.get('product_url', '')
        if not product_id:
            return
        for comment in comments:
            loader = ItemLoader(ReviewItem())
            loader.add_value('product_id', product_id)
            loader.add_value('product_url', product_url)
            loader.add_value('review_text', comment.get('content', ''))
            loader.add_value('review_id', comment.get('id', ''))
            loader.add_value('guid', comment.get('guid', ''))
            loader.add_value('images_count', comment.get('imageCount', ''))
            loader.add_value('creation_time', comment.get('creationTime', ''))
            loader.add_value('images', comment.get('images', []))
            loader.add_value('reviewer', comment.get('nickname', ''))
            loader.add_value('product_color', comment.get('productColor', ''))
            loader.add_value('product_sales', comment.get('productSales', ''))
            loader.add_value('product_size', comment.get('productSize', ''))
            loader.add_value('videos', comment.get('videos', []))
            loader.add_value('reply_count', comment.get('replyCount', ''))
            loader.add_value('reply_count_2', comment.get('replyCount2', ''))
            loader.add_value('review_score', comment.get('score', ''))
            loader.add_value('useful_vote_count', comment.get('usefulVoteCount', ''))
            yield loader.load_item()
        if len(comments) == self.comments_request_length:
            meta.update({'current_page': meta.get('current_page') + 1})
            next_page = meta.get('current_page')
            yield response.follow(self.review_url.format(product_id, next_page, self.comments_request_length),
                                  callback=self.parse_review, meta=meta)

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
