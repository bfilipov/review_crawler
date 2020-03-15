# -*- coding: utf-8 -*-
import csv
from scrapy.utils.project import get_project_settings

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ReviewCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class WriteToCsv(object):
    def process_item(self, item, spider):
        if item.get('article_id'):
            path = 'CSV_PATH_PRODUCTS'
        elif item.get('review_id'):
            path = 'CSV_PATH_REVIEWS'
        # elif item.get('some QA id'):
        #     path = 'CSV_PATH_QA'
        else:
            return None
        write_to_csv(item, path)
        return item


def write_to_csv(item, path):
    settings = get_project_settings()
    writer = csv.writer(open(settings.get(path), 'a'), lineterminator='\n')
    writer.writerow([item[key] for key in item.keys()])
