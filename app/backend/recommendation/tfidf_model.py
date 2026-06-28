import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import os

class MovieRecommender:
    def __init__(self):
        # This locates the folder where tfidf_model.py lives
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
        
        # This points to backend/dataset/
        dataset_folder = os.path.join(base_dir, '..', 'dataset')
        
        self.dataset_path = os.path.join(dataset_folder, 'tmdb_5000_movies.csv')
        self.credits_path = os.path.join(dataset_folder, 'tmdb_5000_credits.csv')
        
        self.df = None
        self.cosine_sim = None
        self.indices = None
        self._initialize_engine()
    def _initialize_engine(self):
        """Complete pipeline: Load, Clean, Engineer, and Compute."""
        try:
            # 1. Load Datasets
            movies = pd.read_csv(self.dataset_path)
            credits = pd.read_csv(self.credits_path)

            # 2. Merge on ID
            credits.columns = ['id', 'tittle', 'cast', 'crew']
            self.df = movies.merge(credits, on='id')

            # 3. Clean and Parse JSON columns
            features = ['cast', 'crew', 'keywords', 'genres']
            for feature in features:
                self.df[feature] = self.df[feature].apply(self._safe_parse)

            # 4. Extract Key Metadata
            self.df['director'] = self.df['crew'].apply(self._get_director)
            self.df['cast'] = self.df['cast'].apply(self._get_list)
            self.df['keywords'] = self.df['keywords'].apply(self._get_list)
            self.df['genres'] = self.df['genres'].apply(self._get_list)

            # 5. Data Cleaning: Strip spaces and lowercase
            for feature in ['cast', 'director', 'keywords', 'genres']:
                self.df[feature] = self.df[feature].apply(self._clean_data)

            # 6. Feature Engineering: Create the "Metadata Soup"
            self.df['soup'] = self.df.apply(self._create_soup, axis=1)

            # 7. Vectorization
            tfidf = TfidfVectorizer(stop_words='english')
            tfidf_matrix = tfidf.fit_transform(self.df['soup'])

            # 8. Compute Cosine Similarity Matrix
            # linear_kernel is faster than cosine_similarity for TF-IDF
            self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            # 9. Construct reverse mapping of indices and titles
            self.df = self.df.reset_index()
            self.indices = pd.Series(self.df.index, index=self.df['id']).drop_duplicates()

        except Exception as e:
            print(f"Error initializing Recommendation Engine: {e}")

    def _safe_parse(self, x):
        try:
            return json.loads(x)
        except (TypeError, ValueError):
            return []

    def _get_director(self, x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan

    def _get_list(self, x):
        if isinstance(x, list):
            names = [i['name'] for i in x]
            # Check if more than 3 elements exist. If yes, return only first three.
            if len(names) > 3:
                names = names[:3]
            return names
        return []

    def _clean_data(self, x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    def _create_soup(self, x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + \
               x['director'] + ' ' + ' '.join(x['genres']) + ' ' + str(x['overview'])

    def get_recommendations(self, movie_id, user_preferred_genres=None, watch_history=None):
        """
        Main recommendation function.
        Factors:
        - Content Similarity (Primary)
        - Genre Boosting (Personalization)
        - History Awareness (Filtering)
        """
        if self.cosine_sim is None or movie_id not in self.indices:
            return []

        # Get index of the movie that matches the movie_id
        idx = self.indices[movie_id]

        # Get the pairwise similarity scores of all movies with that movie
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # Personalization: Boost scores based on user preferences
        if user_preferred_genres:
            cleaned_prefs = [g.lower().replace(" ", "") for g in user_preferred_genres]
            for i, score in sim_scores:
                movie_genres = self.df.iloc[i]['genres']
                # Increase similarity score by 15% if genres match user preferences
                if any(genre in cleaned_prefs for genre in movie_genres):
                    sim_scores[i] = (i, score * 1.15)

        # Sort the movies based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Filter out movies already in watch history
        if watch_history:
            sim_scores = [x for x in sim_scores if self.df.iloc[x[0]]['id'] not in watch_history]

        # Get the scores of the 10 most similar movies (excluding itself)
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies from the dataframe
        return self.df[['id', 'title', 'poster_path', 'vote_average', 'release_date']].iloc[movie_indices].to_dict('records')

    def recommend_by_profile(self, user_preferred_genres, watch_history=None, top_n=10):
        """
        Cold-start / Dashboard recommendation when no specific movie is being viewed.
        Calculates similarity based on user's preferred genres.
        """
        if not user_preferred_genres:
            # Fallback to top rated if no preferences
            return self.df.sort_values('vote_average', ascending=False).head(top_n).to_dict('records')

        cleaned_prefs = " ".join([g.lower().replace(" ", "") for g in user_preferred_genres])
        
        # Temporary TF-IDF vector for the user's preference "soup"
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.df['soup'])
        user_vec = tfidf.transform([cleaned_prefs])
        
        # Calculate similarity between user profile and all movies
        prof_sim = linear_kernel(user_vec, tfidf_matrix).flatten()
        
        sim_scores = list(enumerate(prof_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        if watch_history:
            sim_scores = [x for x in sim_scores if self.df.iloc[x[0]]['id'] not in watch_history]
            
        movie_indices = [i[0] for i in sim_scores[:top_n]]
        return self.df[['id', 'title', 'poster_path', 'vote_average', 'release_date']].iloc[movie_indices].to_dict('records')

# Singleton instance to be used by Flask routes
recommender = MovieRecommender()