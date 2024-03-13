import sqlite3
import requests

# Create or connect to the SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Create a table to store movies if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS movies 
             (id INTEGER PRIMARY KEY, title TEXT UNIQUE, genre TEXT, synopsis TEXT, rating REAL)''')

# Function to insert movie data into the database, avoiding duplicates
def insert_movie(title, genre, synopsis, rating):
    try:
        c.execute("INSERT INTO movies (title, genre, synopsis, rating) VALUES (?, ?, ?, ?)", (title, genre, synopsis, rating))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Movie '{title}' already exists in the database. Skipping...")
        conn.rollback()  # Rollback the transaction to maintain data consistency

# Function to fetch data from the API and add it to the database
def fetch_and_add_movies():
    url = "https://ott-details.p.rapidapi.com/advancedsearch"
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
    print(data)
    for movie in data.get('results', []):
        title = movie.get('title', '')
        genre = ', '.join(movie.get('genre', []))
        synopsis = movie.get('synopsis', '')
        rating = float(movie.get('imdbrating', 0))
        insert_movie(title, genre, synopsis, rating)

# Example usage to fetch data from the API and add it to the database
fetch_and_add_movies()

c.execute("SELECT * from movies")
rows = c.fetchall()
for row in rows:
    print(row)
# Close the database connection when done
conn.close()
