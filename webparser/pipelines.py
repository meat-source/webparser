import hashlib
import json
import unicodedata

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from lxml.html.clean import Cleaner
from w3lib import html as w3lib_html
from w3lib import url as w3lib_url
from w3lib import encoding as w3lib_encoding
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from w3lib.util import to_bytes


def w3lib_cleaner(el):
    # Нормализуем символы &nbsp; и прочие
    el = unicodedata.normalize('NFKC', el)
    # Удалить escape-символы.
    el = w3lib_html.replace_escape_chars(el)
    # Удалите все начальные и конечные пробелы
    el = w3lib_html.strip_html5_whitespace(el)
    # Удалить большие пробелы
    el = el.replace('  ', '')
    el = w3lib_html.replace_entities(el, remove_illegal=True, encoding='utf-8')
    # Удаляем теги вместе с содержимым
    el = w3lib_html.remove_tags_with_content(el, which_ones=('noidex', 'iframe', 'form'))
    # Оставляем разрешенные теги и содержимое
    # (! КАКИМ ТО ВОЛШЕБНЫМ ОБРАЗОМ ТЕКСТ ОСТАВШИЙСЯ БЕЗ ВНЕШНЕГО ТЕГА ОБОРАЧИВАЕТСЯ в <p>
    # и это хорошо)
    allowed_tag = ('p', 'img', 'a', 'b', 'i', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'li', 'ins')
    el = w3lib_html.remove_tags(el, keep=allowed_tag)
    return el


class CleanHTMLPipeline:

    # def file_path(self, request, response=None, info=None):
    #     image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    #     return 'realty-sc/%s/%s/%s/%s.jpg' % ('YEAR', image_guid[:2], image_guid[2:4], image_guid)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('html'):
            cleaner = Cleaner(safe_attrs_only=True, safe_attrs={'src', 'alt', 'href', 'title'})
            adapter['html'] = cleaner.clean_html(adapter['html'])
            adapter['html'] = w3lib_cleaner(adapter['html'])
            if adapter.get('images'):
                for img in adapter.get('images'):
                    adapter['html'] = adapter['html'].replace(img['url'], img['path'])

        if adapter.get('h1'):
            adapter['h1'] = w3lib_html.strip_html5_whitespace(adapter['h1'])
        if adapter.get('title'):
            adapter['title'] = w3lib_html.strip_html5_whitespace(adapter['title'])
        if adapter.get('author'):
            adapter['author'] = w3lib_html.strip_html5_whitespace(adapter['author'])
        return item


class SaveFilePoppeLine():
    def open_spider(self, spider):
        self.file = open('start.html', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        html = """<!DOCTYPE HTML><html lang="ru"><head><meta charset="UTF-8">
            <title>Название страницы</title><meta name="description" content="Описание страницы" /></head><body>"""

        adapter = ItemAdapter(item)
        self.file.write(html)
        for key in adapter.keys():
            if key not in ['images', 'image_urls', 'files', 'file_urls']:
                self.file.write(str(adapter[key]))
                self.file.write('\n')
        self.file.write('</body>')
        return item
