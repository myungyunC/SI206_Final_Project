from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
import json

totalResults = 10

api_key = 'f3761bb4e572493c9f7e9f2d3e9afe57'
url = "http://newsapi.org/v2/top-headlines"
params = {'apiKey': api_key, 'country': 'us', 'totalResults':totalResults}

lst = []
response = requests.get(url, params)

for article in response.json()['articles']:
    lst.append(article['description'])

words = (' ').join(lst)

stopwords = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
wordcount = {}

for word in words.lower().split():
    word = word.replace(".","")
    word = word.replace(",","")
    word = word.replace(":","")
    word = word.replace("\"","")
    word = word.replace("!","")
    word = word.replace("â€œ","")
    word = word.replace("â€˜","")
    word = word.replace("*","")
    word = word.replace('"',"")
    word = word.replace("…","")
    word = word.replace("'","")
    word = word.replace("’","")
    word = word.replace("/","")
    word = word.replace("(","")
    word = word.replace(")","")
    if word not in stopwords:
        wordcount[word] = wordcount.get(word, 0) + 1

keywords = {}

for tup in sorted(wordcount.items(), key=lambda kv: kv[1], reverse=True)[:totalResults]:
    keywords[tup[0]] = tup[1]

print(keywords)