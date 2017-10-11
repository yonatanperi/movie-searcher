import ttk
import datetime
from Tkinter import *
from search_movie import SearchMovie

class Graphics(object):
    def __init__(self):
        
        self.root = Tk()
        self.root.title("Movie Searcher")
        self.root.minsize(width=850, height=655)
        self.root.grid_propagate(False)

        self.user_data = {
            "range_of_years": [],
            "length": [],
            "genres": [],
            "directors": [],
            "stars": [],
            "key_words": []}

        # GUI

        # Labels
        Label(self.root, text="genres", font=(None, 15)).grid(row=1, pady=20, padx=(70, 0))
        Label(self.root, text="range of years:", font=(None, 15)).grid(row=2, column=3, padx=(50, 10))
        Label(self.root, text="-", font=(None, 30)).grid(row=2, column=5, padx=(20, 10))
        Label(self.root, text="range of lengths:", font=(None, 15)).grid(row=3, column=3, padx=(50, 10))
        Label(self.root, text="-", font=(None, 30)).grid(row=3, column=5, padx=(20, 10))
        Label(self.root, text="final result:", font=(None, 15)).grid(row=5, column=4, padx=(20, 10))
        self.lbl_final_result = Label(self.root, text="", font=(None, 20))
        self.lbl_final_result.grid(row=6, column=4, padx=(20, 10), columnspan=3)

        # Check-Buttons
        self.genres_list = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama",
                       "Family",
                       "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi",
                       "Sport", "Thriller", "War", "Western"]

        for index, genre in enumerate(self.genres_list):
            globals()['self.check_button_{0}_active'.format(genre.lower())] = IntVar()
            if index >= len(self.genres_list) / 2:
                globals()['self.check_button_{0}'.format(genre.lower())] = Checkbutton(self.root, text=genre, height=2, font=(None, 12), variable=globals()['self.check_button_{0}_active'.format(genre.lower())])
                globals()['self.check_button_{0}'.format(genre.lower())].grid(row=(index + 2) - len(self.genres_list) / 2, column=1, sticky=W, pady=2, padx=(35, 10))
            else:
                globals()['self.check_button_{0}'.format(genre.lower())] = Checkbutton(self.root, text=genre, height=2,font=(None, 12),variable=globals()['self.check_button_{0}_active'.format(genre.lower())])
                globals()['self.check_button_{0}'.format(genre.lower())].grid(row=(index + 2), column=0,sticky=W, pady=2, padx=(5, 10))

        # Combo Boxes
        now = datetime.datetime.now()
        combo_years = []
        for year in range(1950, now.year, 5):
            combo_years.append(year)

        combo_years.append(now.year)
        combo_years.reverse()

        self.combobox_range_of_years_min = ttk.Combobox(self.root, values=combo_years, textvariable=combo_years, font=(None, 15),
                                                   width=10, height=15)
        self.combobox_range_of_years_min.grid(row=2, column=4)

        combo_years.remove(1950)

        self.combobox_range_of_years_max = ttk.Combobox(self.root, values=combo_years, textvariable=combo_years, font=(None, 15),
                                                        width=10, height=15)
        self.combobox_range_of_years_max.grid(row=2, column=6)

        combo_lengths = []
        for h_length in range(1, 3):
            for min_length in range(0, 60, 15):
                min_length = str(min_length)
                if len(min_length) == 1:
                    min_length = min_length + "0"
                combo_lengths.append("{0}:{1}".format(h_length, min_length))

        combo_lengths.append("3:00")
        combo_lengths.reverse()

        self.combobox_range_of_lengths_min = ttk.Combobox(self.root, values=combo_lengths, textvariable=combo_lengths,
                                                     font=(None, 15), width=10, height=15)
        self.combobox_range_of_lengths_min.grid(row=3, column=4)

        combo_lengths.remove("1:00")

        self.combobox_range_of_lengths_max = ttk.Combobox(self.root, values=combo_lengths, textvariable=combo_lengths,
                                                     font=(None, 15), width=10, height=15)
        self.combobox_range_of_lengths_max.grid(row=3, column=6)

        # main button
        button_style = ttk.Style()
        button_style.configure('my.TButton', font=('Helvetica', 15))
        self.main_button = ttk.Button(text="Search", style='my.TButton', command=self.search_for_movie)
        self.main_button.grid(row=5, column=3, padx=(35, 10))


    def search_for_movie(self):
        self.lbl_final_result["text"] = ""

        self.user_data = {
            "range_of_years": [],
            "length": [],
            "genres": [],
            "directors": [],
            "stars": [],
            "key_words": []}
        # get genres
        for genre in self.genres_list:
            if globals()['self.check_button_{0}_active'.format(genre.lower())].get() == 1:
                self.user_data["genres"].append(genre)

        if self.user_data["genres"] == []:
            self.lbl_final_result["text"] = "you must chose at\n list one genre"
            return 0

        # get years
        if not (self.combobox_range_of_years_min.get().isdigit() and self.combobox_range_of_years_max.get().isdigit()):
            self.lbl_final_result["text"] = "you must give a year\n in the year box!"
            return 0

        self.user_data["range_of_years"] = [int(self.combobox_range_of_years_min.get()),
                                            int(self.combobox_range_of_years_max.get())]

        # get length
        try:
            for length in (self.combobox_range_of_lengths_min.get(),
                           self.combobox_range_of_lengths_max.get()):
                length = length.split(":")
                length = (int(length[0]) * 60) + int(length[1])
                self.user_data["length"].append(int(length))
        except:
            self.lbl_final_result["text"] = "you must give an hour\n in the length box!"
            return 0

        # search for the movie
        file_reader = SearchMovie()
        final_movie = file_reader.search_movie(self.user_data)
        self.lbl_final_result["text"] = final_movie


def main():
    graphic = Graphics()
    graphic.root.mainloop()

if __name__ == '__main__':
    main()