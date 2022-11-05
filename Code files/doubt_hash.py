import gzip
import glob
import json

path='/Users/meghnachaudhary/Desktop/Twitter_Covid_Data/*.json.gz'

files=glob.glob(path)
hashtag_list=[]

doubtful=["rslashblacktears","blackholes", "itsblackleatherforareason", "truthbeblack", "allblackeverything", "blacklockdownlivesmatter"]
#“blackinmarinescienceweek”, “blacktechtwitter”, “goblackknights”, “buyblackowned”, “supportblackbusinesses”, 
#“ianblackfordpropaganda”, “whitegirlsgoneblac”, “quaranteamblackpi”, “blacknbritish”, “blackhistoryflash”, 
#“blackonblack”, “blackdaddy”, “blackhair”, “blackblock”, “blackincarnaby”, “blackeuphoria”, 
#“supportblackownedbusinesses”, “blackopstech”, “buyblack”, “bigblackbullbulls”, “blackmask”, “blackmarkethappiness”, 
#“blacksanta”, “resististhenewblack”  


for i in range(len(files)):
	print("opening file", files[i])
	try:
		with gzip.open(files[i],'r') as fin:
			for line in fin:
				tweet=json.loads(line)
				#print(tweet)
				hashtag_list=tweet['entities']['hashtags'] 
				if hashtag_list!=[] :
					for hashtag in hashtag_list:
						got_hashtag=hashtag['text'].lower() 
						#print(got_hashtag)
						if got_hashtag in doubtful:
							print(tweet['text'])
							break
					break


			#print(f"Hashtag appended for file {i}")
	except:
		print("Faulty file ", files[i])

# hashtags=list(hashtags)

# with open('/Users/meghnachaudhary/Desktop/twitter_doubtful_hashtags.json','w') as f:
# 	json.dump(hahstags,f,indent=4)	