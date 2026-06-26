# MovieSphere – Movie Recommendation System

## Overview

MovieSphere is a full-stack movie recommendation web application that helps users discover movies using **Content-Based Recommendation** techniques. It recommends similar movies by applying **TF-IDF Vectorization** and **Cosine Similarity** to movie metadata. The application provides a responsive interface for searching, exploring, and managing personalized movie collections.

---

## Pages

* Home
* Login & Register
* Movie Details
* User Dashboard (Profile, Favorites, Playlists, Watch Later, Watch History)
* 404 Page

---

## Features

* Secure user authentication using JWT
* User registration with preferred movie genres
* Search movies by title
* Browse trending, popular, top-rated, and latest movies
* Content-based movie recommendations
* Suggested Movies and Top Picks sections
* Favorite movies management
* Custom playlist creation and management
* Watch Later and Watch History
* User profile management
* Responsive and user-friendly interface

---

## Supported Genres

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

1. Load and preprocess movie metadata from the TMDB dataset.
2. Clean and transform the dataset using Pandas and NumPy.
3. Generate feature vectors using TF-IDF Vectorization.
4. Calculate movie similarity with Cosine Similarity.
5. Store user information, preferences, favorites, playlists, and watch history in the database.
6. Generate personalized movie recommendations based on selected movies and preferred genres.
7. Serve movie data and recommendations through RESTful Flask APIs.

---

## Project Highlights

* Full-stack web application with Flask REST APIs
* Content-based recommendation engine using Classical Machine Learning
* Secure JWT-based authentication
* Personalized recommendations based on user interests
* Favorites, Playlists, Watch Later, and Watch History
* Responsive design for desktop and mobile devices
* Modular and scalable project architecture

---

## Getting Started

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required dependencies.
4. Configure the database.
5. Train the recommendation model and generate the `.pkl` files.
6. Start the Flask backend server.
7. Launch the frontend application.
8. Register an account, select your preferred genres, and start exploring personalized movie recommendations.
