import random

__author__ = 'pegah'

import json
import queue


QUERY_TYPES = ["", "PHD", "doctorate", "institute", "master", "undergraduate", "university"]


class queires_to_queue:
    #here we save generates queiries in ../DATA/entities_db/1390 to 7 list of queues

    def __init__(self, person_id):
        self.person_id = person_id
        self.originalEntities = {}


    def filter_queues_save_indexes(self):
        """
        this functions gets all queries with extracted entities, remove empty queues and save the unempty entities in
        a queue to be used i game_unopruno code
        :return:
        """
        #que_type = ""

        queues_indexes =[]
        index = 0

        for que_type in QUERY_TYPES:

            q = queue.Queue()

            with open('../DATA/entities_db/'+ str(self.person_id) +'/queue_' + que_type +'.json') as data:
                d = json.load(data)

            if index == 0:
                self.originalEntities = d["original_entities"]

            queques = d["queue"]
            list_q = []

            for i in queques.keys():
                if queques[i] != {'RN': {'entity': [], 'confidenceScore': []}, 'U': {'entity': [],'confidenceScore': []}, 'Y': {'entity': [], 'confidenceScore': []}}:
                    list_q.append(queques[i])

            random.shuffle(list_q)
            for i in list_q:
                q.put(i)

            queues_indexes.append(q)

            index += 1

        return queues_indexes


#test
t = queires_to_queue("1390")
res = t.filter_queues_save_indexes()

#
# for ele in res:
#     while(not ele.empty()):
#         print(ele.get())
#     print('*******')