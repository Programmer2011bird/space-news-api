from bs4 import BeautifulSoup
import requests


class scraper:
    def __init__(self) -> None:
        self.URL: str = "https://www.space.com/news"
    
    def scrape(self) -> list:
        self.RESPONSE: requests.Response = requests.get(self.URL)
        self.HTML_CONTENT: str = self.RESPONSE.text

        self.SOUP: BeautifulSoup = BeautifulSoup(self.HTML_CONTENT, 'html.parser')
        self.NEWS_DIVS: list = []
        self.CONTENT_DIVS: list = []

        for i in range(11):
            self.NEWS_DIVS.append(self.SOUP.find('div', attrs={'class':f'listingResult small result{i}'}))
        
        return self.NEWS_DIVS
    
    def scrape_whole_article(self, link: str) -> str:
        self.RESPONSE: requests.Response = requests.get(link)
        self.SOUP: BeautifulSoup = BeautifulSoup(self.RESPONSE.text, "html.parser")
        self.PARENT_DIV = self.SOUP.find("div", attrs={"id":"article-body"})
        self.PARAGRAPHS: list = self.PARENT_DIV.find_all("p")
        self.PARAGRAPH: str = ""
        
        for p in self.PARAGRAPHS:
            self.PARAGRAPH += p.text

        return self.PARAGRAPH