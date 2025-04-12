from .conf import database, user, password, host, port
import psycopg2
import datetime


class DB_CONTROLLER:
    def __init__(self):
        self.CONN = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.CURSOR = self.CONN.cursor()

    def insert(self, name:str, category:str, date:datetime.date, link:str, summary:str, article_content:str, author:str) -> None:
        self.CURSOR.execute("SELECT name FROM news;")
        self.IS_REPUTATIVE: bool = False

        titles: list = self.CURSOR.fetchall()

        for title in titles:
            if name == title[0]:
                self.IS_REPUTATIVE = True
                print("reputative insert : Not pushing changes to db")
                
                break

            else:
                self.IS_REPUTATIVE = False
                
                pass
        
        if not self.IS_REPUTATIVE:
            VALUES: tuple = (name, category, date.__str__(), link, summary, article_content, author)
            self.CURSOR.execute(f"INSERT INTO news (name, category, date, link, summary, article_content, author) VALUES (%s, %s, %s, %s, %s, %s, %s);", VALUES)
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
    
    def search_category(self, category: str) -> list:
        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content FROM news WHERE category='{category}'")
        search_results: list = self.CURSOR.fetchall()

        return search_results
