#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os, glob, json

__author__ = "Josué Fabricio Urbina González && Carl Theodoro Posthuma Solis"

# todo the closing files creates more than one '}' if repeated
# todo filter and only store the english
# todo create MEGAUPLOAD file...?

process = CrawlerProcess(get_project_settings())


def get_snippets(id, query):

    source = [id, query, "1"]

    process.crawl("googlespider", source=source)
    process.crawl("bingspider", source=source)
    process.crawl("duckspider", source=source)
    process.crawl("citespider", source=source)


def start_all():
    process.start()


def stop_all():
    process.join()
    # close_files()


def close_files():
    with open('all_the_queries_final.json') as json_data:
        d = json.load(json_data)

    keys = list(map(int, list(d.keys())))
    keys.sort()
    for i in d.keys():
        tpath = "/train_db/" + str(i) + "/*.json"
        files = glob.glob(os.getcwd() + tpath)
        for file in files:
            with open(file, "a") as f:
                f.write("}")

