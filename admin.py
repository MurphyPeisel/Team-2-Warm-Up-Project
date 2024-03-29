import os.path
import json
import sys
import firebaseAuth
        
# this is the function for adding the json file to our collection
def addDocument(json_file):
   '''
   Takes in json_file name, adds content to database
   
   Parameters
   ----------
   json_file : str
      Filename of json file to be loaded into the database.

   Returns
   -------
   None.
   '''
    
   with open(json_file, 'r') as file:
    json_data = json.load(file)
    movies_ref = firebaseAuth.db.collection("movies")
    for movie in json_data:
      movies_ref.document(movie['title']).set(
        firebaseAuth.Movie(
           movie['title'],
           movie['year'],
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


valid = False
while not valid:
    # get filename from command line
    fileName = sys.argv[1]
    if fileName.__contains__(".json"):
        #if json file exists then prompt firebase actions
        if os.path.isfile(fileName):         
            valid = True
            #Delete all data that may exist in firestore
            #Load data(JSON) Fills our firestore database
            addDocument(fileName)
            print("File added.")
        else:
            print("That file was not found, please try again...")
            exit()
    else: 
        print("You didn't provide a .json file, try again...")
        exit()
      
