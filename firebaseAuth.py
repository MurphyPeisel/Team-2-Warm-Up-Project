from google.cloud.firestore import FieldFilter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

class Movie:
    def __init__(self, title, year, certificate, runtime, genre, imdb_rating, meta_score,
                 director, stars, num_votes, gross):
        self.title = title
        self.year = year
        self.certificate = certificate
        self.runtime = runtime
        self.genre = genre
        self.imdb_rating = imdb_rating
        self.meta_score = meta_score
        self.director = director
        self.stars = stars
        self.num_votes = num_votes
        self.gross = gross

    @staticmethod
    def from_dict(source):
        return Movie(
            title=source['title'],
            year=source['year'],
            certificate=source['certificate'],
            runtime=source['runtime'],
            genre=source['genre'],
            imdb_rating=source['imdb_rating'],
            meta_score=source['meta_score'],
            director=source['director'],
            stars=[source['star1'], source['star2'], source['star3'], source['star4']],
            num_votes=source['num_votes'],
            gross=source['gross']
        )

    def to_dict(self):
        return {
            "title": self.title,
            "year": self.year,
            "certificate": self.certificate,
            "runtime": self.runtime,
            "genre": self.genre,
            "imdb_rating": self.imdb_rating,
            "meta_score": self.meta_score,
            "director": self.director,
            "star1": self.stars[0],
            "star2": self.stars[1],
            "star3": self.stars[2],
            "star4": self.stars[3],
            "num_votes": self.num_votes,
            "gross": self.gross
        }

    def __repr__(self):
        return f"Movie(title={self.title}, year={self.year}, genre={self.genre})"

cred = credentials.Certificate("team-2-key.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# this is the function for adding the json file to our collection
def addDocument(json_file):
  with open(json_file, 'r') as file:
    json_data = json.load(file)
    movies_ref = db.collection("movies")
    for movie in json_data:
      movies_ref.document(movie['title']).set(
        Movie(
           movie['title'],
           movie['year'],
           movie['certificate'],
           movie['runtime'],
           movie['genre'],
           movie['imdb_rating'],
           movie['meta_score'],
           movie['director'],
           [movie['star1'], movie['star2'], movie['star3'], movie['star4']],
           movie['num_votes'],
           movie['gross']
        ).to_dict()
      )

def getData():
  # parse through dictionaries in list of queries
  query_list = [{'field': 'year', 'operator': '>', 'value': '1990'}, {'field': 'director', 'operator': '==', 'value': 'Christopher Nolan'}]
  # going to get all movie objects that have been queried, and put them in a list

  movies_ref = db.collection("movies")
  query = movies_ref
  for query_info in query_list:
    field = query_info['field']
    operator = query_info['operator']
    value = query_info['value']
    
    if operator == '<':
        query = query.where(filter=FieldFilter(field, '<', value))
    elif operator == '==':
        query = query.where(filter=FieldFilter(field, '==', value))
        
  docs = (query.stream())

  for doc in docs:
      print(f"{doc.id} => {doc.to_dict()}")
  # return docs

def main():
  # addDocument('movies.json')
  getData()

main()