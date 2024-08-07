"""
Entrypoint for the application.
Logic behind the Movie Management system.

pylint- 10/10
"""

import pandas as pd
import matplotlib.pyplot as plt


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
        recommend_movie(genre):
            Return some movies and highest rated movie of given genre.

        ---Chart Creation---
        chart_distribution():
            Plot a area graph showing the movie ratings.
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
            return pd.read_csv(self._path, encoding=self._encoding)
        except FileNotFoundError as e:
            return f'Could not resove the path: {e}'

    def get_length(self):
        """
        Takes the dataframe and returns the length of columns.

        Return:
            Total number of data (int).
        """
        return self.readcontent_fromcsv().shape[0]

    def get_average_score(self):
        """
        Count and return the average of all movie rating.

        Return:
            Average score of all movie (float:.2f).
        """
        return self.readcontent_fromcsv()['IMDB Score'].mean()

    def get_highest_rated_movies(self, length: int):
        """
        Return selected number of movies with highest score.

        Parameter:
            length (int): length of movies to display.

        Return:
            dataframe with movie name and score in descending order.
        """
        if not isinstance(length, int):
            return f"Enter a valid number."
            # check whether the input is valid integer
        return self.readcontent_fromcsv(
        ).sort_values(by=['IMDB Score'], ascending=False)[:length]

    def filter_movies(self, *args):
        """
        Filter movies with selected genre.
        User can selected one or more genre.

        Parameter:
            args (tuple): total genre to be selected from.

        Return:
            Dataframe containing args as a genre or empty dataframe.

        example: filter_movies('Thriller', 'Drama')
        """

        pattern = '|'.join(list(args))
        df = self.readcontent_fromcsv()
        return df[df['Genre'].str.contains(
            pattern, case=False, na=False)]

    def get_unique_genre(self):
        """
        Splits the value of Genre column with '|' delimiter and prints unique
        values.

        Return:
            List of unique strings.
        """
        df = self.readcontent_fromcsv()['Genre'].str.split('|')
        return df.explode('Genre').unique()

    def rate_movies(self, movie_id: int, new_rating: float):
        """
        Update the imdb Score of a specific movie.

        Parameter:
            movie_id (int): Specific id of a movie.
            new_rating (float:.2f): New rating specified by user.

        Return:
            Successful message or validation error.
        """
        if not isinstance(movie_id, int) and isinstance(new_rating, (float, int)):
            return 'Please enter valid data.'
        
        df = self.readcontent_fromcsv()
        try:
            selected_row_index = df.index[df['imdbId'] == movie_id][0]
        except IndexError as e:
            return f'Given id:{movie_id} does not exist. Warning: {e}'
        rounded_float = round(new_rating, 1)
        df.loc[selected_row_index, 'IMDB Score'] = rounded_float
        df.to_csv(self._path, index=False)
        return f'Value for id:{movie_id} updated to {rounded_float}.'
    
    def recommend_movie(self, *genre):
        """
        This function return 5 movie based upon selected genre.
        Also, return the highest rated movie of same genre.

        Parameter:
            genre (tuple): total genre to be selected from.

        Return:
            Dataframe containing 5 recommended movies.
            Highest rated movie among selected genre.

        example: recommend_movie('Thriller', 'Drama')
        """

        pattern = '|'.join(list(genre))
        df = self.readcontent_fromcsv(
        )[['imdbId', 'Title', 'IMDB Score', 'Genre']]

        filtered_frame = df[df['Genre'].str.contains(
            pattern, case=False, na=False)]

        if filtered_frame.empty:
            return "No movies found"

        highest_rated_movie = filtered_frame.sort_values(
            by=['IMDB Score'], ascending=False)

        # recommend movie based on genre
        print("Recommended movies are:")
        print(highest_rated_movie[:11].sample(frac=0.5))

        # highest score in that genre
        print("The highest movie among the selected genre are is:")
        print(highest_rated_movie[:1]['Title'])

    def chart_distribution(self):
        """
        Plot a area graph of movie index and its imdb score.
        """
        df = self.readcontent_fromcsv()["IMDB Score"]
        df.plot.area(figsize=(12, 4), subplots=True,
                     title="Rating Distribution")
        plt.xlabel("Index")
        plt.ylabel("Rating")
        plt.show()


ENCODINGS = 'charmap'
# change the encodings according to the requirements.

if __name__ == '__main__':
    # update the path to movies.csv file
    movie_object = MovieManager("./movies.csv", ENCODINGS)
    # movie_object.countdata_fromcsv()
    # movie_object.averagescore()
    # movie_object.display_highestrated_movies(length=5)
    # movie_object.filter_movies('Thriller', 'Drama')
    # movie_object.display_unique_genre()
    # movie_object.rate_movies(123123, 4)
    # movie_object.recommend_movie('Thriller', 'Drama')
    # movie_object.chart_distribution()
