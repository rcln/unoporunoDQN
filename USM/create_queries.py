import json
import os

raw = json.load(open('../DATA/train.json', 'r'))
data_dict = raw['_default']

keys = list(map(int, list(data_dict.keys())))
keys.sort()

tags = ['PHD', 'doctorate', 'master', 'undergraduate', 'university', 'institute', '']

dict_queries = {}


def process(name):
    if len(name) > 2:
        prep = ['DE', 'LA', 'LOS', 'DEL']
        if len(set(prep).intersection(set(name))) > 0:
            return ' '.join(name)
        for _ in range(int(len(name))):
            tmp = name.pop(0)
            name.append(tmp)
    return ' '.join(name)


for k in map(str, keys):
    name = data_dict[k]['name']
    name = name.replace('?', 'Ñ').split(' ')
    name = process(name)

    list_queries = []
    for t in tags:
        query = name + ' ' + t
        list_queries.append(query)
    dict_queries[k] = list_queries

with open('queries_file.json', 'w') as f:
    json.dump(dict_queries, f, indent=4)
