import json
c=0
d=0
with open('covid19-1606748971946.json',"r") as f:
    for line in f:

        tweet=json.loads(line)

        c+=1

print(c)
