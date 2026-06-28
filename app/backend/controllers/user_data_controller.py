from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from models import (
    db,
    Favorite,
    WatchHistory,
    WatchLater,
    Playlist,
    Movie
)
from controllers.movie_controller import MovieController

class UserDataController:

    # --- FAVORITES LOGIC ---
    @staticmethod
    @jwt_required()
    def toggle_favorite():
        user_id = get_jwt_identity()
        data = request.get_json()
        movie_id = data.get("movie_id")

        if not movie_id:
            return jsonify({"error": "movie_id is required"}), 400

        movie = Movie.query.filter_by(tmdb_id=movie_id).first_or_404()
        favorite = Favorite.query.filter_by(user_id=user_id, movie_id=movie.id).first()

        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({"message": "Removed from favorites", "status": "removed"}), 200

        new_fav = Favorite(user_id=user_id, movie_id=movie.id)
        db.session.add(new_fav)
        db.session.commit()
        return jsonify({"message": "Added to favorites", "status": "added"}), 201

    @staticmethod
    @jwt_required()
    def get_favorites():
        user_id = get_jwt_identity()
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        movies = [MovieController._format_movie(f.movie) for f in favorites]
        return jsonify(movies), 200

    # --- WATCH LATER LOGIC ---
    @staticmethod
    @jwt_required()
    def toggle_watch_later():
        user_id = get_jwt_identity()
        data = request.get_json()
        movie_id = data.get("movie_id")

        if not movie_id:
            return jsonify({"error": "movie_id is required"}), 400

        movie = Movie.query.filter_by(tmdb_id=movie_id).first_or_404()
        entry = WatchLater.query.filter_by(user_id=user_id, movie_id=movie.id).first()

        if entry:
            db.session.delete(entry)
            db.session.commit()
            return jsonify({"message": "Removed from Watch Later", "status": "removed"}), 200

        new_entry = WatchLater(user_id=user_id, movie_id=movie.id)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "Added to Watch Later", "status": "added"}), 201

    @staticmethod
    @jwt_required()
    def get_watch_later():
        user_id = get_jwt_identity()
        entries = WatchLater.query.filter_by(user_id=user_id).all()
        movies = [MovieController._format_movie(e.movie) for e in entries]
        return jsonify(movies), 200

    # --- WATCH HISTORY LOGIC ---
    @staticmethod
    @jwt_required()
    def add_to_history():
        user_id = get_jwt_identity()
        data = request.get_json()
        movie_id = data.get("movie_id")

        if not movie_id:
            return jsonify({"error": "movie_id is required"}), 400

        movie = Movie.query.filter_by(tmdb_id=movie_id).first_or_404()

        # Update if exists today or add new
        history = WatchHistory(
            user_id=user_id,
            movie_id=movie.id,
            user_rating=data.get("rating"),
            watched_at=datetime.utcnow()
        )

        db.session.add(history)
        db.session.commit()
        return jsonify({"message": "Added to watch history"}), 201

    @staticmethod
    @jwt_required()
    def get_history():
        user_id = get_jwt_identity()
        history = WatchHistory.query.filter_by(user_id=user_id).order_by(WatchHistory.watched_at.desc()).all()

        return jsonify([{
            "id": h.id,
            "watched_at": h.watched_at.isoformat(),
            "user_rating": h.user_rating,
            "movie": MovieController._format_movie(h.movie)
        } for h in history]), 200

    @staticmethod
    @jwt_required()
    def delete_history_item(history_id):
        user_id = get_jwt_identity()
        item = WatchHistory.query.filter_by(id=history_id, user_id=user_id).first_or_404()
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "History item removed"}), 200

    # --- PLAYLIST LOGIC ---
    @staticmethod
    @jwt_required()
    def manage_playlists(playlist_id=None):
        user_id = get_jwt_identity()

        if request.method == "GET":
            playlists = Playlist.query.filter_by(user_id=user_id).all()
            return jsonify([{
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "movies": [MovieController._format_movie(m) for m in p.movies]
            } for p in playlists]), 200

        elif request.method == "POST":
            data = request.get_json()
            if not data.get("name"):
                return jsonify({"error": "Playlist name is required"}), 400

            playlist = Playlist(name=data["name"], description=data.get("description"), user_id=user_id)
            db.session.add(playlist)
            db.session.commit()
            return jsonify({"message": "Playlist created", "playlist_id": playlist.id}), 201

        elif request.method == "PUT":
            data = request.get_json()
            playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first_or_404()
            if data.get("name"): playlist.name = data["name"]
            if data.get("description"): playlist.description = data["description"]
            db.session.commit()
            return jsonify({"message": "Playlist updated"}), 200

        elif request.method == "DELETE":
            playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first_or_404()
            db.session.delete(playlist)
            db.session.commit()
            return jsonify({"message": "Playlist deleted"}), 200

    @staticmethod
    @jwt_required()
    def add_movie_to_playlist(playlist_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        movie_id = data.get("movie_id")

        playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first_or_404()
        movie = Movie.query.filter_by(tmdb_id=movie_id).first_or_404()

        if movie not in playlist.movies:
            playlist.movies.append(movie)
            db.session.commit()
            return jsonify({"message": "Movie added to playlist"}), 200
        
        return jsonify({"message": "Movie already in playlist"}), 200

    @staticmethod
    @jwt_required()
    def remove_movie_from_playlist(playlist_id, movie_id):
        user_id = get_jwt_identity()
        playlist = Playlist.query.filter_by(id=playlist_id, user_id=user_id).first_or_404()
        movie = Movie.query.filter_by(tmdb_id=movie_id).first_or_404()

        if movie in playlist.movies:
            playlist.movies.remove(movie)
            db.session.commit()
            return jsonify({"message": "Movie removed from playlist"}), 200
        
        return jsonify({"error": "Movie not in playlist"}), 404