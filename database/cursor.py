import psycopg2
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

        print(self.CURSOR.execute("SELECT * FROM news;"))
        # TODO: function for inserting stuff to the table 
        # TODO: function for filtering stuff by the category
        # TODO: function for filtering stuff by the date
        # TODO: function for searching for stuff in the table ( title )


if __name__ == "__main__":
    DB = DB_CONTROLLER()
