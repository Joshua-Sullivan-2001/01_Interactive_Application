# leaderboard.py: manages the list of players and their turns taken, providing methods to add new records, retrieve ranked records and load saved entries

def getTurns(record): # A function to return the number of turns taken by a player from a record dictionary
    
    """The key the sorters will use. The fewer turns the better the score"""
    
    return record["turns"] # Returns the number of turns taken by a player from a record dictionary

def makeRecord(initials, turns, timestamp, source): # A function to create a new record for the leaderboard with player initials, turns taken, timestamp and source
    
    """Builds initial base record for leaderboard to use as a dictionary to ease saving as JSON file"""
    
    return {"initials": initials, "turns": turns, "timestamp": timestamp, "source": source} # Returns a new record for the leaderboard as a dictionary with player initials, turns taken, timestamp and source


class Leaderboard: # The Leaderboard class manages the list of players and their turns taken, providing methods to add new records, retrieve ranked records and load saved entries
    
    """Leaderboard class to manage the list of players and their turns taken"""

    def __init__(self, sorter): # A function to initialize the Leaderboard class with a sorter function and an empty list to hold player records
        
        """Stores the sorter function and creates an empty list to hold player records"""
        
        self.entries = [] # Start an empty list to hold player records
        self.sorter = sorter # Stores the sorter function for sorting records

    def addResult(self, record): # A function to add a new record to the end of the leaderboard list and return true if the record was added successfully or false if the record was not added
        
        """Adds a new record to the end of the leaderboard list and returns true if the record was added successfully or false if the record was not added"""
        
        if record.get("source") != "human": # Checks if the record source is not human (i.e. it's a bot)
            return False # Do not let bot records be added to the leaderboard
        
        if not record.get("initials") or record.get("turns", 0) < 1: # Checks if the record has no initials or less than 1 turn
            return False # Returns false to indicate that the record was not added due to invalid data
        self.entries.append(record) # Adds the record to the end of the leaderboard entries list so that same turn records are sorted by timestamp
        return True # Returns true to indicate that the record was added successfully
    
    def getRanked(self): # A function to return a new list of records sorted by the number of turns taken, with the fewest turns first
        
        """Returns a new list with the fewest turns first"""
        
        return self.sorter.orderItems(self.entries, getTurns) # Returns a new list of records sorted by the number of turns taken using the provided sorter function
    
    def getTop(self, n): # Returns a new list with the top n records with the fewest turns first
        
        """Returns a new list with the top n records with the fewest turns first"""
        
        ranked = self.getRanked() # Gets the ranked list of records
        return ranked[:n] # Returns the top n records from the ranked list
    
    def loadEntries(self, saved): # Adds every saved record to the leaderboard list while addResult still checks for valid records
        
        """Adds every saved record to the leaderboard list while addResult still checks for valid records"""
        
        for record in saved: # Iterates through each saved record
            self.addResult(record) # Adds the record to the leaderboard using addResult to ensure validity