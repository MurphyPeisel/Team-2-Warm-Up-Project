
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
import asyncio


cred = credentials.Certificate("movies-database-f449c-firebase-adminsdk-rh05s-7d539e0132.json")
app = firebase_admin.initialize_app(cred)

db = firestore_async.client()

async def addDocument():
  doc_ref = db.collection("movies").document("Shawshank Redemption")
  await doc_ref.set(
      {
  "certificate": "A",
  "director": "Francis Ford Coppola",
  "genre": "Drama",
  "gross": 28341469,
  "imdb_rating": 9.3,
  "meta_score": 80,
  "num_votes": 2343110,
  "runtime": 142,
  "stars": {
    "star1": "Tim Robbins",
    "star2": "Morgan Freeman",
    "star3": "Bob Gunton",
    "star4": "William Sadler"
  },
  "title": "The Shawshank Redemption",
  "year": 1994
}
  )

async def readData():
  # print("done")
  users_ref = db.collection("movies")
  docs = users_ref.stream()

  async for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")


asyncio.run(readData())