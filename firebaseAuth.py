
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async
import asyncio
import json


cred = credentials.Certificate("team-2-key.json")
app = firebase_admin.initialize_app(cred)

db = firestore_async.client()

# this is the function for adding the json file to our collection
async def addDocument(json_file):

  with open(json_file, 'r') as file:
    json_data = json.load(file)

    for item in json_data:
      doc_ref = db.collection("movies").document(item['title'])
      await doc_ref.set(item)

async def readData():
  users_ref = db.collection("movies")
  docs = users_ref.stream()

  async for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")

# still need to figure out how this will interact with the query program. Should we just pull all the documents and then parse through, or should each query get only what is requested from the database. also still need to make class objects of the data, that will probably help with querying a lot actually. 

def main():
  #asyncio.run(addDocument('movies.json'))
  asyncio.run(readData())

main()