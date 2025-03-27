from scraper import scraper
import datetime


class formatter:
    def __init__(self) -> None:
        self.scraper: scraper = scraper()
        self.NEWS_DIVS: list = self.scraper.scrape()
    
    def format(self):
        self.WHOLE_INFO: list[dict[str, str | datetime.date]] = []

        for index in range(len(self.NEWS_DIVS) - 1):
            try:
                CONTENT = self.NEWS_DIVS[index + 1].find('div', attrs={'class':'content'})
    
                CATEGORY: str = self.NEWS_DIVS[index + 1].find('a', attrs={'class':'category-link'}).text
                LINK: str = self.NEWS_DIVS[index + 1].find_all('a', attrs={'class':'article-link'}, href=True)[0]['href']
                ARTICLE_CONTENT: str = self.scraper.scrape_whole_article(LINK)

                NAME: str = CONTENT.find('h3', attrs={'class':'article-name'}).text
                SUMMARY: str = CONTENT.find('p', attrs={'class': 'synopsis'}).text
                DATE: datetime.date = datetime.date.today()
    
                ITERATION_INFO: dict[str, str | datetime.date] = {
                    'Name': NAME,
                    'Category': CATEGORY,
                    'Date': DATE,
                    'Link': LINK,
                    'Summary': SUMMARY,
                    'Article_Content': ARTICLE_CONTENT
                }
    
                self.WHOLE_INFO.append(ITERATION_INFO)

            except AttributeError:
                pass

        return self.WHOLE_INFO
    

# if __name__ == "__main__":
    # FORMATTER: formatter = formatter()
    # print(FORMATTER.format())
