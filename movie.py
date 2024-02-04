"""
Entrypoint for the application.
Logic behind the Movie Management system.
"""

import pandas as pd


class MovieManager:
    """
    A class to represent Movie logic.

    Attributes:
        _path (String): A path to the CSV file.
        _encoding (String): Encoding type for CSV file.

    Methods:
        ---Data Loading---
        readcontent_fromcsv():
            Read the csv file from the path.
        countdata_fromcsv():
            Prints the length of data in csv file.

        ---Advanced manipulation---
        averagescore():
            Prints average movie score.
        display_selected_movies(length):
            Display selected list of highest score movies.
    """

    def __init__(self, path, encoding):
        """
        Constructs all the necessary attributes for the Movie object.

        Parameters:
            path (String): A path to the CSV file.
            encoding (String): Encoding type for CSV file.
        """
        self._path = path
        self._encoding = encoding

    def readcontent_fromcsv(self):
        """
        Takes in a string path of CSV file and return number of data.
        If the path is not valid returns None.

        Return:
            df (dataframe): 2D representation of data.

        """
        try:
            df = pd.read_csv(self._path, encoding=self._encoding)
        except FileNotFoundError:
            return "Path to the CSV file does not exists."
        return df

    def countdata_fromcsv(self):
        """
        Takes the dataframe and returns the length of columns.

        Return:
            Total number of data (int).
        """
        print(f"Total number of data: {self.readcontent_fromcsv().shape[0]}.")

    def averagescore(self):
        """
        Count and display the average of all movie rating.

        Return:
            Average score of all movie (float:.2f).
        """
        mean = self.readcontent_fromcsv()['IMDB Score'].mean()
        print(f"The average score of all movies is {mean:.2f}.")

    def display_selected_movies(self, length):
        """
        Display selected number of movies with highest score.

        Parameter:
            length (int): length of movies to display.

        Return:
            dataframe with movie name and score in descending order.
        """
        if isinstance(length, (int)):
            dataframe = self.readcontent_fromcsv(
            ).sort_values(by=['IMDB Score'], ascending=False)
            print(dataframe[['imdbId', 'Title', 'IMDB Score']][:length])
        else:
            print("Enter a valid number.")


ENCODINGS = 'charmap'
if __name__ == '__main__':
    movie_object = MovieManager("./movies.csv", ENCODINGS)
    movie_object.countdata_fromcsv()
    movie_object.averagescore()
    movie_object.display_selected_movies(length=5)
