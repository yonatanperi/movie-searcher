import urllib2
import sys
from database import DataBase


class Reader(object):

    def __init__(self):
        self.data_base = DataBase()

    def read_html(self):

        last_movie = self.data_base.read_data("SELECT * FROM movies_info ORDER BY imdb_number DESC LIMIT 1")

        for i in range(last_movie[len(last_movie) - 1], 9999999):
            movie_url = "http://www.imdb.com/title/tt"
            movie_url += str(i)

            try:
                web_html = urllib2.urlopen(movie_url)
                web_html = web_html.read()
                web_html_list = web_html.split("\n")
                sys.stdout.write("\n{0}. {1}".format(1000000 - 1111161 + i, i))
                tv_words = ["Series", "Episode"]
                if tv_words[0] in web_html_list[94]:
                    continue

                elif tv_words[1] in web_html_list[94]:
                    continue

            except:
                continue


            """for index, line in enumerate(web_html_list):
                print("{0}. {1}".format(index, line))"""

            movie_length = ""
            try:
                for line in web_html_list[840:860]:
                    if line[(len(line) - 3):(len(line))] == "min":

                        movie_length = line.replace("                        ", "")
                        break
                if not "h" in movie_length:
                    continue
            except:
                continue

            if movie_length == "":
                continue

            try:
                movie_length = movie_length.split("h ")
                movie_length = movie_length[1].replace("min", "")
                movie_length = (int(movie_length[0]) * 60) + int(movie_length[1])
            except:
                movie_length = movie_length.split("h")
                movie_length = int(movie_length[0]) * 60

            try:
                try:
                    movie_year = int(
                        web_html_list[94].replace("""<meta property='og:title' content=""", "").split(" (")[1].replace(
                            ')" />', ""))
                except:
                    movie_year = int(
                        web_html_list[94].replace("""<meta property='og:title' content=""", "").split(" (")[1].replace(
                            ')" />', "").replace("TV Movie ", ""))
            except:
                continue

            if movie_year < 1950:
                continue
            else:
                movie_year = str(movie_year)

            movie_name = web_html_list[94].split("<meta property='og:title' content=")[1].split(" (")[0][1:]

            """rating_list = ["G", "M", "R", "X", "PG", "PG-13", "NC-17"]
            for i in rating_list:
                if i in web_html_list[849]:
                    movie_age = web_html_list[849].split('<meta itemprop="contentRating" content=')[1].split(">")[1]
                else:
                    movie_age = "no data"""""

            try:
                movie_stars = \
                web_html_list[97].split('<meta name="description" content="Directed by ')[1].split(".  With ")[1].split(
                    ". ")[0]
            except:
                movie_stars = "no data"
            try:
                movie_directors = \
                web_html_list[97].split('<meta name="description" content="Directed by ')[1].split(".  With ")[0]
            except:
                movie_directors = "no data"
            try:
                movie_text = \
                web_html_list[97].split('<meta name="description" content="Directed by ')[1].split(".  With ")[1].split(
                    ". ")[1]

                movie_text = movie_text[:(len(movie_text) - 4)]
            except:
                movie_text = "no data"
            try:
                movie_rate = web_html_list[819].replace('<strong title="', '')
                movie_rate = movie_rate.split(' based on ')[0]
                if len(movie_rate) != 3:
                    movie_rate = 0
            except:
                movie_rate = 0

            genres_list = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama",
                           "Family",
                           "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance",
                           "Sci-Fi",
                           "Sport", "Thriller", "War", "Western"]

            movie_genres = []

            try:
                for line in web_html_list[850:1000]:
                    for genre in genres_list:
                        if genre in line:
                            movie_genres.append(genre)

                movie_genres = list(set(movie_genres))
                movie_genres = ', '.join(movie_genres)

                if movie_genres == "":
                    continue

            except:
                continue

            sys.stdout.write(" V")

            movie_info = {"name": movie_name,
                          "year": movie_year,
                          "stars": movie_stars,
                          "directors": movie_directors,
                          "description": movie_text,
                          "length": movie_length,
                          "rating": movie_rate,
                          "genres": movie_genres,
                          "imdb_number": i}

            self.data_base.add_data(movie_info)



def main():
    reader = Reader()
    reader.read_html()

if __name__ == '__main__':
    main()
