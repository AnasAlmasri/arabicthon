
from databuttwiperpanda import ButtWiper
from preprocess import datapreprocessing
from LOGICREGRESSION import LOGREG
from scraper0 import poemscraper
import pickle 

class ModelWrapper:

    model_name = "jhdjskvldskvnsd/njsdvnsj"

    @staticmethod
    def predict_logreg(to_predict,model):
       return model.predict([datapreprocessing.preprocess(to_predict)])
       

    @staticmethod
    def TrainModel():
        LOGREG.TrainModel()
        
    @staticmethod
    def CreateData():
        poemscraper.ScrapeIt()
        ButtWiper.WipeTheButt()


    
