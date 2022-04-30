# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 17:01:10 2022

@author: khale
"""

import string
import re
from nltk.corpus import stopwords
import nltk
from nltk.stem.isri import ISRIStemmer
from nltk.tokenize import word_tokenize
# libraries for data split and feature extraction


# first we define a list of arabic and english punctiations that we want to get rid of in our text

punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ''' + string.punctuation

# Arabic stop words with nltk
stop_words = stopwords.words("arabic")

arabic_diacritics = re.compile("""
                             ّ    | # Shadda
                             َ    | # Fatha
                             ً    | # Tanwin Fath
                             ُ    | # Damma
                             ٌ    | # Tanwin Damm
                             ِ    | # Kasra
                             ٍ    | # Tanwin Kasr
                             ْ    | # Sukun
                             ـ     # Tatwil/Kashida
                         """, re.VERBOSE)
stemmer = ISRIStemmer()
def preprocess(text):
    
    '''
    text is an arabic string input
    
    the preprocessed text is returned
    '''
    
  
    
    #remove punctuations
    translator = str.maketrans('', '', punctuations)
    text = text.translate(translator)
    
    # remove Tashkeel
    text = re.sub(arabic_diacritics, '', text)
    
    #remove longation
    text = re.sub("[إأآا]", "ا", text)
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("گ", "ك", text)
    
    text = ' '.join(stemmer.stem(word) for word in text.split() if stemmer.stem(word) not in stop_words)
    # text = word_tokenize(text)
    # text = ' '.join(text) 
    text = word_tokenize(text)

    
    text = ' '.join(text) 

    return text