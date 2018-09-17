#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest, Request
from scrapy import Selector
from items import UsmItem
from tools.basic_tool import Utils
from tools.filter import FeatureFilter, Cleaner

__author__ = "Josué Fabricio Urbina González && Carl Theodoro Posthuma Solis"


class ResearchGate(scrapy.Spider):
    name = "research_gate"
    start_urls = ["https://www.researchgate.net/"]
    browser = 5
    STATUS_OK = 200

    def parse(self, response):
        return FormRequest.from_response(response, formdata={'email': '', 'pass': ''},
                                  callback=self.after_login)

    def after_login(self, response):
        pass

