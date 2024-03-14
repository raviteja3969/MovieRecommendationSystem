import boto3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('movie_database')

# Function to fetch data from DynamoDB
def fetch_data_from_db():
    response = table.scan()
    return response['Items']

# Fetch movie data from DynamoDB
data = fetch_data_from_db()

# Extract features
titles = [movie['title'] for movie in data]
genres = [movie['genre'] for movie in data]
#synopses = [movie['synopsis'] for movie in data]
ratings = [movie['rating'] for movie in data]

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

recommendations = get_recommendations("Baahubali: The Beginning")
print("Recommendations for 'Baahubali: The Beginning ':")
for movie in recommendations:
    print("-", movie)
