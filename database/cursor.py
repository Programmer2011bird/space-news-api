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
        keyword: str = keyword.replace(" ", "+")
        VALUES: tuple = (keyword, )
        
        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content, author FROM news WHERE name_search @@ to_tsquery('english', %s);", VALUES)
        search_results: list = self.CURSOR.fetchall()
        
        return search_results
    
    def search_date(self, Date: datetime.date) -> list:
        Date: str = Date.__str__()
        VALUES: tuple = (Date, )
        
        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content, author FROM news WHERE date=%s;", VALUES)
        search_results: list = self.CURSOR.fetchall()

        return search_results
    
    def search_between_dates(self, start_date: datetime.date, end_date: datetime.date) -> list:
        start_date: str = start_date.__str__()
        end_date: str = end_date.__str__()
        VALUES: tuple = (start_date, end_date)

        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content, author FROM news WHERE date BETWEEN %s AND %s;", VALUES)
        search_results: list = self.CURSOR.fetchall()

        return search_results
    
    def search_category(self, category: str) -> list:
        VALUES: tuple = (category, )
        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content, author FROM news WHERE category=%s;", VALUES)
        search_results: list = self.CURSOR.fetchall()

        return search_results
    
    def search_author(self, author: str) -> list:
        author = author + " "
        VALUES: tuple = (author, )

        search_query = self.CURSOR.execute(f"SELECT name, category, date, link, summary, article_content, author FROM news WHERE author=%s;", VALUES)
        search_results: list = self.CURSOR.fetchall()

        return search_results
