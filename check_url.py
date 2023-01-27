import requests
import json

def sendRequest(url):
    try:
        page = requests.get(url)

    except Exception as e:
        print("error:", e)
        return False

    # check status code
    if (page.status_code != 200):
        return False

    return page

count=0
with open('path1','rb') as f, open('path2','a') as f1: #path1 read from list of URLs and path2 write the working urls in path 2 json file
    for line in f:
        line = json.loads(line)
        url = str(line['image_url'])
        if sendRequest(url)!=False:
            json.dump(line,f1)
            f1.write('\n')
        else:
            count+=1
print(f"No images for {count} URLs")
