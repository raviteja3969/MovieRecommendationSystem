import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Connect to the SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Function to fetch data from the SQLite database
def fetch_data_from_db():
    c.execute("SELECT * FROM movies")
    return c.fetchall()

# Fetch movie data from the database
data = fetch_data_from_db()

# Extract features
titles = [movie[1] for movie in data]  # Assuming title is in the second column
genres = [movie[2] for movie in data]  # Assuming genre is in the third column
synopses = [movie[3] for movie in data]  # Assuming synopsis is in the fourth column
ratings = [movie[4] for movie in data]  # Assuming rating is in the fifth column

print(titles)
# Vectorize features
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(genres)

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get recommendations based on title
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = titles.index(title)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Exclude the movie itself and get top 5 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return [titles[i] for i in movie_indices]

# Example usage
recommendations = get_recommendations("Mortal Kombat Legends: Scorpion's Revenge")
print("Recommendations for 'Mortal Kombat Legends: Scorpion's Revenge':")
for movie in recommendations:
    print("-", movie)

# Close the database connection
conn.close()
