#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note Adjust the DOWNLOAD_DELAY

import scrapy
from scrapy import Selector
from scrapy.http import FormRequest, Request
from items import UsmItem
from tools.basic_tool import Utils

__author__ = "Josué Fabricio Urbina González"


class GoogleSpider(scrapy.Spider):

    name = "googlespider"
    start_urls = ["https://www.google.com.mx/"]
    browser = 1
    custom_settings = {'DOWNLOAD_DELAY': '5'}

    def __init__(self, source=None, *args, **kwargs):
        super(GoogleSpider, self).__init__(*args, **kwargs)
        if source is not None:
            self.source = source
        else:
            self.source = ""

    def parse(self, response):
        type_b = self.source[-1]
        if self.source != "":
            if type_b == "1":
                search = Utils.get_query_param(self.source)

                request = FormRequest.from_response(response,
                                                    formdata={'q': search[2]},
                                                    callback=self.google_selector)
                request.meta['id_person'] = search[0]
                request.meta['attr'] = search[1]
                request.meta['search'] = search[2]
                request.meta['num_snip'] = 0
                yield request

    def google_selector(self, response):
        base_url = "https://www.google.com.mx/"
        snippets = response.xpath("//div[@class='g']").extract()
        itemproc = self.crawler.engine.scraper.itemproc

        id_person = response.meta['id_person']
        base_attr = response.meta['attr']
        search = response.meta['search']
        num_snippet = response.meta['num_snip']

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//a/b/text() | //a/text()").extract()
            cite = Selector(text=snippet).xpath("//cite").extract()
            # cite = Selector(text=snippet).xpath("//h3/a/@href").extract()

            text = Selector(text=snippet).xpath("//span[@class='st']").extract()

            if title.__len__() >= 2:
                title = title[0]+title[1]
            else:
                title=""

            if cite.__len__() > 0:
                # cite = cite[0].split("url?q=")[-1]
                cite = cite[0]
                for r in ['<cite>', '</cite>', '<b>', '</b>', '<cite class="kv">', '</cite class="kv">']:
                    cite = cite.replace(r, '')
            else:
                cite = ""

            if text.__len__() > 0:
                text = text[0]
                for r in ['<span class="st">', '</span>', '<br>', '</br>', '<b>', '</b>', '<span class="f">',
                          '<span class="nobr">']:
                    text = text.replace(r, '')
            else:
                text = ""

            if cite != "":
                # Todo Filter snippets here



                num_snippet = num_snippet + 1
                self.log("---------------------------------")
                self.log("--------------TITLE--------------")
                self.log(title)
                self.log("-------------CITE----------------")
                self.log(cite)
                self.log("---------------TEXT--------------")
                self.log(text)
                self.log("------------ID PERSON------------")
                self.log(id_person)
                self.log("------------SEARCH---------------")
                self.log(search)
                self.log("--------------ATTR---------------")
                self.log(base_attr)
                self.log("-----------ENGINE SEARCH---------")
                self.log(self.browser)
                self.log("------------NUMBER SNIPPET-------")
                self.log(num_snippet)

                storage_item['title'] = title
                storage_item['cite'] = cite
                storage_item['text'] = text
                storage_item['id_person'] = id_person
                storage_item['search'] = search
                storage_item['attr'] = base_attr
                storage_item['engine_search'] = self.browser
                storage_item['number_snippet'] = num_snippet

                itemproc.process_item(storage_item, self)

        number = response.xpath("//td/b/text()").extract()
        self.log("-----------NUMBER OF PAGE-----")
        self.log(number[0] + "")
        if int(number[0]) < 6:
            res = response.xpath("//td[@class='b'][@style='text-align:left']/a[@class='fl']/@href").extract()

            for url in res:
                self.log("--URL TO FOLLOW--")
                self.log(base_url + url)
                request = Request(base_url + url, callback=self.google_selector)
                request.meta['id_person'] = id_person
                request.meta['search'] = search
                request.meta['attr'] = base_attr
                request.meta['num_snip'] = num_snippet
                yield request
