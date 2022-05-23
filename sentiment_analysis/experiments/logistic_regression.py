import pickle
import pandas as pd
from sklearn.utils import shuffle
from preprocess import datapreprocessing
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV


class LogisticRegression:
    @staticmethod
    def train_model():
        loadeddata = pd.read_csv("poempandas.csv", index_col=0)
        loadeddata.reset_index(drop=True, inplace=True)

        loadeddata["processed"] = loadeddata["String"].apply(
            datapreprocessing.preprocess
        )
        loadeddata = shuffle(loadeddata)

        # splitting the data into target and feature
        feature = loadeddata.processed
        target = loadeddata.Label

        # splitting into train and tests
        X_train, X_test, Y_train, Y_test = train_test_split(
            feature, target, test_size=0.2
        )

        # make pipeline
        pipe = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000))

        # make param grid
        param_grid = {
            "logisticregression__C": [0.01, 0.1, 1, 10, 100],
            "logisticregression__solver": ["newton-cg", "lbfgs", "sag", "saga"],
        }

        # create and fit the model
        model = GridSearchCV(pipe, param_grid, cv=5)
        model.fit(X_train, Y_train)

        # make prediction and print accuracy
        prediction = model.predict(X_test)
        print(f"Accuracy score is {accuracy_score(Y_test, prediction):.2f}")
        print(classification_report(Y_test, prediction))

        with open("logregmodel.pkl", "wb") as f:
            dct = pickle.dump(model, f)
