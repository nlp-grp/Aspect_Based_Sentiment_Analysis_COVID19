import glob
import json

verified_ids=[]
with open('path1', 'rb') as u: #path1 has the verified accounts json file
    for line1 in u:
        data1 = json.loads(line1)
        verified_ids.append(data1['user_id'])


with open('path2', 'rb') as u1,open('path3', 'a') as u2: #add path2 to read from identifed celebrity json file and path 3 file will contain fake celebrities
    for line in u1:
        data = json.loads(line)
        if data['user_id'] not in verified_ids:
            json.dump(data['user_id'],u2)
            u2.write('\n')
