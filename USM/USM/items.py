# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UsmItem(scrapy.Item):
    title = scrapy.Field()
    cite = scrapy.Field()
    text = scrapy.Field()
    id_person = scrapy.Field()
    search = scrapy.Field()
    attr = scrapy.Field()
    engine_search = scrapy.Field()
    number_snippet = scrapy.Field()
