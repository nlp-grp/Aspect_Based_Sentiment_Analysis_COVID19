import gzip
import glob
import json

path = path_to_covid_twitter_data

files=glob.glob(path)
hashtag_list=[]

doubtful=["rslashblacktears","blackholes", "itsblackleatherforareason", "truthbeblack", "allblackeverything", "blacklockdownlivesmatter"]


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
						if got_hashtag in doubtful:
							print(tweet['text'])
							break
					break
	except:
		print("Faulty file ", files[i])
