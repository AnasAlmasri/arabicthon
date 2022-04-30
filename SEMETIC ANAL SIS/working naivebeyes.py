# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 20:56:27 2022

@author: khale
"""

# Load and prepare the dataset
import nltk
from nltk.corpus import movie_reviews
import random
import pandas as pd
from preprocess import preprocess
from nltk.tokenize import word_tokenize

loadeddata=pd.read_csv('poempandas.csv',index_col=0)
loadeddata.reset_index(drop=True, inplace=True)



loadeddata['processed'] = loadeddata['String'].apply(preprocess)

#print((loadeddata.loc[loadeddata['Label'] == 1]).index)
# print(word_tokenize(loadeddata['processed'][1]))
documents = [(list(word_tokenize(loadeddata['processed'][fileid])), Label)
                for Label in [0,1]
                for fileid in (loadeddata.loc[loadeddata['Label'] == 1]).index]

random.shuffle(documents)

all_words = nltk.FreqDist(w  for s in loadeddata['processed'] for w in word_tokenize(s))
word_features = list(all_words)[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features[str(word)] = (word in document_words)
    
    return features
print(word_features)
featuresets=[]
for (d,c) in documents:
    if len(featuresets)<6500:
        featuresets.append((document_features(d), c))

train_set, test_set = featuresets[1000:], featuresets[:1000]

classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(8)
print(classifier.classify(document_features(preprocess("وجهك حلو'"))))
print(classifier.classify(document_features(preprocess(' تبكي لصخرٍ هي العبرَة وَقدْ ولهتْ وَدونهُ منْ جديدِ التُّربِ استارُ'))))
# # 