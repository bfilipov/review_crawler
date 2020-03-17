## Setup

 create virtual environment using conda and install required packages:  
 ```
 conda create --name=review_crawler python=3.7     
 conda activate review_crawler     
 git clone git@github.com:bfilipov/review_crawler.git   
 cd review_crawler   
 pip install -r requirements.txt  
``` 
 

### run crawler:  
 `scrapy crawl jd`   
 
---

### Task:

The task is to scrpape user reviews for tablet products from jd.com.

We first inspect the site. We can see that on the listing page and product page we have most of 
the info about the items in the html document response. In the product page the price and stock 
are loaded dynamically as well the reviews. 

We will use relational database with two tables - one for products and one for reviews, using one
 to one relation with product's id. We will use upsert operation, on each item, thus we will have 
 the latest state of the data. We are not interested in creating history tables for now.
 
In order not to get banned to quickly we are going to create a script using ProxyBroker in order to 
get free public proxies for the scraping task. Next we will use few of the most common used 
user-agent headers that we will rotate along with the proxies. 

---
### Spider:

We generate a new spider and append to the start_urls variable the tablets listing page url:

```
start_urls = [
        'https://list.jd.com/list.html?cat=670,671,2694&page=1&sort=sort_totalsales15_desc&trans=1&JL=6_0_0/']
```

Parse method will be called for each start url. For each item on the listing page we are extracting
 the url and calling parse_product method. We then call the same function on the next_page url, 
 until we reach the last listing page and no next page selector is present.
 
 ```
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
```
 
 On the product page we have almost all of the product information except the price and the stock info,
 which are loaded with additional ajax request. We need to find all selectors in the html for the needed 
 fields, which are defined in the ProductItem class in items module and add them to the ItemLoader instance. 
 After that we load the item to the database and yield two requests for price/stock and reviews APIs.
 
 ```
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
        product = product_loader.load_item()
        yield product
        yield self.get_stock_and_price(product)
        yield response.follow(self.review_url.format(article_id, '0', self.comments_request_length),
                              callback=self.parse_review, meta=meta)
```
 
 We then make a GET request to the price/stock api. If the request sucseeds we add them to the loader 
 and we load the iteam again to update record in the database.
 
 ```
    def get_stock_and_price(self, product):
        art_id = product.get('article_id')
        vendor_id = product.get('vendor_id')
        cat_m = re.search(r'cat=(.*?)(&|$)', product.get('list_page'), re.IGNORECASE)
        cat = cat_m.group(1) if cat_m else None
        url = f'https://c0.3.cn/stock?skuId={art_id}&area=53283_53362_0_0&venderId={vendor_id}&buyNum=1' \
              f'&choseSuitSkuIds=&cat={cat}'
        if art_id and vendor_id and cat:
            return scrapy.Request(url, callback=self.parse_stock_and_price, meta={'product': product})

    def parse_stock_and_price(self, response):
        product_loader = ItemLoader(ProductItem(response.meta.get('product', {})), selector=response)
        dct = json.loads(response.text)
        if dct:
            price = dct.get('stock', {}).get('jdPrice', {}).get('p', '')
            product_loader.add_value('price', price)
            stock = dct.get('stock', {}).get('StockStateName', '')
            product_loader.add_value('stock', stock)
        return product_loader.load_item()

```

We've simultaiously fired a request to the review api wich will be processed in parse_review.
We will call parse_reviews on each next page url until we reach the final review page. 

```
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
```

