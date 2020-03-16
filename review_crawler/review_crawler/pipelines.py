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
                session.add(record)
                session.commit()
            except:
                import ipdb; ipdb.set_trace()
                session.rollback()
                raise
            finally:
                session.close()

        return item
