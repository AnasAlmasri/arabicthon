# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 16:54:42 2022

@author: khale
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import string
import re
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix,accuracy_score, classification_report
from preprocess import preprocess
from sklearn.utils import shuffle
loadeddata=pd.read_csv('poempandas.csv',index_col=0)
loadeddata.reset_index(drop=True, inplace=True)



loadeddata['processed'] = loadeddata['String'].apply(preprocess)
loadeddata=shuffle(loadeddata)
print(loadeddata.head(5))

# splitting the data into target and feature
feature = loadeddata.processed
target = loadeddata.Label
# splitting into train and tests
X_train, X_test, Y_train, Y_test = train_test_split(feature, target, test_size =.2)
print(X_train)
# make pipeline
pipe = make_pipeline(TfidfVectorizer(),
                    LogisticRegression(max_iter=1000))
# make param grid
param_grid = {'logisticregression__C': [0.01, 0.1, 1, 10, 100],'logisticregression__solver':['newton-cg', 'lbfgs', 'sag', 'saga']}

# create and fit the model
model = GridSearchCV(pipe, param_grid, cv=5)
model.fit(X_train,Y_train)

# make prediction and print accuracy
prediction = model.predict(X_test)
print(f"Accuracy score is {accuracy_score(Y_test, prediction):.2f}")
print(classification_report(Y_test, prediction))
print(preprocess('وجهك حلو'))
print(model.predict([preprocess("أن نجعل حبنا يفوق الخيال ")]))
print(model.predict([preprocess(' تبكي لصخرٍ هي العبرَة وَقدْ ولهتْ وَدونهُ منْ جديدِ التُّربِ استارُ')]))