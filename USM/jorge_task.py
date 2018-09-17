import json
import itertools


keys_1 = ["Biología celular ", "biología molecular ",
        "cultivo celular ", "Bioquímica ", "mexicano ", "mexicana "]

keys_2 = ["postdoc ", "post doc ", "post-doc ", "doctorate ", "doctorado "]

keys_3 = ["Facultad de Ciencias", "Facultad de Medicina", "UNAM", "Universidad Nacional "
                                                                  "Autonoma de México"]

keys_4 = [" Personas", " personal", " ", " students", " egresados", " alumnos"]


def to_string(tup):
    s = ""
    for t in tup:
        s+=t
    return s


keys = list(map(to_string, list(itertools.product(keys_1, keys_2, keys_3, keys_4))))

print(keys)

data = {}

for k in keys:
    data[len(data)] = [k]


json.dump(data, open("jorge_task.json", 'w'))





