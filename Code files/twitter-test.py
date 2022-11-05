import gzip
import glob
import json

path='/Users/meghnachaudhary/Desktop/Twitter_Covid_Data/*.json.gz'

files=glob.glob(path)
hashtags=set()



for i in range(len(files)):
	print("opening file", files[i])
	try:
		with gzip.open(files[i],'r') as fin:
			for line in fin:
				tweet=json.loads(line)
				hashtag_list=tweet['entities']['hashtags'] 
				if hashtag_list!=[] :
					for hashtag in hashtag_list:
						got_hashtag=hashtag['text'].lower() 
						if 'black' in got_hashtag:
							hashtags.add(got_hashtag)
			print(f"Hashtag appended for file {i}")
	except:
		print("Faulty file ", files[i])

hashtags=list(hashtags)

with open('/Users/meghnachaudhary/Desktop/twitter_hashtags.json','w') as f:
	json.dump(hahstags,f,indent=4)	