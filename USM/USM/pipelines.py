# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class UsmPipeline(object):
    mapSpider = {}

    def __init__(self):
        # raise DropItem("Duplicate item found: %s" % item)
        self.file = open('test.csv', 'w')
        self.file.write("id_person,search,engine,num_snippet,title,url,text\n")

    def open_spider(self, spider):
        self.mapSpider[spider.name] = False

    def close_spider(self, spider):
        self.mapSpider[spider.name] = True
        close = True
        for bol in self.mapSpider.values():
            if not bol:
                close = False
        if close:
            self.file.close()

    def process_item(self, item, spider):
        # text_w = str(item['id_person']) + ',' + self.process_text(item['search']) + ',' +
        #     str(item['engine_search']) + ',' + str(item['number_snippet']) + ',' +
        #     self.process_text(item['title']) + "," +
        #     self.process_text(item['cite']) + "," +
        #     self.process_text(item['text']) + "\n"
        # self.file.write(text_w)
        return item

    def process_text(self, text):
        text = text.replace('\n', '')
        text = text.replace('"', '')

        if text.find(',') != -1:
            text = "\"" + text + "\""

        return text
