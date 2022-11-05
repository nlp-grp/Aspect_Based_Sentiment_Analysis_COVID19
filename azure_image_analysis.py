import requests
# If you are using a Jupyter Notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
import json
import os
import sys
from PIL import Image
from io import BytesIO

c=0
j=0

users=set()
for_classifier={}

os.environ['COMPUTER_VISION_ENDPOINT']='' #add endpoint
os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']='' #add subscriptio key

# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

analyze_url = endpoint + "vision/v3.1/analyze"


with open('path1','rb') as f, open('/Users/Meghna/Desktop/test_data_potraits.json', 'a') as u : #path1 contains image URLs and path2 contains image URLs of people's faces as identified with >= 50% confidence.
    for line in f:
        line = json.loads(line)
        uid = line['user_id']
        url=str(line['image_url']).split('normal')
        final_url=url[0]+'200x200'+url[1]
        remote_image_url = final_url

        if uid in users:
            j = j + 1
            continue
        users.add(uid)
        c = c + 1

        try:

            # Set image_url to the URL of an image that you want to analyze.
            image_url = remote_image_url

            headers = {'Ocp-Apim-Subscription-Key': subscription_key}
            params = {'visualFeatures': 'Categories,Description,Color'}
            data = {'url': image_url}
            response = requests.post(analyze_url, headers=headers,
                                     params=params, json=data)
            response.raise_for_status()

            # The 'analysis' object contains various fields that describe the image. The most
            # relevant caption for the image is obtained from the 'description' property.
            analysis = response.json()
            for k in analysis["categories"]:
                if k['name']:
                    if (k['name']=='people_portrait' or k['name']=='person') and k['score']>=0.5:
                        # print(k['name'])
                        # print(k['score'])
                        # print(image_url)
                        for_classifier['user_id'] = uid
                        for_classifier['name'] = k['name']
                        for_classifier['score'] = k['score']
                        for_classifier['image_url'] = image_url
                        json.dump(for_classifier,u)
                        u.write('\n')
                        for_classifier.clear()
                        print(c)

        except:
            continue


print("here are duplicates ",j)
