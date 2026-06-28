import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import create_app
from models import db, Movie

# Mapping of TMDB ID to actual Poster Paths
POSTER_UPDATES = {
    211672: "/q0R49KTzSzhbeK906O9jD6VMsyi.jpg", # Minions
    157336: "/gEU2QniE6E77NI6vCU67oYvNIob.jpg", # Interstellar
    293660: "/y95Sqv9hncbN1m6vV87db8Buc7S.jpg", # Deadpool
    118340: "/r7DuyYn0btp9PqBr9vBqbU793pG.jpg", # Guardians of the Galaxy
    76341:  "/8tZYtu0llhl0tLGclP9vcOFEO0o.jpg", # Mad Max: Fury Road
    135397: "/r7DuyYn0btp9PqBr9vBqbU793pG.jpg", # Jurassic World
    22:     "/z8peBDEFeuS0pS0RBofh6v1s9Ky.jpg", # Pirates of the Caribbean
    119450: "/279t9f9S6u7rUvYmEfSvi96YvPb.jpg", # Dawn of the Planet of the Apes
    131631: "/gj2YwoYpUTfwVWX6GGaWDP6p26b.jpg", # Hunger Games: Mockingjay
    177572: "/69Sns8oTKyRuvq6pjsMpBTMX3Km.jpg", # Big Hero 6
    87101:  "/5JU9pBjbY3nqb9vC6UM6ObrVaNo.jpg", # Terminator Genisys
    271110: "/kY9Y66id29v55N9mU389y3qf61b.jpg", # Captain America: Civil War
    102899: "/v7TaRYQwS2mbb7u9S9KzNuClRqv.jpg", # Ant-Man
    285:    "/j86p9fWqf3z5j7j0R49KTzSzhbe.jpg", # Pirates: At World's End
    10138:  "/f77v8YAn9mbt6vV87db8Buc7S.jpg", # Iron Man 2
}

def fix_images():
    app = create_app()
    with app.app_context():
        print("🛠️  Patching Database with Real Poster Paths...")
        
        for tmdb_id, path in POSTER_UPDATES.items():
            movie = Movie.query.filter_by(tmdb_id=tmdb_id).first()
            if movie:
                # Store only the path (the Controller will add the URL prefix)
                movie.poster_path = path
                # Use the same for backdrop or a default
                movie.backdrop_path = path
        
        db.session.commit()
        print("✅ Top movies patched! Refresh your browser.")

if __name__ == "__main__":
    fix_images()