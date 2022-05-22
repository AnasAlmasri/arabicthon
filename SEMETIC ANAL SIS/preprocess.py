import re
import string
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer
from nltk.tokenize import word_tokenize
# libraries for data split and feature extraction

class datapreprocessing:
        
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
        translator = str.maketrans('', '', datapreprocessing.punctuations)
        text = text.translate(translator)
        
        # remove Tashkeel
        text = re.sub(datapreprocessing.arabic_diacritics, '', text)
        
        #remove longation
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ى", "ي", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("ة", "ه", text)
        text = re.sub("گ", "ك", text)
        
        text = ' '.join(datapreprocessing.stemmer.stem(word) for word in text.split() if datapreprocessing.stemmer.stem(word) not in datapreprocessing.stop_words)
        # text = word_tokenize(text)
        # text = ' '.join(text) 
        text = word_tokenize(text)
    
        
        text = ' '.join(text) 
    
        return text