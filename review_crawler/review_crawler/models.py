from sqlalchemy import create_engine, ARRAY, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.get('DATABASE')))


def create_tables(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Products(DeclarativeBase):
    """Sqlalchemy products model"""
    __tablename__ = "products"

    article_id = Column('article_id', String, primary_key=True)
    title = Column('title', String)
    images = Column('images', ARRAY(String))
    url = Column('url', String)
    list_page = Column('list_page', String)
    price = Column('price', String)
    stock = Column('stock', String)
    currency = Column('currency', String)
    description = Column('description', String)
    vendor_id = Column('vendor_id', String)
    reviews = relationship("Reviews")


class Reviews(DeclarativeBase):
    """Sqlalchemy reviews model"""
    __tablename__ = "reviews"

    guid = Column('guid', String, primary_key=True)
    product_id = Column('product_id', ForeignKey('products.article_id'))
    product_url = Column('product_url', String)
    review_text = Column('review_text', String)
    review_id = Column('review_id', String)
    images_count = Column('images_count', Integer)
    creation_time = Column('creation_time', DateTime)
    images = Column('images', ARRAY(String))
    reviewer = Column('reviewer', String)
    product_color = Column('product_color', String)
    product_sales = Column('product_sales', String)
    product_size = Column('product_size', String)
    videos = Column('videos', ARRAY(String))
    reply_count = Column('reply_count', String)
    reply_count_2 = Column('reply_count_2', String)
    review_score = Column('review_score', String)
    useful_vote_count = Column('useful_vote_count', String)
