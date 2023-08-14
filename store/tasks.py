from celery import shared_task, Celery
from threading import Thread
import os
from .update_products import FeedParser, ProductUpdater


app = Celery()


@shared_task
def make_goods_update():
    feed_url = os.environ.get('GOODS_FEED_URL')
    feed_parser = FeedParser(feed_url)
    product_updater = ProductUpdater(feed_parser)
    Thread(target=product_updater.update_products, args=()).start()
