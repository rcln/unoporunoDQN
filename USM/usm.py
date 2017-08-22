#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

__author__ = "Josué Fabricio Urbina González && Carl Theodoro Posthuma Solis, but mostly Urbs"

# todo fix the problems detected, with some of the span and ...


process = CrawlerProcess(get_project_settings())

def get_snippets(id, query):

    source = [id, query, "1"]

    #process.crawl("googlespider", source=source)
    #process.crawl("bingspider", source=source)
    process.crawl("duckspider", source=source)
    # process.crawl("citespider", source=source)

def start_all():
    process.start()

def stop_all():
    process.join()


