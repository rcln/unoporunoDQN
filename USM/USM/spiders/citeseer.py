#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest, Request
from scrapy import Selector
from items import UsmItem
from tools.basic_tool import Utils
from tools.filter import FeatureFilter, Cleaner
from datetime import datetime

__author__ = "Josué Fabricio Urbina González"


class CiteSearch(scrapy.Spider):
    name = "citespider"
    start_urls = ["http://citeseerx.ist.psu.edu/"]
    browser = 3
    STATUS_OK = 200

    def __init__(self, source=None, *args, **kwargs):
        super(CiteSearch, self).__init__(*args, **kwargs)
        if source is not None:
            self.source = source
        else:
            self.source = ""
        self.filter = None

    def parse(self, response):
        if response.status != self.STATUS_OK:
            pass

        type_b = self.source[-1]
        if self.source != "":
            if type_b == "1":
                search = Utils.get_query_param(self.source)

                request = FormRequest.from_response(response,
                                                    formdata={'q': search[2]},
                                                    callback=self.cite_selector)
                request.meta['id_person'] = search[0]
                request.meta['attr'] = search[1]
                request.meta['search'] = search[2]
                self.filter = FeatureFilter(search[3])
                request.meta['num_snip'] = 0
                yield request

    def cite_selector(self, response):
        # Utils.create_page(Utils(), response.body, "-citeseerx")

        if response.status != self.STATUS_OK:
            with open("error.log", "a") as log_file:
                log_file.write(response.status + " " + str(self.browser) + " " + datetime.today().strftime("%y-%m-%d-%H-%M"))
                return

        base_url = "http://citeseerx.ist.psu.edu/"
        snippets = response.xpath("//div[@class='result']").extract()
        itemproc = self.crawler.engine.scraper.itemproc

        id_person = response.meta['id_person']
        base_attr = response.meta['attr']
        search = response.meta['search']
        num_snippet = response.meta['num_snip']

        with open("system.log", "a") as log_file:
            log_file.write(response.status + " " + str(self.browser) + " " + str(search) + " " + str(num_snippet) + " " + datetime.today().strftime("%y-%m-%d-%H-%M"))

        for snippet in snippets:
            storage_item = UsmItem()

            title = Selector(text=snippet).xpath("//h3/a/node()").extract()
            # tmpTitle = Selector(text=snippet).xpath("//div[@class='pubinfo']")
            cite = Selector(text=snippet).xpath("//h3/a/@href").extract()
            text = Selector(text=snippet).xpath("//div[@class='snippet']/text()").extract()

            if title.__len__() > 0:
                tmp = ""
                for txt in title:
                    for r in ['<em>', '</em>', '\n']:
                        txt = txt.replace(r, '')
                    tmp = tmp + txt
                title = tmp.strip()
            else:
                title = ""

            if cite.__len__() > 0:
                cite = base_url + cite[0]
            else:
                cite = ""

            if text.__len__() > 0:
                text = text[0]
            else:
                text = ""

            if cite != "":
                if not cite.__contains__("facebook") and not cite.__contains__("youtube"):

                    text = Cleaner.clean_reserved_xml(Cleaner(), text)
                    text = Cleaner.remove_accent(Cleaner(), text)
                    title = Cleaner.clean_reserved_xml(Cleaner(), title)
                    title = Cleaner.remove_accent(Cleaner(), title)


                    if FeatureFilter.is_lang(text) == 'en':
                        num_snippet = num_snippet + 1

                        self.log("---------------------------------")
                        self.log("------------TITLE----------------")
                        self.log(title)
                        self.log("------------CITE-----------------")
                        self.log(cite)
                        self.log("------------TEXT-----------------")
                        self.log(text)
                        self.log("------------ID PERSON----------------")
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

        num = response.xpath("//div[@id='result_info']/strong/text()").extract()

        self.log("----------NUM OF ELEMENTS---------")
        self.log(num[0].split(' ')[2])
        num = num[0].split(' ')[2]
        # ToDo Add constant names
        if int(num) < 60 and num_snippet < 10:
            url = response.xpath("//div[@id='result_info']"
                                 "/div[@id='pager']/a/@href").extract()
            self.log("------------URL TO FOLLOW ------------")
            if url.__len__() > 0:
                self.log(base_url + url[0])

                request = Request(base_url+url[0], callback=self.cite_selector)
                request.meta['id_person'] = id_person
                request.meta['search'] = search
                request.meta['attr'] = base_attr
                request.meta['num_snip'] = num_snippet
                yield request
