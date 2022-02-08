#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system('pip install tweepy')
get_ipython().system('pip install textblob')
get_ipython().system('pip install pycountry')
get_ipython().system('pip install wordcloud')
get_ipython().system('pip install langdetect')


# In[3]:


import tweepy
consumer_key = "RvasjCNwOlppQgi2tJc8rw0yw"
consumer_secret = "5PFHhDY7JrSJQAhLoD2IEnBw4GubmMuCpbibfSgCTbi9yUfZVW"
access_token = "1368915789718298624-IDDJLdadRjhWbv3D4NtsRzZMLMoMCb"
access_token_secret = "7KxmJ1D9FcZjFyeggn3dBkkSsDqKmkcUO6kxfZjG5Wuur"


# In[4]:


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)


# In[5]:


public_tweets = api.home_timeline()
# foreach through all tweets pulled
for tweet in public_tweets:
   # printing the text stored inside the tweet object
   print(tweet.text)
    
print(public_tweets)


# api = tweepy.API(auth)
# 
# # The Twitter user who we want to get tweets from
# name = "nytimes"
# # Number of tweets to pull
# tweetCount = 20
# 
# # Calling the user_timeline function with our parameters
# results = api.user_timeline(id=name, count=tweetCount)
# 
# # foreach through all tweets pulled
# for tweet in results:
#    # printing the text stored inside the tweet object
#    print(tweet.text)
#     
# print(results)

# In[6]:


query="bete"
language='id'

results=api.search(q=query, lang=language)

for tweet in results:
    print(tweet.user.screen_name,"Tweeted:",tweet.text)


# In[54]:


query="sebel"
language='id'

results=api.search(q=query, lang=language)

for tweet in results:
    print(tweet.user.screen_name,"Tweeted:",tweet.text)


# In[7]:


query="bucin"
language='id'

results=api.search(q=query, lang=language)

for tweet in results:
    print(tweet.user.screen_name,"Tweeted:",tweet.text)


# In[8]:


from textblob import TextBlob
import sys
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import nltk
import pycountry
import re
import string

from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from langdetect import detect
from nltk.stem import SnowballStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer


# In[11]:


def percentage(part,whole):
 return 100 * float(part)/float(whole)

keyword = input('Please enter keyword or hashtag to search: ')
noOfTweet = int(input ('Please enter how many tweets to analyze: '))
tweets = tweepy.Cursor(api.search, q=keyword).items(noOfTweet)
positive = 0
negative = 0
neutral = 0
polarity = 0
tweet_list = []
neutral_list = []
negative_list = []
positive_list = []

for tweet in tweets:
 
 #print(tweet.text)
 tweet_list.append(tweet.text)
 analysis = TextBlob(tweet.text)
 score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
 neg = score['neg']
 neu = score['neu']
 pos = score['pos']
 comp = score['compound']
 polarity += analysis.sentiment.polarity
 
 if neg > pos:
     negative_list.append(tweet.text)
     negative += 1

 elif pos > neg:
    positive_list.append(tweet.text)
    positive += 1
 
 elif pos == neg:
     neutral_list.append(tweet.text)
     neutral += 1

positive = percentage(positive, noOfTweet)
negative = percentage(negative, noOfTweet)
neutral = percentage(neutral, noOfTweet)
polarity = percentage(polarity, noOfTweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')


# In[12]:


tweet_list = pd.DataFrame(tweet_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
print('total number: ',len(tweet_list))
print('positive number: ',len(positive_list))
print('negative number: ', len(negative_list))
print('neutral number: ',len(neutral_list))


# In[30]:


print(tweet_list)


# In[13]:


tweet_list.drop_duplicates(inplace = True)


# In[15]:


tw_list = pd.DataFrame(tweet_list)
tw_list['text'] = tw_list[0]
#Removing RT, Punctuation etc
remove_rt = lambda x: re.sub('RT @\w+: ',' ',x)
rt = lambda x: re.sub('(@[A-Za-z0–9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)',' ',x)
tw_list['text'] = tw_list.text.map(remove_rt).map(rt)
tw_list['text'] = tw_list.text.str.lower()
tw_list.head(25)


# In[16]:


tw_list[['polarity', 'subjectivity']] = tw_list['text'].apply(lambda Text: pd.Series(TextBlob(Text).sentiment))
for index, row in tw_list['text'].iteritems():
 score = SentimentIntensityAnalyzer().polarity_scores(row)
 neg = score['neg']
 neu = score['neu']
 pos = score['pos']
 comp = score['compound']
 if neg > pos:
     tw_list.loc[index, 'sentiment'] = 'negative'
 elif pos > neg:
     tw_list.loc[index, 'sentiment'] = 'positive'
 else:
     tw_list.loc[index, 'sentiment'] = 'neutral'
     tw_list.loc[index, 'neg'] = neg
     tw_list.loc[index, 'neu'] = neu
     tw_list.loc[index, 'pos'] = pos
     tw_list.loc[index, 'compound'] = comp

print(tw_list.head(25))


# In[17]:


tw_list_negative = tw_list[tw_list['sentiment']=='negative']
tw_list_positive = tw_list[tw_list['sentiment']=='positive']
tw_list_neutral = tw_list[tw_list['sentiment']=='neutral']


# In[18]:


def count_values_in_column(data,feature):
 total=data.loc[:,feature].value_counts(dropna=False)
 percentage=round(data.loc[:,feature].value_counts(dropna=False,normalize=True)*100,2)
 return pd.concat([total,percentage],axis=1,keys=['Total','Percentage'])
#Count_values for sentiment
count_values_in_column(tw_list,'sentiment')


# In[ ]:





# In[ ]:




