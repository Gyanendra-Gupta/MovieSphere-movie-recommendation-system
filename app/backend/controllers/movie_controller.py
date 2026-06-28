from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Movie, Genre, User
from recommendation.tfidf_model import recommender

class MovieController:

    @staticmethod
    def get_all_movies():
        """Returns a paginated list of all movies."""
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=20, type=int)

        movies = Movie.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        return jsonify({
            "movies": [MovieController._format_movie(m) for m in movies.items],
            "total": movies.total,
            "pages": movies.pages,
            "current_page": movies.page
        }), 200

    @staticmethod
    def get_trending():
        """Returns the top 20 movies based on popularity."""
        movies = Movie.query.order_by(Movie.popularity.desc()).limit(20).all()
        return jsonify([MovieController._format_movie(m) for m in movies]), 200

    @staticmethod
    def get_top_rated():
        """Returns the top 20 movies based on rating."""
        movies = Movie.query.order_by(Movie.rating.desc()).limit(20).all()
        return jsonify([MovieController._format_movie(m) for m in movies]), 200

    @staticmethod
    def get_by_id(movie_id):
        """Returns full details for a specific movie by its TMDB ID."""
        movie = Movie.query.filter_by(tmdb_id=movie_id).first_or_404()
        return jsonify(MovieController._format_movie(movie, full_details=True)), 200

    @staticmethod
    def search():
        """Dynamic search by title and/or genre."""
        query = request.args.get("q", "").strip()
        genre_name = request.args.get("genre", "").strip()

        movie_query = Movie.query
        if query:
            movie_query = movie_query.filter(Movie.title.ilike(f"%{query}%"))
        if genre_name:
            movie_query = movie_query.join(Movie.genres).filter(Genre.name.ilike(f"%{genre_name}%"))

        movies = movie_query.limit(50).all()
        return jsonify([MovieController._format_movie(m) for m in movies]), 200

    @staticmethod
    @jwt_required(optional=True)
    def get_recommendations(movie_id):
        """Fetches ML-based recommendations, personalized if user is logged in."""
        user_id = get_jwt_identity()
        preferred_genres = None
        watch_history = []

        if user_id:
            user = User.query.get(user_id)
            if user:
                preferred_genres = [g.name for g in user.preferred_genres]
                watch_history = [h.movie.tmdb_id for h in user.watch_history]

        # Call the ML Engine
        recommendations = recommender.get_recommendations(
            movie_id=int(movie_id),
            user_preferred_genres=preferred_genres,
            watch_history=watch_history
        )
        return jsonify(recommendations), 200

    @staticmethod
    def _format_movie(movie, full_details=False):
        """
        Internal helper to format database objects into JSON.
        Includes TMDB Image CDN logic and reliable fallbacks.
        """
        POSTER_BASE = "https://image.tmdb.org/t/p/w500"
        BACKDROP_BASE = "https://image.tmdb.org/t/p/original"
        PLACEHOLDER = "https://placehold.co/500x750/1a1a1a/ffffff?text="

        # Logic to handle TMDB Paths vs Fallbacks
        poster = movie.poster_path
        if poster and poster.startswith('/'):
            poster = f"{POSTER_BASE}{poster}"
        elif not poster or not poster.startswith('http'):
            poster = f"{PLACEHOLDER}{movie.title.replace(' ', '+')}"

        backdrop = movie.backdrop_path
        if backdrop and backdrop.startswith('/'):
            backdrop = f"{BACKDROP_BASE}{backdrop}"
        else:
            backdrop = poster # Fallback backdrop to poster if missing

        data = {
            "id": movie.tmdb_id,
            "tmdb_id": movie.tmdb_id,
            "title": movie.title or "Unknown Title",
            "overview": movie.overview or "No description available for this title.",
            "poster_path": poster,
            "backdrop_path": backdrop,
            "rating": round(movie.rating, 1) if movie.rating else 0.0,
            "release_date": movie.release_date or "N/A",
            "genres": [g.name for g in movie.genres]
        }

        if full_details:
            data.update({
                "runtime": movie.runtime or 0,
                "popularity": movie.popularity or 0.0,
                "language": movie.language or "en",
                "director": movie.director or "Information Unavailable",
                "cast": movie.cast or "[]", # Expected as JSON string from seed_db
                "production": movie.production_company or "N/A"
            })

        return data