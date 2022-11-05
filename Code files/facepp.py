from facepplib import FacePP
import json

facepp = FacePP(api_key='', api_secret='')
#image = facepp.image.get(image_url='http://pbs.twimg.com/profile_images/1322616772495839232/L9Lkn4DO_400x400.jpg',return_attributes=['ethnicity','gender'])


with open('/Users/Meghna/Desktop/test_images_no_celeb.json','rb') as f:
    for line in f:
        line = json.loads(line)
        uid = line['user_id']
        url=str(line['image_url']).split('normal')
        final_url=url[0]+'400x400'+url[1]
        remote_image_url = final_url

        # if uid in users:
        #     j = j + 1
        #     continue
        # users.add(uid)
        # c = c + 1

        try:

            # Set image_url to the URL of an image that you want to analyze.
            image_url = remote_image_url

            image = facepp.image.get(image_url=image_url,return_attributes=['ethnicity','gender'])

            #print(image.image_id)
            if len(image.faces)>0 and image.faces[0].ethnicity['value']!='':
                print(image.faces[0].ethnicity)

        except:
            continue
