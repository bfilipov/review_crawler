# -*- coding: utf-8 -*-
import os

# Scrapy settings for review_crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'review_crawler'

SPIDER_MODULES = ['review_crawler.spiders']
NEWSPIDER_MODULE = 'review_crawler.spiders'

DNS_TIMEOUT = 15
DOWNLOAD_TIMEOUT = 15

# most common user agents from:
# https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
USER_AGENT_CHOICES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/79.0.3945.130 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/80.0.3987.122 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/80.0.3987.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) '
    'Version/13.0.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/80.0.3987.116 Safari/537.36',
]


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# generate proxy file with: python proxy_generator.py > proxies
ROTATING_PROXY_LIST_PATH = os.path.realpath(os.path.join(os.getcwd(), 'proxies'))

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
HTTPCACHE_ENABLED = True  # should be true in debug only\

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_TARGET_CONCURRENCY = 3
AUTOTHROTTLE_DEBUG = True
CONCURRENT_REQUESTS = 3
DOWNLOAD_DELAY = 3
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'review_crawler.middlewares.ReviewCrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'review_crawler.middlewares.RotateUserAgentMiddleware': 110,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
    'review_crawler.middlewares.ReviewCrawlerDownloaderMiddleware': 543,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'review_crawler.pipelines.ReviewCrawlerPipeline': 300,
# }

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
