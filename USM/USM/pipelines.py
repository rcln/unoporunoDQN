# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
import glob
import logging

__author__ = "Josué Fabricio Urbina González && Carl Theodoro Posthuma Solis"


class UsmPipeline(object):

    data_map = {}

    def process_item(self, item, spider):

        person_id = str(item['id_person'])
        query = str(item['search'])

        data_to_dump = {"id_person": str(item['id_person']),
                        "search": str(item['search']),
                        "engine_search": str(item['engine_search']),
                        "number_snippet": str(item['number_snippet']),
                        "title": str(item['title']),
                        "cite": str(item['cite']),
                        "text": str(item['text'])
                        }
        path = "train_db/" + person_id + "/" + query.strip().replace(" ", "_") + ".json"

        if os.path.isfile(path):

            try:
                num = self.data_map[str(item['search'])]
                num = num + 1
                self.data_map[str(item['search'])] = num

                cad = ",\""+str(num)+"\": "+json.dumps(data_to_dump, indent=4)
                file = open(path, "a")
                file.write(cad)
                file.close()
            except:
                with open("error_key_error_google.html", "w") as log_file:
                    log_file.write(str(self.data_map) + "\n\n\n" + str(item))
        else:
            self.data_map[str(item['search'])] = 0
            cad = "{ \"0\": "+json.dumps(data_to_dump, indent=4)
            file = open(path, "w")
            file.write(cad)
            file.close()

        return item
