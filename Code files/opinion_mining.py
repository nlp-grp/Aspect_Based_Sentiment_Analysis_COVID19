import gzip
import glob
import json

path = path_to_filtered_tweets_posted_by_african_american

key = ""
endpoint = "https://textanalyticsresouce.cognitiveservices.azure.com/"

files=glob.glob(path)

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

def sentiment_analysis_with_opinion_mining_example(client):

    for i in range(len(files)):
        print("opening file", files[i])
        file_name=files[i].split("/")[-1]
        try:
            with gzip.open(files[i],'r') as fin:
                for line in fin:
                    tweet=json.loads(line)
                    tweet_text=[tweet['text']]
                    tweet_date='_'.join(tweet['created_at'].split()[1:3])
                    tweet_id=tweet['id']
                    file_is='path'+tweet_date+'.json.gz'

                    result = client.analyze_sentiment(tweet_text, show_opinion_mining=True)
                    doc_result = [doc for doc in result if not doc.is_error]
                    positive_reviews = [doc for doc in doc_result if doc.sentiment == "positive"]
                    negative_reviews = [doc for doc in doc_result if doc.sentiment == "negative"]

                    positive_mined_opinions = []
                    mixed_mined_opinions = []
                    negative_mined_opinions = []
                    
                    with gzip.open(file_is,'ab') as fout:
                        fout.write(json.dumps(tweet_date).encode('utf-8')+b"\n")
                        fout.write(json.dumps(tweet_id).encode('utf-8')+b"\n")

                        for document in doc_result:
                            
                            fout.write(json.dumps("Document Sentiment: {}".format(document.sentiment),indent=4).encode('utf-8')+b"\n")
                            fout.write(json.dumps("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f}".format(
                                document.confidence_scores.positive,
                                document.confidence_scores.neutral,
                                document.confidence_scores.negative,
                            ),indent=4).encode('utf-8'))
                            for sentence in document.sentences:
                                fout.write(json.dumps("Sentence: {}".format(sentence.text),indent=4).encode('utf-8')+b"\n")
                                fout.write(json.dumps("Sentence sentiment: {}".format(sentence.sentiment),indent=4).encode('utf-8')+b"\n")
                                fout.write(json.dumps("Sentence score: Positive={0:.2f}..Neutral={1:.2f}..Negative={2:.2f}".format(
                                    sentence.confidence_scores.positive,
                                    sentence.confidence_scores.neutral,
                                    sentence.confidence_scores.negative,
                                ),indent=4).encode('utf-8'))
                                for mined_opinion in sentence.mined_opinions:
                                    aspect = mined_opinion.aspect
                                    fout.write(json.dumps("......'{}' aspect '{}'".format(aspect.sentiment, aspect.text),indent=4).encode('utf-8')+b"\n")
                                    fout.write(json.dumps("......Aspect score:......Positive={0:.2f}......Negative={1:.2f}".format(
                                        aspect.confidence_scores.positive,
                                        aspect.confidence_scores.negative,
                                    ),indent=4).encode('utf-8'))
                                    for opinion in mined_opinion.opinions:
                                        fout.write(json.dumps("......'{}' opinion '{}'".format(opinion.sentiment, opinion.text),indent=4).encode('utf-8')+b"\n")
                                        fout.write(json.dumps("......Opinion score:......Positive={0:.2f}......Negative={1:.2f}".format(
                                            opinion.confidence_scores.positive,
                                            opinion.confidence_scores.negative,
                                        ),indent=4).encode('utf-8'))
#                                print("\n")
#                            print("\n")
        except:
            print("Faulty file ", files[i])
sentiment_analysis_with_opinion_mining_example(client)
