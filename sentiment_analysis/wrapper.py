from Dictionary import WordInterpretation
from pandawetwipe import wetWiper
from preprocess import datapreprocessing
from LOGICREGRESSION import LOGREG
from poem_scraper import PoemScraper


class ModelWrapper:
    @staticmethod
    def predict_logreg(to_predict, model):
        return model.predict([datapreprocessing.preprocess(to_predict)])

    @staticmethod
    def train_model():
        LOGREG.TrainModel()

    @staticmethod
    def create_data():
        PoemScraper.scrape()
        wetWiper.WipeTheThing()

    @staticmethod
    def GetMeaning(word):
        return WordInterpretation.getMeaning(word)
