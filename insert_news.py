from scraper import formatter
from database import cursor
import datetime


class inserter:
    def __init__(self):
        self.DB_CONTROLLER: cursor.DB_CONTROLLER = cursor.DB_CONTROLLER()
        self.FORMATTER: formatter.formatter = formatter.formatter()

        self.news: list[dict[str, str | datetime.date]] = self.FORMATTER.format()
        
        for news in self.news:
            self.DB_CONTROLLER.insert(
                news["name"],
                news["category"],
                news["date"],
                news["link"],
                news["summary"],
                news["article_content"]
            )


if __name__ == "__main__":
    INS = inserter()
