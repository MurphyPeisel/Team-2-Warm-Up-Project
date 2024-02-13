from google.cloud.firestore import FieldFilter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# creating a movie class to define each movie as an object. Each movie is initialized with the following values.
class Movie:
    def __init__(self, title, year, runtime, genre, imdb_rating, meta_score,
                 director, stars, num_votes, gross):
        self.title = title
        self.year = year
        self.runtime = runtime
        self.genre = genre
        self.imdb_rating = imdb_rating
        self.meta_score = meta_score
        self.director = director
        self.stars = stars
        self.num_votes = num_votes
        self.gross = gross

    #
    @staticmethod
    def from_dict(source):
        return Movie(
            title=source['title'],
            year=source['year'],
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

def getData(query_list):
    movies_ref = db.collection("movies")
    docs_list = []
    for query_info in query_list:
        field = query_info['field']
        operator = query_info['operator']
        value = query_info['value']

        if field in ["year", "meta_score", "num_votes"]:
            value = int(value)
        if field == "imdb_rating":
            value = float(value)
        query = movies_ref.where(field, operator, value)
        docs = query.stream()
        docs_list.append(docs)

    queried_movies = []
    seen_ids = set()
    for docs in docs_list:
        for doc in docs:
            if doc.id in seen_ids:
                # if the id has been seen before, add the document to queried_movies
                queried_movies.append(doc)
            else:
                # if the id is encountered for the first time, add it to the set of seen ids
                seen_ids.add(doc.id)
    # for doc in queried_movies:
    #     print(doc.id)
    return queried_movies