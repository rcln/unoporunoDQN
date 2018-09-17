import usm as u
import sys

import json

# Index 0 - 4517

# with open('_all_the_queries_final.json') as json_data:
#     d = json.load(json_data)
with open('queries_file.json') as json_data:
    d = json.load(json_data)


keys = list(map(int, list(d.keys())))
keys.sort()

# i = 0
# for e in keys:
#     print(i,e)
#     i+=1

#4514
start = sys.argv[1]
end = int(sys.argv[2])

while end >= len(keys):
    end = end-1

testkeys = keys[int(start):int(end)]
# print("These are the ids of the victims:\n"+str(testkeys))
# print(len(testkeys)) # 4518 values

for key in testkeys:
    k = str(key)
    for snippet in d[k]:
        u.get_snippets(k, [snippet, d[k][-1]])
        # print(key, snippet)

u.start_all()

u.stop_all()
