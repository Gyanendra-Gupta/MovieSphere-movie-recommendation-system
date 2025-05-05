# Movie Recommendation System (Tkinter GUI)

This project is a simple content-based movie recommendation system built with Python. It uses a graphical user interface (GUI) made with Tkinter and recommends movies based on their descriptions using TF-IDF and cosine similarity.

## Features

- Select a movie from a dropdown menu
- Get top 5 content-based movie recommendations
- View recommendations as text and bar chart
- Compare total watch counts of all movies with a bar chart
- Simple, interactive GUI using Tkinter
- Visualizations with Matplotlib

## Technologies Used

- Python
- pandas
- scikit-learn (TF-IDF and cosine similarity)
- Matplotlib
- Tkinter

## How It Works

1. The program loads a set of movies with their descriptions and watch counts.
2. When a user selects a movie, TF-IDF vectorization is used to compare the description to others.
3. Cosine similarity determines the top 5 most similar movies.
4. Results are shown as a list and a horizontal bar chart.
5. Users can also view a bar chart of watch counts for all movies.

## Getting Started

1. Clone this repository:
