import pandas as pd


class DataCleaner:
    @staticmethod
    def run():
        loadeddata = pd.read_csv("poempandas.csv", index_col=0)

        loadeddata = loadeddata.dropna()

        loadeddata.reset_index(drop=True, inplace=True)
        loadeddata.to_csv("test.csv", encoding="utf-8-sig")

        count = 0
        todelete = []
        for i in range(len(loadeddata)):

            if "المزيد عن" in loadeddata["String"][i]:
                count = count + 1
                todelete.append(i)

            elif "أضف معلومة او شرح" in loadeddata["String"][i]:
                count = count + 1
                todelete.append(i)

        loadeddata = loadeddata.drop(labels=todelete, axis=0)

        loadeddata.reset_index(drop=True, inplace=True)

        loadeddata.to_csv("poempandas.csv", encoding="utf-8-sig")
