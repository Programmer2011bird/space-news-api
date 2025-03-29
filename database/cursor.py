import psycopg2
import datetime
import conf


class DB_CONTROLLER:
    def __init__(self):
        self.CONN = psycopg2.connect(
            database=conf.database,
            user=conf.user,
            password=conf.password,
            host=conf.host,
            port=conf.port
        )
        self.CURSOR = self.CONN.cursor()

        # function for filtering stuff by the date

    def insert(self, name:str, category:str, date:datetime.date, link:str, summary:str, article_content:str) -> None:
        self.CURSOR.execute("SELECT name FROM news;")
        self.IS_REPUTATIVE: bool = False

        titles: list = self.CURSOR.fetchall()

        for title in titles:
            if name == title[0]:
                print("reputative insert : Not pushing changes to db")
                self.IS_REPUTATIVE = True
                break
            else:
                self.IS_REPUTATIVE = False
                pass
        
        if not self.IS_REPUTATIVE:
            self.CURSOR.execute(f"INSERT INTO news (name, category, date, link, summary, article_content) VALUES ('{name}', '{category}', '{date.__str__()}', '{link}', '{summary}', '{article_content}');")
            self.CONN.commit()
            
            print("successfully inserted the data into db")
    
    def search_title(self, keyword: str) -> list:
        keyword = keyword.replace(" ", "+")
        
        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content FROM news WHERE title_search @@ to_tsquery('english', '{keyword}')")
        search_results: list = self.CURSOR.fetchall()
        
        return search_results
    
    def search_date(self, Date: datetime.date) -> list:
        Date: str = Date.__str__()
        
        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content FROM news WHERE date='{Date}';")
        search_results: list = self.CURSOR.fetchall()

        return search_results
    
    def search_between_dates(self, start_date: datetime.date, end_date: datetime.date) -> list:
        start_date: str = start_date.__str__()
        end_date: str = end_date.__str__()

        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content FROM news WHERE date BETWEEN '{start_date}' AND '{end_date}';")
        search_results: list = self.CURSOR.fetchall()

        return search_results


if __name__ == "__main__":
    DB: DB_CONTROLLER = DB_CONTROLLER()
    print(DB.search_between_dates(datetime.date(2025, 3, 28), datetime.date(2025, 4, 1)))
