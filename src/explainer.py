from bs4 import BeautifulSoup
import requests


class WordInterpretation:
    @staticmethod
    def get_data(URL):
        page = requests.get(str(URL))

        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.body  # find(id='top')
        results = soup.find(class_="termDefintion")
        results = str(results.contents[0])
        results = str(results).strip()
        return results

    @staticmethod
    def get_meaning(word):
        return WordInterpretation.get_data(
            "https://www.arabdict.com/ar/" + "عربي-عربي/" + str(word)
        )
