# Movie Recommendation System

This repository contains code for a movie recommendation system built using Python and AWS services. The recommendation system is based on movie genres and utilizes cosine similarity to suggest similar movies to a given title.

## Overview

The movie recommendation system consists of several components:

1. **Data Retrieval from DynamoDB**: The system fetches movie data from a DynamoDB table named `movie_database`.

2. **Data Loading from CSV**: Data from a CSV file containing movie information is loaded into the DynamoDB table. The CSV file is expected to have columns for movie title, genres, and IMDb rating.

3. **Data Insertion from API**: Movie data is fetched from an external API using RapidAPI and added to the DynamoDB table. This data includes movie titles, genres, synopses, and IMDb ratings.

4. **Recommendation Generation**: Recommendations are generated based on the similarity of movie genres using TF-IDF vectorization and cosine similarity.

## Files

### File 1: recommendation.py

This file contains the main logic for generating movie recommendations.

- **Dependencies**: boto3, sklearn
- **Functions**:
  - `fetch_data_from_db()`: Fetches movie data from DynamoDB.
  - `get_recommendations(title)`: Generates movie recommendations based on a given movie title.

### File 2: load_data.py

This file handles the loading of movie data from a CSV file into the DynamoDB table.

- **Dependencies**: boto3, csv
- **Functions**:
  - `movie_exists(title)`: Checks if a movie already exists in the DynamoDB table.
  - `load_data_from_csv(file_path)`: Loads movie data from a CSV file into the DynamoDB table.

### File 3: fetch_and_insert.py

This file retrieves movie data from an external API and inserts it into the DynamoDB table.

- **Dependencies**: boto3, requests
- **Functions**:
  - `insert_movie(title, genre, synopsis, rating)`: Inserts movie data into the DynamoDB table.
  - `fetch_and_add_movies()`: Fetches data from an external API and adds it to the DynamoDB table.

## Usage

To use the movie recommendation system:

1. Ensure you have the necessary dependencies installed (`boto3`, `sklearn`, `requests`).
2. Run `load_data.py` to load movie data from a CSV file into the DynamoDB table.
3. Run `fetch_and_insert.py` to fetch additional movie data from the API and insert it into the DynamoDB table.
4. Run `recommendation.py` and call the `get_recommendations(title)` function to get movie recommendations based on a given title.

## External APIs

The system utilizes the RapidAPI platform to fetch additional movie data. Ensure you have an API key from RapidAPI and set it in the `X-RapidAPI-Key` header of the `fetch_and_insert.py` file.

## Note

- Ensure you have appropriate permissions set up for accessing DynamoDB.
- Modify the configuration and parameters as needed to fit your use case.
