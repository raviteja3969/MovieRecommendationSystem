import csv
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('movie_database')

def movie_exists(title):
    response = table.get_item(Key={'title': title})
    return 'Item' in response

def load_data_from_csv(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            # Check if the pipe character exists in the value before replacing it
            if '|' in row['genres']:
                row['genres'] = row['genres'].replace('|', ',')
                row['movie_title'] = row['movie_title'].replace('\xa0','')

            # Check if a movie with the same title already exists in DynamoDB
            if not movie_exists(row['movie_title']):
                item = {
                    'title': row['movie_title'],
                    'genre': row['genres'],
                    'rating': row['imdb_score'],
                }
                # Insert item into DynamoDB table
                table.put_item(Item=item)
            else:
                print(f"Movie '{row['movie_title']}' already exists in DynamoDB. Skipping...")

load_data_from_csv('/Users/ravitejanidanampally/Documents/MyProjects/RecommendationSystem/src/movie_data.csv')
