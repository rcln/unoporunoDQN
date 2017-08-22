import usm as u
import json

#TODO
"""
 ability to run multiple times, Done, but google is a sneaky little bitch, up to josue
 only english, ask josue
 only 20 snippets, ask josue
 make into folders, should i just build all of them on the go? or make sum functions that build them? probably the latter
"""

with open('all_the_queries_final.json') as json_data:
    d = json.load(json_data)


testkeys = list(d.keys()) [0:3]
print("These are the ids of the victums:\n"+str(testkeys))

for key in testkeys:
    for snippet in d[key]:
        u.get_snippets(str(key),str(snippet))
        #print(str(key),snippet)

# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA PHD")
# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA doctorate")
# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA master")
# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA undergraduate")
# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA university")
# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA institute")
# u.get_snippets("7", "MURRIETA FLORES PATRICIA ALEJANDRA ")
#

u.start_all()

u.stop_all()
