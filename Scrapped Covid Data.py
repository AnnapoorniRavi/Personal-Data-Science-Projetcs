# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 00:20:28 2020

@author: Sahi
"""

import os
import tweepy as tw

##Twitter Credentials 

consumer_key = '********'
consumer_secret = '********'
access_token = '******-*******'
access_secret = '*******'

## Authorization Handlers 

auth= tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth,wait_on_rate_limit='TRUE') ##unless we have an enterprise account, we can pull only 1500 tweets after which we have a break of 15 mins follwed by wheich we can pull tweets again. 

##Setting Parameters 

search_words = '#coronavirus'
date =  '2020-03-01'

tweets_data = tw.Cursor(api.search, q = search_words, lang = "en", since = date). items(101)

tweets_data ## output : <tweepy.cursor.ItemIterator at 0x12d5ab624c8>

##Tweet Details 

info = [[tweets_data.geo, tweets_data.text, tweets_data.user.screen_name, tweets_data.user.location] for tweets_data in tweets_data]

##Code: 

import pandas as pd
tweet_df = pd.DataFrame(data = info, columns=['geo', 'text', 'user', 'location'])
pd.set_option('max_colwidth', 800)
tweet_df.head(20)   

tweet_df.user.value_counts()
tweet_df.location.value_counts()

##Data Cleaning 

import re

def clean_tweets(text):
    text = re.sub('RT @[\w]*:',"", text)
    text = re.sub('@[\w]*',"", text)
    text = re.sub('#[\w]*',"", text)
    text = re.sub(':[\w]*',"", text)
    text = re.sub('https?://[A-Za-z0-9./]*',"", text)
    text = re.sub('\n',"", text)
    return text

tweet_df['text'] = tweet_df['text'].apply(lambda x: clean_tweets(x))
tweet_df.head(20)

tweet_df.to_csv('tweets.csv')

import spacy
import en_core_web_sm
nlp = en_core_web_sm.load() #nlp is spacy object 
    
tweet_df['text'].apply(lambda x: [print('\tText : {}, Entity : {}'.format(ent.text, ent.label_)) if (not ent.text.startswith('#')) else "" for ent in nlp(x).ents])
tweet_df['entities'] = tweet_df['text'].apply(lambda x:[(ent.text, ent.label_) if (not ent.text.startswith('#')) else "" for ent in nlp(x).ents])
tweet_df.head(20)

##Sentiment Analysis 

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
tweet_df['sentiment'] = tweet_df['text'].apply(lambda x: sid.polarity_scores(x))
tweet_df.head(10)

