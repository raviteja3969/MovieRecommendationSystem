import boto3
import requests

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = 'movie_database'
table = dynamodb.Table(table_name)

# Function to insert movie data into DynamoDB
def insert_movie(title, genre, synopsis, rating):
    try:
        table.put_item(
            Item={
                'title': title,
                'genre': genre,
                'synopsis': synopsis,
                'rating': str(rating)
            },
            ConditionExpression="attribute_not_exists(title)"  # Avoid duplicates
        )
    except dynamodb.meta.client.exceptions.ConditionalCheckFailedException:
        print(f"Movie '{title}' already exists in the database. Skipping...")
# Function to fetch data from the API and add it to the database
def fetch_and_add_movies():
    url = "https://ott-detail`s.p.rapidapi.com/advancedsearch"
    querystring = {
        "start_year": "1970",
        "end_year": "2020",
        "min_imdb": "6",
        "max_imdb": "7.8",
        "genre": "action",
        "language": "english",
        "type": "movie",
        "sort": "latest",
        "page": "1"
    }
    headers = {
        "X-RapidAPI-Key": "7077f1bf90msh5d75774364e0c6fp1b6e1djsn75b289be8e57",
        "X-RapidAPI-Host": "ott-details.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()
    for movie in data.get('results', []):
        title = movie.get('title', '')
        genre = ', '.join(movie.get('genre', []))
        synopsis = movie.get('synopsis', '')
        rating = float(movie.get('imdbrating', 0))
        insert_movie(title, genre, synopsis, rating)

# Example usage to fetch data from the API and add it to the database
fetch_and_add_movies()
