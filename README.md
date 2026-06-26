# MovieSphere – Movie Recommendation System

## Overview

MovieSphere is a full-stack movie recommendation web application that helps users discover movies based on their interests using **content-based recommendation techniques**. The system analyzes movie metadata and recommends similar movies by applying **TF-IDF Vectorization** and **Cosine Similarity**. It provides a modern, responsive, and user-friendly interface for searching, exploring, discovering, and organizing movies.

---

## Features

* Secure user registration and login using JWT authentication
* Browse trending, popular, top-rated, and latest movies
* Search movies by title
* View detailed movie information
* Receive content-based movie recommendations
* View a **Suggested Movies** section on the Home page based on the selected movie
* Add and manage favorite movies
* Create and manage personalized movie playlists
* Add or remove movies from playlists
* View user profile and watch history
* Responsive and modern web interface
* Fast and accurate recommendation engine powered by Classical Machine Learning

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

1. The system loads movie data, including titles, genres, descriptions, and other metadata.
2. The dataset is cleaned and preprocessed using Pandas and NumPy.
3. Movie descriptions are converted into numerical feature vectors using TF-IDF Vectorization.
4. Cosine Similarity is used to calculate the similarity between movies.
5. When a user searches for or selects a movie, the recommendation engine identifies and returns the most similar movies.
6. Recommended movies are displayed in the **Suggested Movies** section on the Home page and on the Movie Details page.
7. Users can create custom playlists, organize their favorite movies, and manage their personal movie collections.
8. The Flask backend processes client requests, communicates with the database, and executes the recommendation engine.
9. The backend returns movie data and recommendations to the frontend through RESTful APIs.
10. Users can register, log in, manage favorites, create playlists, view watch history, and discover personalized movie recommendations through the MovieSphere web application.

---

## Project Highlights

* Full-stack web application with a RESTful Flask backend
* Content-based movie recommendation system using Classical Machine Learning
* Secure user authentication using JWT
* Personalized movie playlists and favorites management
* Suggested Movies section powered by a recommendation engine
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
8. Register a new account and start exploring, organizing, and discovering movies with **MovieSphere**.
