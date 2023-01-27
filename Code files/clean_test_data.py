import json
import cv2
import urllib
import numpy as np
from skimage import io

count=0
count_correct=0

users = set()
working_images = {}

with open(url_file_path, 'rb') as u, open(twitter_test_images_path, 'a') as u1:
    for line in u:
        data = json.loads(line)
        try:
            image = io.imread(data["image_url"])
            count_correct+=1
            working_images['user_id'] = data["user_id"]
            working_images['image_url'] = data["image_url"]
            json.dump(working_images,u1)
            u1.write('\n')
            working_images.clear()

        except:
            count+=1
            continue

print("Loaded Images are ",count_correct)
print("Faulty Images are ",count)
