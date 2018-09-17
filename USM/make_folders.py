import os
import json


print(os.getcwd())

# with open('all_the_queries_final.json') as json_data:
#     d = json.load(json_data)
#

with open('queries_file.json') as json_data:
    d = json.load(json_data)


keys = list(map(int, list(d.keys())))
keys.sort()

for i in d.keys():
    os.makedirs(os.getcwd() +"/train_db/" + str(i), 0o755)