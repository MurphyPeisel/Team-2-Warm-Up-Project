import os.path

#Get json file name from user with validation
valid = False
while not valid:
    fileName = input("Please provide the name of the JSON file (ex.name.json): ")
    if fileName.__contains__(".json"):
        #if json file exists then prompt firebase actions
        if os.path.isfile(fileName):         
            valid = True
            #Delete all data that may exist in firestore

            #Load data(JSON) Fills our firestore database
        else:
            print("That file was not found, please try again...")
    else: 
        print("You didn't provide a .json file, try again...")
        

