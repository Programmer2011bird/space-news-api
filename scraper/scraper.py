from bs4 import BeautifulSoup
from lxml import etree
import requests


class scraper:
    def __init__(self) -> None:
        self.URL: str = "https://www.space.com/news"
        self.RESPONSE: requests.Response = requests.get(self.URL)
        self.HTML_CONTENT: str = self.RESPONSE.text

        self.SOUP: BeautifulSoup = BeautifulSoup(self.HTML_CONTENT, 'html.parser')
        self.NEWS_DIVS: list = []

        for i in range(11):
            self.NEWS_DIVS.append(self.SOUP.find('div', attrs={'class':f'listingResult small result{i}'}))
        
        for DIV in self.NEWS_DIVS[1:]:
            print(DIV.find_all('div', attrs={'class':'content'}))
        

if __name__ == "__main__":
    SCRAPER: scraper = scraper()
# /html/body/div[6]/div[4]/article/div/div[1]/div[5]/div/section/div/div[4]
# /html/body/div[6]/div[4]/article/div/div[1]/div[5]/div/section/div/div[9]
