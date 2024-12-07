import pandas as pd
import numpy as np

class RuleBasedFiltering:
    """
    A rule-based content filtering recommender system.

    This class recommends top-rated movies based on overall ratings or genre.
    """

    def __init__(self, ratings_file, metadata_file):
        """
        Initialize the rule-based recommender system.
        """
        self.ratings_file = ratings_file
        self.metadata_file = metadata_file
        self.ratings = None
        self.items_metadata = None
        self.top_movies = None
        self._load_data()
        self._compute_top_movies()

    def _load_data(self):
        """Load the ratings and item metadata datasets."""
        self.ratings = pd.read_csv(
            self.ratings_file,
            sep='\t',
            names=['user', 'item', 'rating', 'timestamp']
        )
        self.items_metadata = pd.read_csv(
            self.metadata_file,
            sep='|',
            encoding='latin-1',
            names=[
                'item', 'title', 'release_date', 'video_release_date',
                'IMDb_URL', 'unknown', 'Action', 'Adventure', 'Animation',
                'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
            ]
        )

        #add top genre for the movies
        self.ratings['gen'] = 'unknown'

        #add a new column with genre of the movie rated
        for i, row in self.ratings.iterrows():
            # Genre columns
            gen_cols = [
                'unknown', 'Action', 'Adventure', 'Animation',
                'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
                'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
                'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
            ]

            # Get the genres of the item
            rand_item = self.items_metadata[self.items_metadata['item'] == row['item']]
            gen_item = rand_item.iloc[0][gen_cols]
            gen_list = gen_item[gen_item == 1].index.to_list()
            if len(gen_list) > 0:
                gen = gen_list[0]
            else:
                gen = 'unknown'

            self.ratings.loc[i, 'gen'] = gen

    def _compute_top_movies(self):
        """Compute the top-rated movies overall."""
        avg_ratings = self.ratings.groupby('item')['rating'].mean()
        movie_counts = self.ratings.groupby('item')['rating'].count()

        # Only consider movies with a significant number of ratings
        popular_movies = avg_ratings[movie_counts >= 50]
        top_movies = popular_movies.sort_values(ascending=False)

        self.top_movies = self.items_metadata.set_index('item').loc[top_movies.index]
        self.top_movies['average_rating'] = top_movies.values

    def recommend_top_movies(self, n=10):
        """
        Recommends top movies.
        """
        return self.top_movies.head(n)

    def recommend_by_genre(self, genre, n=10):
        """
        Recommend the top-rated movies for a specific genre.

        """
        if genre not in self.items_metadata.columns:
            raise ValueError(f"Genre '{genre}' not found in metadata.")

        genre_movies = self.top_movies[self.top_movies[genre] == 1]
        return genre_movies.head(n)

    def _get_user_profile(self, user_id):
        """Create a user profile based on the user's past ratings."""
        user_ratings = self.ratings[self.ratings['user'] == user_id]
        return user_ratings
    
    def _predict(self, item_id):
        "Given the item ID checks the genre and then uses the global average rating as the predicted rating."
        
        # Genre columns
        gen_cols = [
            'unknown', 'Action', 'Adventure', 'Animation',
            'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
            'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
        ]

        # Get the genres of the item
        rand_item = self.items_metadata[self.items_metadata['item'] == item_id]
        gen_item = rand_item.iloc[0][gen_cols]
        gen_list = gen_item[gen_item == 1].index.to_list()
        if len(gen_list) > 0:
            gen = gen_list[0]
        else:
            gen = 'unknown'

        #find the item mean rating from the list
        predicted_rating = self.ratings[self.ratings['gen'] == gen]['rating'].mean()
    
        return predicted_rating
    


if __name__ == "__main__":
    recommender = RuleBasedFiltering(
        ratings_file='storage/u.data',
        metadata_file='storage/u.item'
    )

    import pdb; pdb.set_trace()