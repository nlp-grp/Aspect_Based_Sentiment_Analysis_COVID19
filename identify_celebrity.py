from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

users = set()
celebrities = {}
c = 0 # Reference for unique users
j = 0 # Reference for duplicate users

subscription_key = "" #azure subscription key
endpoint = "" #add endpoint

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

with open('path1','rb') as f, open('path2', 'a') as u : #path1 to read from and path2 to write into
    for line in f:
        line = json.loads(line)
        uid = line['user_id']
        url=str(line['image_url']).split('normal')
        final_url=url[0]+'400x400'+url[1]
        remote_image_url_celebs = final_url

        if uid in users:
            j = j + 1
            continue
        users.add(uid)
        c = c + 1

        try:
            # URL of one or more celebrities
            #remote_image_url_celebs = "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-sample-data-files/master/ComputerVision/Images/faces.jpg"
            # Call API with content type (celebrities) and URL
            detect_domain_results_celebs_remote = computervision_client.analyze_image_by_domain("celebrities", remote_image_url_celebs)

            # Print detection results with name
            #print("Celebrities in the remote image:")
            if len(detect_domain_results_celebs_remote.result["celebrities"]) == 0:
                #print("No celebrities detected.")
                continue
            else:
                for celeb in detect_domain_results_celebs_remote.result["celebrities"]:
                    #print(line["user_id"], " ", celeb["name"])
                    celebrities['user_id'] = uid
                    celebrities['celeb_name'] = celeb["name"]
                    json.dump(celebrities,u)
                    u.write('\n')
                    celebrities.clear()
                    print(c)
        except:
            continue
print("here are duplicates ",j)
