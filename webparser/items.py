# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import Join

import scrapy
from w3lib.html import remove_tags


def html_processor(arg):
    print(arg)
    return arg


class ArticleItem(scrapy.Item):
    title = scrapy.Field(output_processor=Join())
    h1 = scrapy.Field(output_processor=Join())
    html = scrapy.Field(output_processor=Join())
    author = scrapy.Field(output_processor=Join())
    url = scrapy.Field(output_processor=Join())
    images = scrapy.Field()
    image_urls = scrapy.Field()

