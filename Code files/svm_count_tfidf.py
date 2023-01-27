import pandas as pd
import re
import string
import numpy as np
import nltk
import json
import glob
import gzip
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
from nltk.util import ngrams
from scipy.sparse import hstack
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from scipy import sparse
import os
import pickle

covid_files_path = covid_data_tweets

covid_train_data = []
noncovid_train_data = []
covid_train_labels = []
noncovid_train_labels = []


try:
    with open(covid_files_path,'r') as fin:
        for line in fin:
            tweet = json.loads(line)
            covid_train_data.append(tweet['text'])
            covid_train_labels.append(1)
except:
    print("Faulty file ")
            
noncovid_files_path = r'noncovid_data_path'
noncovid_files = glob.glob(noncovid_files_path)
num_noncovid_tweets = 0

for i in range(len(noncovid_files)):
    print("opening file", noncovid_files[i])
    try:
        with gzip.open(noncovid_files[i],'r') as fin:
            for line in fin:
                if num_noncovid_tweets < 27068:
                    tweet = json.loads(line)
                    noncovid_train_data.append(tweet['text'])
                    noncovid_train_labels.append(0)
                    num_noncovid_tweets += 1

    except:
        print("Faulty file ", noncovid_files[i])


print(len(covid_train_labels))
print(len(noncovid_train_labels))


train_data = covid_train_data + noncovid_train_data
train_labels = covid_train_labels + noncovid_train_labels


train_corpus,test_corpus,train_labels,test_labels = train_test_split(train_data,train_labels,stratify=train_labels,test_size=0.25)


vectorizer = 'tfidf'   # set 'count' or 'tfidf'
analyzer = 'word'  # set 'word' or 'both' ( word and char)


if vectorizer == 'count':
    if analyzer == 'word':
        vectorizer = CountVectorizer(analyzer='word',ngram_range=(1,1))
    else:
        vectorizer = CountVectorizer(analyzer='word',ngram_range=(1,3))
        char_vectorizer = CountVectorizer(analyzer='char',ngram_range=(2,5))
else:
    if analyzer == 'word':
        vectorizer = TfidfVectorizer(analyzer='word',ngram_range=(1,3))
    else:
        vectorizer = TfidfVectorizer(analyzer='word',ngram_range=(1,3))
        char_vectorizer = TfidfVectorizer(analyzer='char',ngram_range=(2,5))
        
        
def get_training_data_and_labels(train_corpus, train_labels):    
    if analyzer == 'word':
        ngram_vectorized_data = vectorizer.fit_transform(train_corpus)
        
        return ngram_vectorized_data, train_labels
    else:
        ngram_vectorized_data = vectorizer.fit_transform(train_corpus)
        char_vectorized_data = char_vectorizer.fit_transform(train_corpus)
        l = np.hstack((ngram_vectorized_data.toarray(), char_vectorized_data.toarray()))
        train_vectorized_data = sparse.csr_matrix(l)
        
        return train_vectorized_data, train_labels 


def get_test_data_and_labels(test_corpus, test_labels):   
    if analyzer == 'word':
        test_ngram_vectorized_data = vectorizer.transform(test_corpus)
        
        return test_ngram_vectorized_data, test_labels
    else:
        test_ngram_vectorized_data = vectorizer.transform(test_corpus)
        test_char_vectorized_data = char_vectorizer.transform(test_corpus)
        l2 = np.hstack((test_ngram_vectorized_data.toarray(), test_char_vectorized_data.toarray()))
        test_vectorized_data = sparse.csr_matrix(l2)
        
        return test_vectorized_data,test_labels
    

X_train, y_train =  get_training_data_and_labels(train_corpus, train_labels)
X_test, y_test = get_test_data_and_labels(test_corpus, test_labels)


# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]}, {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]
scores = ['precision', 'recall']


for score in scores:
    
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(
        SVC(), tuned_parameters, scoring='%s_macro' % score
    )
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()

file_path = output_file_path
pickle.dump(clf, open(file_path, 'wb'))






