from database import DataBase


class SearchMovie(object):
    def __init__(self):
        self.movies_info = []
        self.data_base = DataBase()

    def read_database_files(self):

        movies_info = self.data_base.read_data("SELECT * FROM movies_info")

        for movie_info_list in movies_info:

            movie_info = {
                "name": movie_info_list[0],
                "year": int(movie_info_list[1]),
                "rating": movie_info_list[2],
                "length": int(movie_info_list[3]),
                "genres": movie_info_list[4].split(', '),
                "directors": movie_info_list[5].split(', '),
                "stars": movie_info_list[6].split(', '),
                "description": movie_info_list[7],
                "imdb_number": int(movie_info_list[8])}

            self.movies_info.append(movie_info)

    def search_movie(self, user_data):

        for key in user_data.keys():
            if user_data[key] == [""]:
                user_data[key] = "no data"

        self.read_database_files()

        # step 1
        step1_match_movies = []
        for movie in self.movies_info:

            genres_number = 0
            for user_genre in user_data["genres"]:
                if user_genre in movie["genres"]:
                    genres_number += 1

            if len(user_data["genres"]) >= 2:
                if genres_number < 2:
                    continue
            else:
                if genres_number == 0:
                    continue

            if (movie["year"] >= user_data["range_of_years"][0]) and (movie["year"] <= user_data["range_of_years"][1]):
                if (movie["length"] >= user_data["length"][0]) and (movie["length"] <= user_data["length"][1]):
                    step1_match_movies.append(movie)
        # step 2
        step2_match_movies = step1_match_movies
        for index, movie in enumerate(step2_match_movies):

            step2_match_movies[index]['score'] = 0.0

            step2_match_movies[index]['score'] += float((user_data["range_of_years"][1] - user_data["range_of_years"][0]) - (user_data["range_of_years"][1] - movie["year"])) / 10

            if user_data["key_words"] != "no data":
                for user_keyword in user_data["key_words"]:
                    if user_keyword in movie["description"]:
                        step2_match_movies[index]['score'] += 1

            if user_data["stars"] != "no data":
                for user_star in user_data["stars"]:
                    if user_star in movie["stars"]:
                        step2_match_movies[index]['score'] += 4

            if user_data["directors"] != "no data":
                for user_director in user_data["directors"]:
                    if user_director in movie["directors"]:
                        step2_match_movies[index]['score'] += 4


        # step 3
        step3_match_movies = step2_match_movies
        for i in range(len(step3_match_movies)):
            for j in range(len(step3_match_movies) - i - 1):
                if step3_match_movies[j]['score'] > step3_match_movies[j + 1]['score']:
                    step3_match_movies[j], step3_match_movies[j + 1] = step3_match_movies[j + 1], step3_match_movies[j]

        step3_match_movies.reverse()

        if len(step3_match_movies) > 5:
            for i in range(5, len(step3_match_movies) - 1):
                step3_match_movies.remove(step3_match_movies[5])

        step3_match_movies.reverse()

        for i in range(len(step3_match_movies)):
            for j in range(len(step3_match_movies) - i - 1):
                if step3_match_movies[j]['rating'] > step3_match_movies[j + 1]['rating']:
                    step3_match_movies[j], step3_match_movies[j + 1] = step3_match_movies[j + 1], step3_match_movies[j]

        step3_match_movies.reverse()

        for movie in step3_match_movies:
            for movie_key in movie.keys():
                print("{0}: {1}".format(movie_key, movie[movie_key]))
            print("")

        if len(step3_match_movies) > 0:
            return step3_match_movies[0]["name"]
        else:
            return "I didn't find any thing"
