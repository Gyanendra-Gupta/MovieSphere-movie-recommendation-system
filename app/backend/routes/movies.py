# routes/movies.py
from flask import Blueprint
from controllers.movie_controller import MovieController

movies_bp = Blueprint('movies', __name__)

movies_bp.route('/', methods=['GET'])(MovieController.get_all_movies)
movies_bp.route('/trending', methods=['GET'])(MovieController.get_trending)
movies_bp.route('/top-rated', methods=['GET'])(MovieController.get_top_rated)
movies_bp.route('/search', methods=['GET'])(MovieController.search)
movies_bp.route('/<int:movie_id>', methods=['GET'])(MovieController.get_by_id)
movies_bp.route('/recommend/<int:movie_id>', methods=['GET'])(MovieController.get_recommendations)