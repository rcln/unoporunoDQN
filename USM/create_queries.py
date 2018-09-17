import json
import os

raw = json.load(open('../DATA/train.json', 'r'))
data_dict = raw['_default']

keys = list(map(int, list(data_dict.keys())))
keys.sort()

tags = ['PHD', 'doctorate', 'master', 'undergraduate', 'university', 'institute', '']

dict_queries = {}

for k in map(str, keys):
    name = data_dict[k]['name'].split(' ')
    for i in range(2):
        tmp = name.pop(0)
        name.append(tmp)
    list_queries = []
    for t in tags:
        query = ' '.join(name) + ' ' + t
        list_queries.append(query)
    dict_queries[k] = list_queries

with open('queries_file.json', 'w') as f:
    json.dump(dict_queries, f, indent=4)
