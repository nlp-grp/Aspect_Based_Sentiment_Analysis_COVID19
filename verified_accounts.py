import gzip
import glob
import json


path='' #add path
files=glob.glob(path)

users = set()
verified_accounts = {}
c = 0 # Reference for unique users
j = 0 # Reference for duplicate users

for i in range(len(files)):
    try:
        with gzip.open(files[i], 'rb') as f, open('path2', 'a') as u: #add path
            m=0
            for line in f:
                data = json.loads(line)
                try:
                    uid = data['user']['id_str']
                except:
                    continue

                if uid in users:
                    j = j + 1
                    continue

                users.add(uid)
                c = c + 1

                if data['user']['verified']==True:
                    m+=1
                    verified_accounts['user_id'] = uid
                    verified_accounts['user_name'] = data['user']['name']
                    verified_accounts['image_url'] = data['user']['verified']
                    json.dump(verified_accounts,u)
                    u.write('\n')
                    verified_accounts.clear()
                    print(c)
    except:
        print("Faulty file ", files[i]) #some files are faulty in the retrieved dataset and do not open

print("here are duplicates ",j)
print("m value is ",m)
