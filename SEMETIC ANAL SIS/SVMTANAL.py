# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 13:38:37 2022

@author: khale
"""
import nltk
from nltk import classify
from nltk import NaiveBayesClassifier
from pprint import pprint
from nltk.sentiment import SentimentIntensityAnalyzer
from random import shuffle
from statistics import mean
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
# libraries for data split and feature extraction
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

# library for evaluation
from sklearn import metrics

# libraries for ML algorithms
from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB

# libraries for data plotting
import seaborn as sns
import matplotlib.pyplot as plt 

from preprocess import preprocess
RANDOM_SEED = 100

def get_svm_predictions(X_train, X_val, y_train, y_val, class_names):
  # build model
  clf = svm.SVC() 
  clf.fit(X_train, y_train)

  # Make predictions on test data
  y_pred = clf.predict(X_val)

  # evalution
  accuracy, confusion_matrix = evaluate(y_val, y_pred, class_names)
  print(f'Accuracy: {accuracy}')
  plot_confusion_matrix(confusion_matrix, class_names)

  return clf

def plot_confusion_matrix(matrix, class_names):
    plt.clf()
    plt.imshow(matrix, interpolation='nearest', cmap=plt.cm.Set2_r)
    plt.title('Confusion Matrix')
    plt.ylabel('Predicted')
    plt.xlabel('Actual')
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    s = [['TP','FP'], ['FN', 'TN']]

    for i in range(2):
        for j in range(2):
            plt.text(j,i, str(s[i][j])+" = "+str(matrix[i][j]))
    plt.show()

# method to calculate evaluation results
def evaluate(actuals, predictions, class_names):
  accuracy = metrics.accuracy_score(actuals, predictions)
  confusion_matrix = metrics.confusion_matrix(actuals, predictions, labels=class_names)
  return accuracy, confusion_matrix


loadeddata=pd.read_csv('poempandas.csv',index_col=0)
df=loadeddata    
df['Tokenised_Text'] = loadeddata['String'].apply(preprocess)
df.to_csv('test.csv', encoding='utf-8-sig')

X_train_tokenised_text, X_val_tokenised_text, y_train, y_val = train_test_split(df['Tokenised_Text'], df['Label'], test_size=0.2)
print(f'training data set size: {len(X_train_tokenised_text)}')
print(f'validation data set size: {len(X_val_tokenised_text)}')
print(X_train_tokenised_text[:5])
print(y_train[:5])
class_list = [1, 0]

vectorizer = CountVectorizer()  # default: lowercase=True, ngram_range=(1,1)
vectorizer.fit(X_train_tokenised_text)

# convert train and test text data to numeric vectors
X_train = vectorizer.transform(X_train_tokenised_text)
X_val = vectorizer.transform(X_val_tokenised_text)

m1 = get_svm_predictions(X_train, X_val, y_train, y_val, class_list)
print(m1.predict(preprocess(('وجهك حلو'))))
print(m1.predict(preprocess(' تبكي لصخرٍ هي العبرَة وَقدْ ولهتْ وَدونهُ منْ جديدِ التُّربِ استارُ')))