#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest

__author__ = "Josué Fabricio Urbina González && Carl Theodoro Posthuma Solis"


class ResearchGate(scrapy.Spider):
    name = "research_gate"
    start_urls = ["https://www.researchgate.net/"]
    browser = 5
    STATUS_OK = 200

    def parse(self, response):
        search_text = "Carl Posthuma"
        request = FormRequest.from_response(response,
                                            formdata={'q': search_text},
                                            callback=self.google_selector)
        self.log(request.url)

        import pdb; pdb.set_trace()


