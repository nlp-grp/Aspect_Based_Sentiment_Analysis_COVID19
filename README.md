# Code and Data for the paper "On the Use of Aspect-Based Sentiment Analysis of Twitter Data to Explore the Experiences of African Americans During COVID-19"

## This repository includes the code, saved models, and data for replicating the above mentioned study.

Project Active

For more information, please e-mail Meghna Chaudhary at meghna1@usf.edu.

## Dataset Description

This repository contains COVID-19 related tweet IDs from January 2020 to Decemeber 2020. This dataset is useful for Sentiment Analysis and Aspect-Based Sentiment Analysis.

Each of these .json.gz file contains a list of dictionaries. Each dictionary contains the following information:

Tweet ID
Docment Sentiment (tweet sentiment)
Sentence Sentiment (sentiment of a sentence in the tweet with values positive, negative, and neutral)
Sentence positive score
Sentence neutral score
Sentence negative score
The following fields may be present in the tweet sentence.

Target (aspect towards which the sentiment has been expressed)
Target polarity (polarity of the target with values positive, negative, and neutral)
Positive Target Value (model's confidence in label classification in the range [0.0,1.0] with 0.0 being the lowest and 1.0 being the highest)
Negative Target Value (model's confidence in label classification)
Assessment (opinion word)
Assessment Polarity (polarity of the assessment with values positive, negative, and neutral)
Positive Assessment Value (model's confidence in label classification)
Negative Assessment Value (model's confidence in label classification)
Please note: you need to hydrate (download the tweets) for the given tweet IDs.

Note: This dataset is a subset of the dataset provided by:
Chen E, Lerman K, Ferrara E. Tracking Social Media Discourse About the COVID-19 Pandemic: Development of a Public Coronavirus Twitter Data Set. JMIR Public Health Surveill 2020;6(2):e19273. URL: https://publichealth.jmir.org/2020/2/e19273. DOI: 10.2196/19273. 
