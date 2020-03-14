### create virtual invironment and install required packages:
 conda create --name=review_crawler python=3.7
 conda activate review_crawler
 pip install scrapy
 pip install scrapy-rotating-proxies
 pip install proxybroker

### start project:
 scrapy startproject review_crawler
 cd review_crawler
 scrapy genspider jd jd.com

### setup:
 Using proxy broker we create a script to generate proxy list with 100 free proxies.
 We create custom rotating user agent middleware. 
 We set autothrottle, to slow down crawling.

### run project:
 scrapy crawl jd