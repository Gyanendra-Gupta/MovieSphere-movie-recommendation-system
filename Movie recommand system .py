#  This Python program builds a movie recommendation system with a Tkinter GUI. It suggests the top 5 similar movies based on descriptions using TF-IDF
#  and cosine similarity, and displays results in text and charts using Matplotlib. Users can also compare movie watch counts visually.

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

data = {
    'title': [
        'The Matrix', 'John Wick', 'The Notebook', 'Avengers: Endgame',
        'Inception', 'Interstellar', 'The Dark Knight', 'Titanic',
        '3 Idiots', 'Dangal', 'Dilwale Dulhania Le Jayenge', 'Zindagi Na Milegi Dobara',
        'Gully Boy', 'PK'
    ],
    'description': [
        'A hacker discovers reality is a simulation and joins a rebellion.',
        'An ex-hitman seeks vengeance against those who wronged him.',
        'A romantic drama about a couple who fall in love in the 1940s.',
        'Superheroes unite to undo the damage caused by Thanos.',
        'A thief enters people’s dreams to steal their secrets.',
        'Astronauts search for a new home as Earth becomes uninhabitable.',
        'Batman faces the Joker in a battle for Gotham’s soul.',
        'A love story set during the sinking of the Titanic.',
        'Three engineering students challenge the Indian education system.',
        'A former wrestler trains his daughters to become world-class champions.',
        'Two young lovers must overcome family opposition to be together.',
        'Three friends rediscover themselves on a life-changing road trip in Spain.',
        'A street rapper rises from the slums of Mumbai to become a sensation.',
        'An alien on Earth questions religious dogma and societal norms.'
    ],
    'watch_count': [120, 90, 75, 200, 160, 145, 180, 195, 210, 180, 140, 135, 125, 165]
}

df = pd.DataFrame(data)

vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df['description'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_recommendations(title, cosine_sim=cosine_sim):
    if title not in df['title'].values:
        return pd.DataFrame()
    idx = df[df['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]
    recommended = df.iloc[movie_indices][['title', 'description']].copy()
    recommended['similarity'] = scores
    return recommended

def plot_recommendations(title, recommendations):
    titles = recommendations['title']
    scores = recommendations['similarity']
    plt.figure(figsize=(8, 4))
    plt.barh(titles, scores, color='skyblue')
    plt.xlabel("Similarity Score")
    plt.title(f"Top 5 Recommendations for '{title}'")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def plot_watch_counts():
    plt.figure(figsize=(10, 6))
    plt.bar(df['title'], df['watch_count'], color='lightgreen')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Watch Count")
    plt.title("Most Watched Movies Comparison")
    plt.tight_layout()
    plt.show()

def show_recommendations():
    selected_title = title_var.get()
    recommendations = get_recommendations(selected_title)

    text_box.delete("1.0", tk.END)

    if recommendations.empty:
        text_box.insert(tk.END, "No recommendations found.")
    else:
        for _, row in recommendations.iterrows():
            text_box.insert(tk.END, f"{row['title']} (Similarity: {row['similarity']:.2f}):\n{row['description']}\n\n")
        plot_recommendations(selected_title, recommendations)

root = tk.Tk()
root.title("Movie Recommendation System")
root.geometry("750x650")
root.resizable(False, False)

title_var = tk.StringVar()

ttk.Label(root, text="Select a Movie:", font=("Helvetica", 13)).pack(pady=10)
movie_dropdown = ttk.Combobox(root, textvariable=title_var, values=sorted(df['title'].tolist()), width=60)
movie_dropdown.pack(pady=5)

ttk.Button(root, text="Get Recommendations", command=show_recommendations).pack(pady=10)
ttk.Button(root, text="Compare Watch Counts", command=plot_watch_counts).pack(pady=5)

text_box = tk.Text(root, height=25, width=85, wrap='word')
text_box.pack(padx=10, pady=10)

root.mainloop()
