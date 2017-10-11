import urllib2
from database import DataBase


class Reader(object):

    def __init__(self):
        self.data_base = DataBase()

    def read_html(self, movie_imdb_number):

        movie_url = "http://www.imdb.com/title/tt"
        movie_url += str(movie_imdb_number)

        try:
            web_html = urllib2.urlopen(movie_url)
            web_html = web_html.read()
            web_html_list = web_html.split("\n")
            tv_words = ["Series", "Episode"]
            if tv_words[0] in web_html_list[94]:
                return 0

            elif tv_words[1] in web_html_list[94]:
                return 0

        except:
            return 0

        movie_length = ""
        try:
            for line in web_html_list[840:860]:
                if line[(len(line) - 3):(len(line))] == "min":
                    movie_length = line.replace("                        ", "")
                    break
            if not "h" in movie_length:
                return 0
        except:
            return 0

        if movie_length == "":
            return 0

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
            return 0

        if movie_year < 1950:
            return 0
        else:
            movie_year = str(movie_year)

        movie_name = web_html_list[94].split("<meta property='og:title' content=")[1].split(" (")[0][1:]

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
                return 0

        except:
            return 0

        movie_info = {"name": movie_name,
                      "year": movie_year,
                      "stars": movie_stars,
                      "directors": movie_directors,
                      "description": movie_text,
                      "length": movie_length,
                      "rating": movie_rate,
                      "genres": movie_genres,
                      "imdb_number": movie_imdb_number}

        self.data_base.add_data(movie_info)

        return 1


def main():

    movie_imdb_number = int(raw_input("Enter movie number: "))

    reader = Reader()
    movie_pass = reader.read_html(movie_imdb_number)
    if movie_pass == 0:
        print("not pass")
    else:
        print("pass")

if __name__ == '__main__':
    main()
