# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import logging


class UsmPipeline(object):
    mapSpider = {}
    all_the_data = {}
    filepath = os.getcwd()
    i = 0
    person_id = "fuck"
    query = "fuck"

    # def __init__(self):
    #     # raise DropItem("Duplicate item found: %s" % item)
    #     self.file = open('test.csv', 'w')
    #     self.file.write("id_person,search,engine,num_snippet,title,url,text\n")

    def open_spider(self, spider):
        self.mapSpider[spider.name] = False

    def close_spider(self, spider):
        self.mapSpider[spider.name] = True
        close = True
        for bol in self.mapSpider.values():
            if not bol:
                close = False
        if close:
            self.file = open("train_db/7/test_for_" +self.person_id+"_with_query_"+self.query.replace(" ","_") +  ".json", "w")
            self.file.write(json.dumps(self.all_the_data, indent=4, sort_keys=True))
            logging.debug("File made")
            self.file.close()

    def process_item(self, item, spider):
        self.person_id = str(item['id_person'])
        self.query = str(item['search'])

        data_to_dump = {"id_person": str(item['id_person']),
                        "search": str(item['search']),
                        "engine_search": str(item['engine_search']),
                        "number_snippet": str(item['number_snippet']),
                        "title": str(item['title']),
                        "cite": str(item['cite']),
                        "text": str(item['text'])
                        }

        # text_w = str(item['id_person']) + ',' + self.process_text(item['search']) + ',' \
        #          + str(item['engine_search']) + ',' \
        #          + str(item['number_snippet']) + ',' + \
        #          self.process_text(item['title']) + "," + \
        #          self.process_text(item['cite']) + "," + \
        #          self.process_text(item['text']) + "\n"

        self.all_the_data[self.i] = data_to_dump
        self.i += 1
        return item

    def process_text(self, text):
        text = text.replace('\n', '')
        text = text.replace('"', '')

        if text.find(',') != -1:
            text = "\"" + text + "\""

        return text
