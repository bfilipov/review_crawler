# -*- coding: utf-8 -*-
import csv
from scrapy.utils.project import get_project_settings
from sqlalchemy.orm import sessionmaker
from review_crawler.models import Products, Reviews, db_connect, create_tables


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ReviewCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item


class WriteToCsv(object):

    write_headers_products = True
    write_headers_reviews = True
    settings = get_project_settings()

    @staticmethod
    def get_path(item):
        if item.get('article_id'):
            return 'CSV_PATH_PRODUCTS'
        elif item.get('review_id'):
            return 'CSV_PATH_REVIEWS'

    def write_headers_first_time(self, item):

        path = self.get_path(item)
        if self.write_headers_products and item.get('article_id'):
            writer = csv.writer(open(self.settings.get(path), 'w'), lineterminator='\n')
            writer.writerow([key for key in item.keys()])
            self.write_headers_products = False

        elif self.write_headers_reviews and item.get('guid'):
            writer = csv.writer(open(self.settings.get(path), 'w'), lineterminator='\n')
            writer.writerow([key for key in item.keys()])
            self.write_headers_reviews = False

    def process_item(self, item, spider):
        self.write_headers_first_time(item)
        path = self.get_path(item)
        if not path:
            return None
        self.write_to_csv(item, path)
        return item

    def write_to_csv(self, item, path):
        writer = csv.writer(open(self.settings.get(path), 'a'), lineterminator='\n')
        writer.writerow([item[key] for key in item.keys()])


class PostgresPipeline(object):
    """Livingsocial pipeline for storing scraped items in the database"""
    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.Session()
        record = None
        if item.get('guid'):
            record = Reviews(**item)
        elif item.get('article_id'):
            record = Products(**item)
        if record:
            try:
                session.merge(record)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item
