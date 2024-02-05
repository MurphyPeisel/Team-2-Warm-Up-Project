
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
import asyncio
import csv


cred = credentials.Certificate("team-2-key.json")
app = firebase_admin.initialize_app(cred)

db = firestore_async.client()

async def addDocument():
  with open('imdb_top_49_edited.csv', 'r') as csv_file:

    # creating csv reader
    csv_reader = csv.reader(csv_file)
    # skip header of csv file
    next(csv_reader)
    for row in csv_reader:
      doc_ref = db.collection("movies").document(row[0])
      await doc_ref.set(
          {
      "certificate": row[2],
      "director": row[7],
      "genre": row[4],
      "gross": row[13],
      "imdb_rating": row[5],
      "meta_score": row[6],
      "num_votes": row[12],
      "runtime": row[3],
      "stars": {
        "star1":row[8] ,
        "star2": row[9],
        "star3": row[10],
        "star4": row[11]
      },
      "title": row[0],
      "year": row[1]
    }
      )

async def readData():
  users_ref = db.collection("movies")
  docs = users_ref.stream()

  async for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")


# asyncio.run(addDocument())
# asyncio.run(readDocument())