#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install requests-oauthlib==1.3.0')


# In[ ]:


get_ipython().system('pip install requests')
get_ipython().system('pip install requests-oauthlib')


# In[ ]:


import requests
import os
import json
import datetime
import itertools
import gzip
os.environ['BEARER_TOKEN'] = 'ADD BEARER TOKEN HERE'


# In[ ]:


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

bearer_token = os.environ.get("BEARER_TOKEN")


# In[ ]:


search_url = "https://api.twitter.com/2/tweets/search/all"


# In[ ]:


# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields


query_params = {'query': '(Coronavirus OR Corona OR CDC OR Ncov OR Wuhan OR outbreak OR China OR Koronavirus OR Wuhancoronavirus OR Wuhanlockdown OR N95 OR Kungflu OR Epidemic OR Sinophobia OR covid-19 OR covid OR covid19 OR sars-cov-2 OR COVID–19 OR corona virus OR COVD OR pandemic OR coronapocalypse OR canceleverything OR Coronials OR SocialDistancing OR SocialDistancingNow OR Social Distancing OR panicbuying OR panic buy OR panicbuy OR 14DayQuarantine OR DuringMy14DayQuarantine OR panic shopping OR panic shop OR panicshop OR InMyQuarantineSurvivalKit OR panic-buy OR panic-shop OR coronakindness OR quarantinelife OR chinese virus OR chinesevirus OR stayhomechallenge OR stay home challenge OR sflockdown OR DontBeASpreader OR lockdown OR shelteringinplace OR staysafestayhome OR trumppandemic OR flattenthecurve OR chinavirus OR flatten the curve OR quarantinelife OR PPEshortage OR saferathome OR stayathome OR stayhome OR GetMePPE OR covidiot OR epitwitter OR pandemie OR wear a mask) lang:en -is:retweet place_country:US', 
                'max_results':'500','start_time': '2020-04-01T00:00:01.000Z',
                'end_time': '2020-04-05T23:59:00.000Z'}
# query_params = {'query': '(Coronavirus OR Corona OR CDC OR Ncov OR Wuhan OR Outbreak OR China OR Koronavirus OR Wuhancoronavirus OR Wuhanlockdown OR N95 OR Kungflu OR Epidemic OR Sinophobia OR Covid-19 OR Covid OR Covid19 OR Sars-cov-2 OR COVID–19 OR COVD OR Pandemic OR Coronapocalypse OR CancelEverything OR Coronials OR SocialDistancing OR Panic buying OR DuringMy14DayQuarantine OR Panic shopping OR InMyQuarantineSurvivalKit OR chinese virus OR stayhomechallenge OR DontBeASpreader OR lockdown OR shelteringinplace OR staysafestayhome OR trumppandemic OR flatten the curve OR PPEshortage OR saferathome OR stayathome OR GetMePPE OR covidiot OR epitwitter OR Pandemie OR antivaccine OR  betweenmeandmydoctor OR vaccine OR cdcfraud OR cdctruth OR covidvaccineispoison OR forcedvaccines OR mybodymychoice OR noforcedflushots OR NoForcedVaccines OR notomandatoryvaccines OR NoVaccine OR saynotovaccines OR unvaccinated OR vaccinationchoice OR vaccineharm OR VaccinesAreNotTheAnswer OR vaxxed OR yeht) lang:en -is:retweet place_country:US', 
#                 'max_results':'500','start_time': '2019-11-01T00:00:01.000Z',
#                 'end_time': '2019-11-30T23:59:00.000Z'}


# In[ ]:


# AND (place_country: US) AND (start_time:2020-01-01 00:00), (end_time:2020-01-31 23:59)
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


# In[ ]:


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


# In[ ]:


def main():
    headers = create_headers(bearer_token)
    count = 0
    #with gzip.open('/Users/Meghna/Desktop/noncovid_tweets_nov.gz', 'wt', encoding='UTF-8') as zipfile:
    with gzip.open('/Users/Meghna/Desktop/noncovid_tweets_oct.gz', 'w') as output:
        while count <5000000:
            time.sleep(2)
            json_response = connect_to_endpoint(search_url, headers, query_params)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            print()
            for val in json_response['data']:
                #json.dump(val, zipfile)
                output.write(json.dumps(val).encode('utf8') + b"\n")
            count += json_response["meta"]["result_count"]
            print(count)
            #print(json_response['meta'])
            query_params["next_token"] = json_response["meta"]["next_token"]


# In[ ]:


if __name__ == "__main__":
    main()


# In[ ]:


# with gzip.open('/Users/Meghna/Desktop/noncovid_tweets.gz', 'rb') as zipfile:
#     for line in zipfile:
#         tweet = json.loads(line)
#         print(tweet['id'])
#         break
               


# In[ ]:


# from searchtweets import ResultStream, gen_request_parameters, load_credentials


# In[ ]:


# search_args = load_credentials(filename="~/.twitter_keys.yaml",
#                  yaml_key="search_tweets_v2",
#                  env_overwrite=False)

# query = gen_request_parameters(query, start_time=start_time, results_per_call=100, expansions='author_id,geo.place_id', tweet_fields='created_at,geo',user_fields='description,location')

# rs = ResultStream(request_parameters=query,
#                     max_results=10000,
#                     max_pages=10000,
#                     max_tweets=10000,
#                     **search_args)


# In[ ]:


from twarc.client2 import Twarc2
from twarc.expansions import flatten

# Your bearer token here
t = Twarc2(bearer_token='ADD BEARER TOKEN HERE')

# Start and end times must be in UTC
start_time = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
end_time = datetime.datetime(2020, 1, 31, 0, 0, 0, 0, datetime.timezone.utc)

# search_results is a generator, max_results is max tweets per page, 500 max for full archive search.
search_results = t.search_all(query="covid lang:en -is:retweet", start_time=start_time, end_time=end_time, max_results=500)

# # Get just 1 page of results instead of iterating over everything in search_results:
# # To get everything use `for page in search_results:`
# for page in itertools.islice(search_results, 1):
#     # Do something with the page of results:
#     # print(page)
#     # or alternatively, "flatten" results returning 1 tweet at a time, with expansions inline:
#     for tweet in flatten(page)['data']:
#         # Do something with the tweet
#         print(tweet)

# this will get all pages
for page in search_results:
    # flatten applies to a page of results, 
    # and modifies the original response to append extra info
    expanded = flatten(page) 
    #for tweet in expanded['data']:
    for tweet in expanded['data']:
        print(tweet)


# In[ ]:




