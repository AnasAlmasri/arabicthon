import requests
import urllib.parse
from bs4 import BeautifulSoup


class PoetScraper:

    base_url = "https://www.google.com/search?q="

    @staticmethod
    def search(keywords: list):
        search_str = "+".join(keywords)
        search_url = PoetScraper.base_url + urllib.parse.quote_plus(search_str)

        r = requests.get(search_url)
        r.text

        soup = BeautifulSoup(r.text, "html.parser")

        content = soup.find_all("span", {"dir": "rtl"}, recursive=True)

        text = ""
        for i in range(1, 7):
            text += " " + content[i].get_text()

        return text
