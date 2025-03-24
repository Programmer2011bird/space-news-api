from bs4 import BeautifulSoup
import datetime
import requests


class scraper:
    def __init__(self) -> None:
        self.URL: str = "https://www.space.com/news"
    
    def scrape(self) -> list:
        self.RESPONSE: requests.Response = requests.get(self.URL)
        self.HTML_CONTENT: str = self.RESPONSE.text

        self.SOUP: BeautifulSoup = BeautifulSoup(self.HTML_CONTENT, 'html.parser')
        print(type(self.SOUP))
        self.NEWS_DIVS: list = []
        self.CONTENT_DIVS: list = []

        for i in range(11):
            self.NEWS_DIVS.append(self.SOUP.find('div', attrs={'class':f'listingResult small result{i}'}))
        
        return self.NEWS_DIVS
    

if __name__ == "__main__":
    SCRAPER: scraper = scraper()
    SCRAPER.scrape()
