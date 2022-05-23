from data_cleaner import DataCleaner
from preprocess import DataPreprocessing
from experiments.logistic_regression import LogisticRegression
from poem_scraper import PoemScraper


class ModelWrapper:
    @staticmethod
    def predict_logreg(to_predict, model):
        return model.predict([DataPreprocessing.preprocess(to_predict)])

    @staticmethod
    def train_model():
        LogisticRegression.train_model()

    @staticmethod
    def create_data():
        PoemScraper.scrape()
        DataCleaner.run()
