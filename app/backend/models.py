from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

# --- Many-to-Many Association Tables ---

user_genres = db.Table('user_genres',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete='CASCADE'), primary_key=True)
)

playlist_movies = db.Table('playlist_movies',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlists.id', ondelete='CASCADE'), primary_key=True),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), primary_key=True),
    db.Column('added_at', db.DateTime, default=datetime.utcnow)
)

# --- Models ---

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True, default='default_profile.png')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    preferred_genres = db.relationship('Genre', secondary=user_genres, backref='interested_users')
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade="all, delete-orphan")
    watch_later = db.relationship('WatchLater', backref='user', lazy=True, cascade="all, delete-orphan")
    watch_history = db.relationship('WatchHistory', backref='user', lazy=True, cascade="all, delete-orphan")
    playlists = db.relationship('Playlist', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    tmdb_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.String(50), nullable=True)
    poster_path = db.Column(db.String(255), nullable=True)
    backdrop_path = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=0.0)
    popularity = db.Column(db.Float, default=0.0)
    runtime = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(10), default='en')
    
    # Metadata for ML
    cast = db.Column(db.Text, nullable=True) # JSON string of top cast
    director = db.Column(db.String(100), nullable=True)
    production_company = db.Column(db.String(255), nullable=True)

    genres = db.relationship('Genre', secondary=movie_genres, backref='movies')

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    movie = db.relationship('Movie')

class WatchLater(db.Model):
    __tablename__ = 'watch_later'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    movie = db.relationship('Movie')

class WatchHistory(db.Model):
    __tablename__ = 'watch_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_rating = db.Column(db.Float, nullable=True)
    
    movie = db.relationship('Movie')

class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    movies = db.relationship('Movie', secondary=playlist_movies, backref='in_playlists')

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Float, nullable=False) # Relevance score
    reason = db.Column(db.String(100), nullable=True) # e.g., "Because you liked Inception"
    
    movie = db.relationship('Movie')