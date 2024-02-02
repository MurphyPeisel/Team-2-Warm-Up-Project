import shlex 

# initialize valid fields and operators list
FIELDS = ["title", "year", "runtime", "genre", "imdb_rating", "director", "star1", 
          "star2","star3", "star4", "num_votes", "certificate", "meta_score", "gross"]
OPERATORS = ["==", "!=", "<", "<=", ">", ">=", "in"]

def get_input(): 
    """Receive keyboard input from user."""
    user_input = input("?? ")
    return user_input

def parse_input(in_string):
    """Parse input string into correct format for querying.

    Parameters:
    in_string -- input string

    Returns:
    ERROR -- indicates an error has occurred (-1)
    parsed_query -- list of dictionaries where each dictionary is a subquery
    """
    # queries are held in a list of dictionaries where each dictionary is a query with keys field, operator, value
    NUM_PARTS = 3 # number of parts in a query (field, operator, value)
    COMPOUND = " AND " # compound operator
    ERROR = -1

    num_comparisons = in_string.count(COMPOUND) + 1 # always 1 more comparison than compound operators
    query_list = in_string.split(" AND ")
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
    return parsed_query
    
user_input = get_input()
parsed_query = parse_input(user_input)
# sample loop. makes sure parsed_query is in right format, running until it is
while parsed_query == -1:
    user_input = get_input()
    parsed_query = parse_input(user_input)
    
print(parsed_query)

#TODO: every query is a list, even non-compound queries. to evaluate, make sure to do "for x in parsed_query" and evaluate all parts


#%%
import firebaseAuth

# Terms that will bring up the help output
HELP_LIST = ["help", "?"]
EXIT_LIST = ["exit", "stop", "logout", "quit", "signout"]

def get_help():
    """
    Prints out a string to help clarify operations for the user
    """
    
    print(""""
    You've accessed the help screen
    
    Enter exit, stop, logout, quit, signout to stop the program
    """)
    

# Query Engine: 
def query_engine():
    while True:
        user_input = get_input()
        
        # Allow user to call for help at any time
        while user_input in HELP_LIST:
            get_help()
            user_input = get_input()
            
        # Allow user to exit the program at any time
        if user_input in EXIT_LIST:
            return
        
        parsed_query = parse_input(user_input)
        
        # make sure parsed_query is in right format, running until it is
        if parsed_query != -1:
            # Proceed with querying database, otherwise start over
            pass
            
            # Call upon firebaseAuth function with the parsed query
            
            
        
query_engine()