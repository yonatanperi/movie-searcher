import sqlite3


class DataBase(object):
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.conn.text_factory = str
        self.c = self.conn.cursor()

    def create_table(self, table_name, table_values):
        self.c.execute("CREATE TABLE IF NOT EXISTS {0}({1})".format(table_name, table_values).replace("[", "").replace("]", ""))

    def add_data(self, movie_info):

        data = self.read_data("SELECT imdb_number FROM movies_info")

        if (movie_info["imdb_number"], ) in data:
            return 0

        self.c.execute("INSERT INTO movies_info(name, year, rating, length, genres, directors, stars, description, imdb_number) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (movie_info["name"],
             movie_info["year"],
             movie_info["rating"],
             movie_info["length"],
             movie_info["genres"],
             movie_info["directors"],
             movie_info["stars"],
             movie_info["description"],
             movie_info["imdb_number"]))

        self.conn.commit()

    def read_data(self, sq_read_line):
        self.c.execute(sq_read_line)
        data = self.c.fetchall()
        return data
