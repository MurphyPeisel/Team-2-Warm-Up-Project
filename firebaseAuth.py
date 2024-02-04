
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("movies-database-f449c-firebase-adminsdk-rh05s-7d539e0132.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

print(cred)