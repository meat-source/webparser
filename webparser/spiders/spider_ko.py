import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose

from webparser.items import ArticleItem
from urllib.parse import urljoin


class ExampleSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)


class Spider_rusjurist(scrapy.Spider):
    name = "rusjurist"
    allowed_domains = ['rusjurist.ru']
    start_urls = [
        'https://rusjurist.ru/rospotrebnadzor/uvedomlenie_v_rospotrebnadzor_o_nachale_predprinimatelskoj_deyatelnosti/',
        # 'https://rusjurist.ru/rospotrebnadzor/shtrafy_rospotrebnadzora_dlya_yuridicheskih_lic/',
    ]

    def parse(self, response):
        l = ItemLoader(item=ArticleItem(), response=response)
        l.add_xpath('url', response.url.split("/")[-2])
        l.add_xpath('title', "//title/text()")
        l.add_xpath('h1', "//h1[@class='article_title']/text()")
        l.add_xpath('html', "//div[@class='article_lid']")
        l.add_xpath('html', "//div[@class='article_content text-content']")
        l.add_xpath('author', "//a[@class='article_author_link']/text()")
        l.add_xpath('image_urls', "//img/@src", MapCompose(lambda i: urljoin(response.url, i)))
        yield l.load_item()
