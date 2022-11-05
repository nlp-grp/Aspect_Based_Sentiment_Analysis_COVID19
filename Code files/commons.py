import json

celebs=set()
verified=set()
celebs_verified=set()
urls = {}
c=0

with open('celebrities.json',"r") as f, open('verified_accounts.json',"r") as f2:
    for line in f:
        try:
            tweet=json.loads(line)
            celebs.add(tweet['user_id'])
        except:
            continue

    for line2 in f2:
        try:
            tweet2=json.loads(line2)
            verified.add(tweet2['user_id'])
        except:
            continue

print(len(celebs))
print(len(verified))
celebs_verified=celebs.intersection(verified)
print(len(celebs_verified))
celebs_not_verified=celebs.difference(celebs_verified)
print(len(celebs_not_verified))

with open('twitter_test_images.json',"r") as f3, open('test_images_no_celeb.json',"a") as u:
        for line in f3:
            try:
                tweet3=json.loads(line)
                id=tweet3['user_id']
                url=tweet3['image_url']
                if id not in celebs_not_verified:
                    urls['user_id']=id
                    urls['image_url']=url
                    json.dump(urls,u)
                    u.write('\n')
                    urls.clear()
                    c+=1

            except:
                continue

print("filtered links ",c)
