from Dictionary import WordInterpretation
from pandawetwipe import wetWiper
from preprocess import datapreprocessing
from LOGICREGRESSION import LOGREG
from scraper0 import poemscraper


class ModelWrapper:

    @staticmethod
    def predict_logreg(to_predict,model):
       return model.predict([datapreprocessing.preprocess(to_predict)])
       

    @staticmethod
    def TrainModel():
        LOGREG.TrainModel()
        
    @staticmethod
    def CreateData():
        poemscraper.ScrapeIt()
        wetWiper.WipeTheThing()
    
    @staticmethod
    def GetMeaning(word):
        return(WordInterpretation.getMeaning(word))
    


    
