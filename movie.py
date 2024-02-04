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
        display_highestrated_movies(length):
            Display selected list of highest score movies.

        ---Data Operations---
        filter_movies(args):
            Prints all the data with given genre.
        display_unique_genre():
            Prints all unique genre.

        ---Additional Complexity---
        rate_movies(movie_id, new_rating):
            Overwrite the imdb score.
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

    def display_highestrated_movies(self, length: int):
        """
        Display selected number of movies with highest score.

        Parameter:
            length (int): length of movies to display.

        Return:
            dataframe with movie name and score in descending order.
        """
        if isinstance(length, (int)):
            # check whether the input is valid integer
            dataframe = self.readcontent_fromcsv(
            ).sort_values(by=['IMDB Score'], ascending=False)
            print(dataframe[:length])
        else:
            print("Enter a valid number.")

    def filter_movies(self, *args):
        """
        Filter movies with selected genre

        Parameter:
            args (tuple): total genre to be selected from.

        Return:
            Dataframe containing args as a genre or empty dataframe.
        """

        pattern = '|'.join(list(args))
        df = self.readcontent_fromcsv()
        filtered_frame = df[df['Genre'].str.contains(
            pattern, case=False, na=False)]
        print(filtered_frame)

    def display_unique_genre(self):
        """
        Splits the value of Genre column with '|' delimiter and prints unique
        values.

        Return:
            List of unique strings.
        """
        df = self.readcontent_fromcsv()['Genre'].str.split('|')
        unique_genres = df.explode('Genre').unique()
        print(unique_genres)

    def rate_movies(self, movie_id: int, new_rating: float):
        """
        Update the imdb Score of a specific movie.

        Parameter:
            movie_id (int): Specific id of a movie.
            new_rating (float:.2f): New rating specified by user.

        Return:
            Successful message or validation error.
        """
        if isinstance(movie_id, int) and isinstance(new_rating, (float, int)):
            df = self.readcontent_fromcsv()
            try:
                selected_row_index = df.index[df['imdbId'] == movie_id][0]
            except:
                print(f'Given id:{movie_id} does not exist.')
                return
            rounded_float = round(new_rating, 1)
            df.loc[selected_row_index, 'IMDB Score'] = rounded_float
            df.to_csv(self._path, index=False)
            print(f'Value for id:{movie_id} updated to {rounded_float}.')
        else:
            print('Please enter valid data.')


ENCODINGS = 'charmap'
# change the encodings according to the requirements.

if __name__ == '__main__':
    movie_object = MovieManager("./movies.csv", ENCODINGS)
    # movie_object.countdata_fromcsv()
    # movie_object.averagescore()
    # movie_object.display_highestrated_movies(length=5)
    # movie_object.filter_movies('Thriller', 'Drama')
    # movie_object.display_unique_genre()
    # movie_object.rate_movies(112302, 4)
