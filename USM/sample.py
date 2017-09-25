import usm as u
import json

with open('all_the_queries_final.json') as json_data:
    d = json.load(json_data)


keys = list(map(int, list(d.keys())))
keys.sort()

testkeys = keys[0:5]
# print("These are the ids of the victims:\n"+str(testkeys))
# print(len(testkeys)) # 4518 values


for key in testkeys:
    k = str(key)
    for snippet in d[k]:
        u.get_snippets(k, [snippet, d[k][-1]])
        # print(key, snippet)


u.start_all()

u.stop_all()

