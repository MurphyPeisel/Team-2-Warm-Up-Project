import shlex 

# initialize valid fields and operators list
FIELDS = ["title", "year", "runtime", "genre", "imdb_rating", "director", "star1", 
          "star2","star3", "star4", "num_votes", "meta_score", "gross"]
OPERATORS = ["==", "!=", "<", "<=", ">", ">=", "contains"]

def get_input(): 
    """Receive keyboard input from user."""
    user_input = input("?? ")
    return user_input

def parse_input(in_string):
    """Parse input string into correct format for querying.

    Parameters:
    in_string -- input string

    Returns:
    ERROR -- indicates an error has occurred (-1,-1)
    or
    selected_fields -- list of fields that the user wants to view, or -1 if no input
    parsed_query -- list of dictionaries where each dictionary is a subquery
    """
    # queries are held in a list of dictionaries where each dictionary is a query with keys field, operator, value
    NUM_PARTS = 3 # number of parts in a query (field, operator, value)
    COMPOUND = " AND " # compound operator
    SELECTOR = " WHERE "
    ERROR = (-1, -1)

    selected_fields = -1
    if in_string.count(SELECTOR) > 1:
        print("ERROR -- More than one selector, please only use keyword WHERE once")
        return ERROR
    
    if in_string.count(SELECTOR) == 1:
        # allow user to select which fields to return
        selected_fields_string, in_string = in_string.split(SELECTOR)
        selected_fields = shlex.split(selected_fields_string)
        for field in selected_fields:
            if field not in FIELDS:
                print("ERROR -- Selected non-field before WHERE clause")
                return ERROR
    
    query_list = in_string.split(COMPOUND)
    parsed_query = []
    query_dict = {}
    for query in query_list:
        query = shlex.split(query)
        # validate query has correct number of parts
        if len(query) != NUM_PARTS:
            print("ERROR --  Invalid query structure: Please use command 'help' for help formatting queries.")
            return ERROR
        query_field = query[0]
        query_operator = query[1]
        query_value = query[2]
        # validate order of parts
        if query_field not in FIELDS or query_operator not in OPERATORS:
            print("ERROR --  Invalid query structure: Please use command 'help' for help formatting queries.")
            return ERROR
        # format query section as dictionary
        query_dict = {"field": query_field, "operator": query_operator, "value": query_value}
        # add to parsed query
        parsed_query.append(query_dict)
    return selected_fields, parsed_query
    
# For testing the parser

# user_input = get_input()
# parsed_query = parse_input(user_input)
# # sample loop. makes sure parsed_query is in right format, running until it is
# while parsed_query == -1:
#     user_input = get_input()
#     selected_fields, parsed_query = parse_input(user_input)
    
# print(selected_fields, parsed_query)

#TODO: every query is a list, even non-compound queries. to evaluate, make sure to do "for x in parsed_query" and evaluate all parts

import firebaseAuth

# Terms that will bring up the help output
HELP_LIST = ["help", "?"]
EXIT_LIST = ["exit", "stop", "logout", "quit", "signout"]

