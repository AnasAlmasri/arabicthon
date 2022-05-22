import requests
import requests
from bs4 import BeautifulSoup
import numpy as np
import json
import pandas as pd


class WordInterpretation:
    
    @staticmethod
    def getdata(URL):
        

    
        page = requests.get(str(URL))

     
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.body#find(id='top')
        results=soup.find(class_='termDefintion')
        results=results.contents[0].getText()
        results=(str(results).strip())
        return(results)
        
    @staticmethod
    def getMeaning(word):
        
        meaning=WordInterpretation.getdata("https://www.arabdict.com/ar/"+"عربي-عربي/"+str(word))
        return(meaning)
        

