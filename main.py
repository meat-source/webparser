from scrapy.crawler import CrawlerProcess
from webparser.spiders.spider_ko import *
# Загружаем настройки проекта (файл settings)
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(Spider_rusjurist)
process.start()