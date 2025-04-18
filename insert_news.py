from scraper import formatter
from database import cursor
from time import sleep
import schedule
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
                news["article_content"],
                news["author"]
            )


def main():
    INS = inserter()

schedule.every().day.at("01:00").do(main)
schedule.every().day.at("18:00").do(main)

while True:
    schedule.run_pending()
    sleep(3600)
