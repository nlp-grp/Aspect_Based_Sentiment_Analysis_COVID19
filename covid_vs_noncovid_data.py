
from google.colab import drive
drive.mount('/content/gdrive')

import pandas as pd
import re
import string
import numpy as np
import nltk
import json
import glob
import gzip
import os
import random

covid_files_path = '' #add path
covid_files = glob.glob(covid_files_path)

train_count = 0
train_data = []
train_labels = []

print(covid_files)


tweet_ids = set()
counter = 0
with open('path', 'a') as l: #add your own path
  for i in range(len(covid_files)):
      print("opening file", covid_files[i])
      try:
          with gzip.open(covid_files[i],'rb',) as fin:
            j = 0
            tweets = fin.read().splitlines()
            while j<= 100:
              covid_tweets_train = {}
              random_tweet = random.choice(tweets)
              tweet = json.loads(random_tweet)
              try:
                # Filtering Retweets  
                while (tweet['retweeted_status']): 
                  random_tweet = random.choice(tweets)
                  tweet = json.loads(random_tweet)
                
              except:
                #Filtering replies, language, and duplicates
                if tweet['in_reply_to_user_id'] == None and tweet['lang'] == 'en' and tweet['id'] not in tweet_ids:
                  j += 1             
                  tweet_ids.add(tweet['id'])
                  covid_tweets_train['id'] = tweet['id']

                  if tweet['truncated'] == True:
                    covid_tweets_train['text'] = tweet['extended_tweet']['full_text']
                  else:
                    covid_tweets_train['text'] = tweet['text']

                  json.dump(covid_tweets_train,l)
                  l.write('\n')

      except:
          print("Faulty file ", covid_files[i])
          counter += 1

print(counter)

count = 0
with open('path', 'r') as l: #add path
  for line in l:
    count += 1

print(count)
