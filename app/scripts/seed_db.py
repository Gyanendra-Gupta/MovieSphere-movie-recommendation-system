import pandas as pd
import json
import sys
import os

# Add the backend directory to the path for imports
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(base_dir, '..', 'backend'))

from app import create_app
from models import db, Movie, Genre

def get_director(crew_str):
    crew = json.loads(crew_str)
    for member in crew:
        if member['job'] == 'Director':
            return member['name']
    return "Unknown"

def get_cast(cast_str):
    cast = json.loads(cast_str)
    # Return top 5 cast members as a string for the DB
    cast_names = [member['name'] for member in cast[:5]]
    return json.dumps(cast_names)

def seed_database():
    app = create_app()
    with app.app_context():
        print("🚀 Starting Production Database Seed...")
        db.create_all()

        # Resolve paths dynamically
        movies_path = os.path.join(base_dir, '..', 'backend', 'dataset', 'tmdb_5000_movies.csv')
        credits_path = os.path.join(base_dir, '..', 'backend', 'dataset', 'tmdb_5000_credits.csv')

        try:
            df_movies = pd.read_csv(movies_path)
            df_credits = pd.read_csv(credits_path)
        except Exception as e:
            print(f"❌ Error loading CSVs: {e}")
            return

        # Merge datasets to get cast/crew
        df = df_movies.merge(df_credits, left_on='id', right_on='movie_id')

        # 1. Seed Genres
        print("🎨 Seeding Genres...")
        genre_map = {}
        for _, row in df.iterrows():
            genres = json.loads(row['genres'])
            for g in genres:
                if g['name'] not in genre_map:
                    genre = Genre.query.filter_by(name=g['name']).first()
                    if not genre:
                        genre = Genre(name=g['name'])
                        db.session.add(genre)
                        db.session.commit()
                    genre_map[g['name']] = genre

        # 2. Seed Movies
        print(f"🎬 Seeding {len(df)} Movies (This may take a minute)...")
        for index, row in df.iterrows():
            if Movie.query.filter_by(tmdb_id=row['id']).first():
                continue

            # Generate simulated poster/backdrop since the CSV lacks them
            # In a real app, you'd fetch these from the TMDB API using the ID
            poster = f"https://image.tmdb.org/t/p/w500/or06vSneywvPiA3z9qZ2ThpzdvX.jpg" # Fallback
            backdrop = f"https://image.tmdb.org/t/p/original/6EL63j6aqovWDQH3uR87le9Zky3.jpg"

            new_movie = Movie(
                tmdb_id=int(row['id']),
                title=row['title_x'],
                overview=row['overview'] if pd.notna(row['overview']) else "",
                release_date=row['release_date'] if pd.notna(row['release_date']) else "Unknown",
                poster_path=poster, 
                backdrop_path=backdrop,
                rating=float(row['vote_average']),
                popularity=float(row['popularity']),
                runtime=int(row['runtime']) if pd.notna(row['runtime']) else 0,
                language=row['original_language'],
                director=get_director(row['crew']),
                cast=get_cast(row['cast']),
                production_company="Various"
            )

            # Link Genres
            movie_genres = json.loads(row['genres'])
            for g in movie_genres:
                new_movie.genres.append(genre_map[g['name']])

            db.session.add(new_movie)
            
            if index % 200 == 0:
                db.session.commit()
                print(f"✅ Processed {index} movies...")

        db.session.commit()
        print("🎉 Database Seeded Successfully!")

if __name__ == "__main__":
    seed_database()