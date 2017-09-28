import os

folders = []

for folder in folders:
    for json in os.listdir(folder):
         with open(os.getcwd()+"/"+str(folder)+"/"+json,"a") as f:
            f.write("}")
