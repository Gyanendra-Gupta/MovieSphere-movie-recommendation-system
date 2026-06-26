# MovieSphere – Movie Recommendation System

## Overview

MovieSphere is a full-stack movie recommendation web application that helps users discover movies based on their interests using **content-based recommendation techniques**. The system analyzes movie metadata and recommends similar movies by applying **TF-IDF Vectorization** and **Cosine Similarity**. It provides a modern, responsive, and user-friendly platform for searching, exploring, discovering, and organizing movies.

---
## Pages

* Home
* Login
* Register
* Search Movies
* Movie Details
* Favorites
* Playlists
* Watch Later
* Watch History
* User Profile
* 404 Page

---

## Features

### Authentication

* Secure user registration and login using JWT Authentication
* Password hashing and protected routes
* User logout and session management

### User Registration

Users can register with:

* Full Name
* Username
* Email Address
* Password
* Profile Picture (Optional)
* Date of Birth (Optional)
* Preferred Movie Genres

### Supported Genres

* Action
* Adventure
* Animation
* Comedy
* Crime
* Documentary
* Drama
* Family
* Fantasy
* Horror
* Mystery
* Romance
* Sci-Fi
* Thriller

Selected genres are stored in the database and used to generate personalized movie recommendations.

---

## Home Page

* Hero Banner
* Trending Movies
* Popular Movies
* Top Rated Movies
* Latest Releases
* Suggested Movies
* Top Picks For You
* Movies Based on User Interests
* Continue Watching
* Recently Viewed Movies
* Browse Movies by Genre

---

## Search

* Search movies by title
* Instant search suggestions
* Filter by genre
* Filter by language
* Filter by release year
* Filter by IMDb rating
* Sort by popularity
* Sort by latest release

---

## Movie Details

Display:

* Movie Poster
* Movie Title
* Genre
* Overview
* Release Date
* Runtime
* IMDb Rating
* Cast
* Director
* Similar Movie Recommendations
* Add to Favorites
* Add to Playlist
* Add to Watch Later
* Mark as Watched

---

## Favorites

* View favorite movies
* Add movies to favorites
* Remove movies from favorites
* Search favorite movies

---

## My Playlists

Users can:

* Create custom playlists
* Rename playlists
* Delete playlists
* Add movies to playlists
* Remove movies from playlists
* View playlist details

Example playlists:

* Weekend Movies
* Watch Later
* Action Collection
* Comedy Collection
* Sci-Fi Favorites

---

## Watch Later

* Save movies to watch later
* Remove movies from the watch later list
* Move movies from Watch Later to Favorites or Playlists

---

## Watch History

* View recently watched movies
* Track watched movies
* Continue watching list
* Clear watch history

---

## User Profile

Display:

* Profile Picture
* Full Name
* Username
* Email Address
* Preferred Genres
* Favorite Movies
* Created Playlists
* Watch Later List
* Watch History
* Account Creation Date
* Total Favorite Movies
* Total Playlists
* Total Movies Watched

Users can:

* Edit Profile
* Update Profile Picture
* Update Preferred Genres
* Change Password

---

## Technologies Used

### Frontend

* HTML5
* Tailwind CSS
* JavaScript

### Backend

* Python
* Flask
* Flask SQLAlchemy
* Flask-JWT-Extended
* Flask-CORS

### Database

* SQLite (Development)
* PostgreSQL (Production)

### Machine Learning

* Pandas
* NumPy
* Scikit-learn
* TF-IDF Vectorization
* Cosine Similarity

---

## How It Works

1. The application loads movie data, including movie titles, genres, descriptions, keywords, cast, and other metadata.
2. The dataset is cleaned and preprocessed using Pandas and NumPy.
3. Movie descriptions and metadata are transformed into numerical feature vectors using TF-IDF Vectorization.
4. Cosine Similarity is used to calculate similarity scores between movies.
5. When a user searches for or selects a movie, the recommendation engine returns the most similar movies.
6. During registration, users select their preferred movie genres, which are stored in the database.
7. Personalized recommendations are generated using the user's preferred genres, favorite movies, and recently viewed movies.
8. Users can create playlists, manage favorites, save movies to Watch Later, and maintain their watch history.
9. The Flask backend processes client requests, communicates with the database, and executes the recommendation engine.
10. RESTful APIs deliver movie information and recommendations to the frontend.

---

## Project Highlights

* Full-stack web application with a RESTful Flask backend
* Content-based recommendation system using Classical Machine Learning
* Secure JWT-based authentication and authorization
* Personalized recommendations based on user preferences
* Suggested Movies and Top Picks For You sections
* Favorites, Watch Later, and custom playlist management
* User profile with watch history and personalized statistics
* Responsive design optimized for desktop and mobile devices
* Modular, scalable, and maintainable project architecture
* Clean, reusable, and well-structured code following software development best practices

---

## Getting Started

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the required backend dependencies.
4. Configure the database.
5. Train the recommendation model and generate the required `.pkl` files.
6. Start the Flask backend server.
7. Launch the frontend application.
8. Register a new account and select your preferred movie genres.
9. Log in to explore movies, receive personalized recommendations, manage favorites, create playlists, save movies to Watch Later, and enjoy the complete MovieSphere experience.
