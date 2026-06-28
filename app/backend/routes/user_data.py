from flask import Blueprint, request
from controllers.user_data_controller import UserDataController

user_data_bp = Blueprint('user_data', __name__)

# --- Favorites ---
@user_data_bp.route('/favorites', methods=['POST'])
def toggle_fav():
    return UserDataController.toggle_favorite()

@user_data_bp.route('/favorites/list', methods=['GET'])
def list_favs():
    return UserDataController.get_favorites()


# --- Watch Later ---
@user_data_bp.route('/watchlater', methods=['POST'])
def toggle_wl():
    return UserDataController.toggle_watch_later()

@user_data_bp.route('/watchlater/list', methods=['GET'])
def list_wl():
    return UserDataController.get_watch_later()


# --- Watch History ---
@user_data_bp.route('/history', methods=['GET', 'POST'])
def handle_history():
    if request.method == 'POST':
        return UserDataController.add_to_history()
    return UserDataController.get_history()

@user_data_bp.route('/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    return UserDataController.delete_history_item(history_id)


# --- Playlists ---
@user_data_bp.route('/playlists', methods=['GET', 'POST'])
def handle_playlists_root():
    """Handles viewing all playlists and creating a new one"""
    return UserDataController.manage_playlists()

@user_data_bp.route('/playlists/<int:playlist_id>', methods=['PUT', 'DELETE'])
def handle_playlist_ops(playlist_id):
    """Handles updating playlist metadata or deleting the playlist"""
    return UserDataController.manage_playlists(playlist_id)

@user_data_bp.route('/playlists/<int:playlist_id>/movie', methods=['POST'])
def add_movie_to_pl(playlist_id):
    """Adds a movie to a specific playlist"""
    return UserDataController.add_movie_to_playlist(playlist_id)

@user_data_bp.route('/playlists/<int:playlist_id>/movie/<int:movie_id>', methods=['DELETE'])
def remove_movie_from_pl(playlist_id, movie_id):
    """Removes a specific movie from a playlist"""
    return UserDataController.remove_movie_from_playlist(playlist_id, movie_id)