def get_help():
    """
    Prints out a string to help clarify operations for the user
    """
    
    print(""""
    You've accessed the help screen [By entering "help" or "?"]
    
    How to Search:
        --------------------------------------------------------------------------------------------
        Searching can be catagorized by one or more intervals of three parts. 
        (FIELD) SPACE (OPERATOR) SPACE (VALUE) ... 
        --------------------------------------------------------------------------------------------
        Example One Parameter: 
            ?? title > S   ENTER
            This will provide all movies whos name is BELOW the VALUE
        --------------------------------------------------------------------------------------------
        Example Two Parameters:
            ?? year > 1990 AND title == "Movie This One"
                Understand, the year declaration will provide all movies whos year is ABOVE 1990.
                This is different than how it works with strings. Be aware.
            AND seperates the two search terms.
                The final search term searches for a movie with the EXACT title as the VALUE. 
                Note that the movie has multiple words, it must be within quotes to operate.
            The output from this query would provide the movie 'Movie This One" from 1998.
        --------------------------------------------------------------------------------------------
    Possible Fields:
        --------------------------------------------
          *NOTE: All movies have these fields below.
        --------------------------------------------
          Known Fields:
          title         :   Title of desired movie.
          year          :   The release year with 4 digits XXXX.
          runtime       :   Duration of a movie is in MINUTES. 
          genre         :   The genre of a movie catagorizing by theme.
          imdb_rating   :   Ratings given to movies by IMBD
          director      :   Search by director and their film catalog.
          star1         :   Search by the primary actor/actress, the movies they're in.
          star2         :   Secondary actor/actress.
          star3         :   Tertiary actor/actress.
          star4         :   Quaternary actor/actress.
          num_votes     :   The number of votes on a movie for IMBD ratings.
        --------------------------------------------------------------------------------------------
          *NOTE: Not all movies have all fields, below are fields where only some contain data for. 
        --------------------------------------------------------------------------------------------    
          Optional Fields:
          meta_score    :   Ratings given to movies by Metacritic.
          gross         :   Seach by how much money a movie made.
          certificate   :   This is a rating given for audience appropriateness.
        --------------------------------------------------------------------------------------------
    Possible Operators:
        --------------------------------------------------------------------------------------------
          *NOTE: Strings and integers will work differently within these operations. 
                 Please see the rules below for the clarifaction.
        --------------------------------------------------------------------------------------------
          ==            :   Find by exact match 
          !=            :   Find everything except  
          <             :   Find values less then.
          <=            :   Find values equal to or less than 
          >             :   Find values greater then 
          >=            :   Find values equal to or greater than 
          contains      :   Find that which includes value 
        --------------------------------------------------------------------------------------------  
    About Values:
        --------------------------------------------------------------------------------------------
          Values may range and vary depending on what the user is intending on searching. Thus, 
          users must understand a couple rules and what may be accepted. Rules for values are 
          listed below:
        --------------------------------------------------------------------------------------------
          1. Some values must be searched by as STRINGS, they are listed below:
                Strings: title, genre, director, star1/2/3/4, and certificate.
          2. Some values must be searched by as INTEGERS or DOUBLES, they are listed below:
                Ints: year, runtime, votes, meta_score, and gross.
                Double: imbd_rating
          3. Querys are case sensitive, fields must be lowercase i.e. title, year, ...
          4. Understand ints and strings work differently when using < > <= >= operators. 
                Strings increase in weight from A-Z, thus Z is MORE than A.
                    title > S, will show titles that start with S-Z not A-S.
                Ints increase how one would expect, 1 is LESS than 2.
                    year > 1990, will show movies that were made after 1990.
        --------------------------------------------------------------------------------------------
          
    Enter exit, stop, logout, quit, signout to stop the program
    """)
    

# Query Engine: 
def query_engine():
    """
    Loops to allow user input that will be used to query the database
    """
    while True:
        user_input = get_input()
        
        # Allow user to call for help at any time
        while user_input in HELP_LIST:
            get_help()
            user_input = get_input()
            
        # Allow user to exit the program at any time
        if user_input in EXIT_LIST:
            return
        
        selected_fields, parsed_query = parse_input(user_input)
        
        # Proceed with querying database if the query is valid
        if parsed_query != -1:
            
            # At this point, parsed_query will be a list of dictionaries,
            # each with the following keys:
                # field, operator, and value
            
            # Sequential items in the parsed_query are to be intersected
            # This intersection will occur in the getData function
            # Call a function to query the database with the values stored
            # in the parsed query
            
            # Once select is implemented, 
            docs = firebaseAuth.getData(parsed_query)
            
            # Receive a list of movie objects that fit the query,
            # print the title and year of each item
            for doc in docs:
                
                # By default, print the title
                print_string = f"{doc.id}, "
                
                # If user selected fields with WHERE clause...
                if selected_fields != -1:
                    # See if title is requested, don't force it if it was
                    if 'title' in selected_fields:
                        print_string = ''
                        
                    # Go through the fields requested in order of request
                    for field in selected_fields:
                        print_string += f"{doc.to_dict()[field]}, "
                # Print out the requested information
                print(print_string)
                # print(f"{doc.to_dict()}") # Print out everything
            
            
            
        
query_engine()