get_ipython().system('pip install requests-oauthlib==1.3.0')
get_ipython().system('pip install requests')
get_ipython().system('pip install requests-oauthlib')

import requests
import os
import json
import datetime
import itertools
import gzip
os.environ['BEARER_TOKEN'] = 'ADD BEARER TOKEN HERE'


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/all"


# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields


query_params = {'query': '(Coronavirus OR Corona OR CDC OR Ncov OR Wuhan OR outbreak OR China OR Koronavirus OR Wuhancoronavirus OR Wuhanlockdown OR N95 OR Kungflu OR Epidemic OR Sinophobia OR covid-19 OR covid OR covid19 OR sars-cov-2 OR COVID–19 OR corona virus OR COVD OR pandemic OR coronapocalypse OR canceleverything OR Coronials OR SocialDistancing OR SocialDistancingNow OR Social Distancing OR panicbuying OR panic buy OR panicbuy OR 14DayQuarantine OR DuringMy14DayQuarantine OR panic shopping OR panic shop OR panicshop OR InMyQuarantineSurvivalKit OR panic-buy OR panic-shop OR coronakindness OR quarantinelife OR chinese virus OR chinesevirus OR stayhomechallenge OR stay home challenge OR sflockdown OR DontBeASpreader OR lockdown OR shelteringinplace OR staysafestayhome OR trumppandemic OR flattenthecurve OR chinavirus OR flatten the curve OR quarantinelife OR PPEshortage OR saferathome OR stayathome OR stayhome OR GetMePPE OR covidiot OR epitwitter OR pandemie OR wear a mask) lang:en -is:retweet place_country:US', 
                'max_results':'500','start_time': '2019-10-01T00:00:01.000Z',
                'end_time': '2019-10-31T23:59:00.000Z'}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main():
    headers = create_headers(bearer_token)
    count = 0
    with gzip.open(path, 'w') as output:
        while count <25000:
            time.sleep(1)
            json_response = connect_to_endpoint(search_url, headers, query_params)
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            print()
            for val in json_response['data']:
                output.write(json.dumps(val).encode('utf8') + b"\n")
            count += json_response["meta"]["result_count"]
            print(count)
            print(json_response['meta'])
            query_params["next_token"] = json_response["meta"]["next_token"]

if __name__ == "__main__":
    main()


from twarc.client2 import Twarc2
from twarc.expansions import flatten

# Your bearer token here
t = Twarc2(bearer_token='ADD BEARER TOKEN HERE')

# Start and end times must be in UTC
start_time = datetime.datetime(2020, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)
end_time = datetime.datetime(2020, 1, 31, 0, 0, 0, 0, datetime.timezone.utc)

# search_results is a generator, max_results is max tweets per page, 500 max for full archive search.
search_results = t.search_all(query="covid lang:en -is:retweet", start_time=start_time, end_time=end_time, max_results=500)


# this will get all pages
for page in search_results:
    # flatten applies to a page of results, 
    # and modifies the original response to append extra info
    expanded = flatten(page) 
    #for tweet in expanded['data']:
    for tweet in expanded['data']:
        print(tweet)

