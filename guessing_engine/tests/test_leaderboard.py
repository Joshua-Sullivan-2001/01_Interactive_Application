# test_leaderboard.py: tests the leaderboard functionality and score management

from engine.leaderboard import Leaderboard, makeRecord, getTurns # Import the Leaderboard class and utility functions from the leaderboard module
from engine.sorting import insertionSorter, mergeSorter # Import the insertionSorter and mergeSorter functions from the sorting module

def humanRecord(initials, turns, timestamp = "2026-11-20T10:00:00"): # A function to create a human record with default timestamp for testing purposes
    
    """Creates a human record with the given initials, turns and timestamp."""
    
    return makeRecord(initials, turns, timestamp, "human") # Return a record dictionary with the provided initials, turns, timestamp and source set to "human"
    

class TestLeaderboard: # A class holding the tests for the Leaderboard functionality
    
    """Tests for the Leaderboard class and makeRecord and getTurns."""
    
    def testMakeRecord(self): # A function to test the makeRecord function
        
        """Tests that makeRecord creates a record with the correct structure and values."""
        
        record = makeRecord("ABC", 7, "2026-11-20T10:00:00", "human") # Create a record using makeRecord with specified initials, turns, timestamp and source
        assert record == {"initials": "ABC", "turns": 7, "timestamp": "2026-11-20T10:00:00", "source": "human"}, "The record should hold all four values." # Assert that the created record matches the expected dictionary structure and values

    def testGetTurns(self): # A function to test the getTurns function
        
        """Tests that getTurns retrieves the number of turns from a record."""
        
        assert getTurns(humanRecord("ABC", 7)) == 7, "getTurns should return the turns." # Assert that getTurns returns the correct number of turns from a human record

    def testEmptyLeaderboard(self): # A function to test the behavior of a new empty leaderboard
        
        """Tests that a new leaderboard is empty and returns empty lists for ranked and top results.""" 
        
        board = Leaderboard(insertionSorter()) # Create a new Leaderboard instance using the insertionSorter for sorting
        assert board.getRanked() == [], "A new leaderboard should be empty." # Assert that getRanked returns an empty list for a new leaderboard
        assert board.getTop(3) == [], "The top of an empty leaderboard should be empty." # Assert that getTop returns an empty list when requesting the top results from a new leaderboard

    def testAddHumanResult(self): # A function to test adding a valid human result to the leaderboard
        
        """Tests that a valid human result can be added to the leaderboard and is stored correctly."""
        
        board = Leaderboard(insertionSorter()) # Create a new Leaderboard instance using the insertionSorter for sorting
        assert board.addResult(humanRecord("ABC", 5)) == True, "A good human result should be added." # Assert that adding a valid human record returns True indicating successful addition
        assert len(board.entries) == 1, "The result should be in the list." # Assert that the length of the entries list is 1 confirming that the result was added to the leaderboard

    def testBotResultsAreRejected(self): # A function to test that bot results are not added to the leaderboard
        
        """Tests that results from bots are rejected and not stored in the leaderboard."""
        
        board = Leaderboard(insertionSorter()) # Create a new Leaderboard instance using the insertionSorter for sorting
        botRecord = makeRecord("BOT", 7, "2026-11-20T10:00:00", "bot") # Create a bot record using makeRecord with specified initials, turns, timestamp and source set to "bot"
        assert board.addResult(botRecord) == False, "A bot result should be rejected." # Assert that adding a bot record returns False,# indicating that the result was rejected
        assert board.entries == [], "Nothing should be stored." # Assert that the entries list is still empty confirming that the bot result was not stored in the leaderboard

    def testBadRecordsAreRejected(self): # A function to test that invalid records are rejected and not added to the leaderboard
        
        """Tests that records with missing or invalid data are rejected and not stored in the leaderboard."""
        
        board = Leaderboard(insertionSorter()) # Create a new Leaderboard instance using the insertionSorter for sorting
        assert board.addResult(humanRecord("", 5)) == False, "Empty initials should be rejected." # Assert that adding a record with empty initials returns False indicating that the result was rejected
        assert board.addResult(humanRecord("ABC", 0)) == False, "Zero turns should be rejected." # Assert that adding a record with zero turns returns False indicating that the result was rejected
        assert board.addResult(humanRecord("ABC", -3)) == False, "Negative turns should be rejected." # Assert that adding a record with negative turns returns False indicating that the result was rejected
        assert board.addResult({"source": "human"}) == False, "A record with missing keys should be rejected." # Assert that adding a record with missing keys returns False indicating that the result was rejected
        assert board.entries == [], "Nothing should be stored." # Assert that the entries list is still empty confirming that no invalid records were stored in the leaderboard

    def testRankedFewestTurnsFirst(self): # A function to test that the leaderboard ranks results with the fewest turns first regardless of the sorting algorithm used
        
        """Tests that the leaderboard ranks results with the fewest turns first regardless of the sorting algorithm used."""
        
        for sorter in (insertionSorter(), mergeSorter()): # Loop through both sorting algorithms to ensure consistent behavior across different sorting methods
            board = Leaderboard(sorter) # Create a new Leaderboard instance using the current sorter for sorting
            board.addResult(humanRecord("AAA", 9)) # Add a human record with initials "AAA" and 9 turns to the leaderboard
            board.addResult(humanRecord("BBB", 3)) # Add a human record with initials "BBB" and 3 turns to the leaderboard
            board.addResult(humanRecord("CCC", 6)) # Add a human record with initials "CCC" and 6 turns to the leaderboard
            ranked = board.getRanked() # Get the ranked list of results from the leaderboard
            assert [r["initials"] for r in ranked] == ["BBB", "CCC", "AAA"], "The fewest turns should come first." # Assert that the ranked list of initials is in the expected order confirming that results with the fewest turns are ranked first

    def testTiesKeepTheEarlierResultFirst(self): # A function to test that when results have the same number of turns the earlier result is ranked first
        
        """Tests that when results have the same number of turns the earlier result is ranked first.""" 
        
        for sorter in (insertionSorter(), mergeSorter()): # Loop through both sorting algorithms to ensure consistent behavior across different sorting methods
            board = Leaderboard(sorter) # Create a new Leaderboard instance using the current sorter for sorting
            board.addResult(humanRecord("AAA", 4, "2026-11-20T10:00:00")) # Add a human record with initials "AAA", 4 turns and a specific timestamp to the leaderboard
            board.addResult(humanRecord("BBB", 4, "2026-11-20T10:05:00")) # Add a human record with initials "BBB", 4 turns and a later timestamp to the leaderboard
            board.addResult(humanRecord("CCC", 2, "2026-11-20T10:10:00")) # Add a human record with initials "CCC", 2 turns and a later timestamp to the leaderboard
            ranked = board.getRanked() # Get the ranked list of results from the leaderboard
            assert [r["initials"] for r in ranked] == ["CCC", "AAA", "BBB"], "The earlier tied result should rank first." # Assert that the ranked list of initials is in the expected order confirming that when results have the same number of turns the earlier result is ranked first

    def testGetRankedDoesNotChangeEntries(self): # A function to test that calling getRanked does not change the order of the stored entries in the leaderboard
        
        """Tests that calling getRanked does not change the order of the stored entries in the leaderboard."""
        
        board = Leaderboard(insertionSorter()) # Create a new Leaderboard instance using the insertionSorter for sorting
        board.addResult(humanRecord("AAA", 9)) # Add a human record with initials "AAA" and 9 turns to the leaderboard
        board.addResult(humanRecord("BBB", 3)) # Add a human record with initials "BBB" and 3 turns to the leaderboard
        board.getRanked() # Call getRanked to retrieve the ranked list of results from the leaderboard
        assert [r["initials"] for r in board.entries] == ["AAA", "BBB"], "The stored order should not change." # Assert that the order of the stored entries in the leaderboard remains unchanged after calling getRanked confirming that the method does not modify the original entries list

    def testGetTop(self): # A function to test that getTop returns the best n results and handles cases where n is larger than the number of entries in the leaderboard
        
        """Tests that getTop returns the best n results and handles cases where n is larger than the number of entries in the leaderboard."""
        
        board = Leaderboard(mergeSorter()) # Create a new Leaderboard instance using the mergeSorter for sorting
        board.addResult(humanRecord("AAA", 9)) # Add a human record with initials "AAA" and 9 turns to the leaderboard
        board.addResult(humanRecord("BBB", 3)) # Add a human record with initials "BBB" and 3 turns to the leaderboard
        board.addResult(humanRecord("CCC", 6)) # Add a human record with initials "CCC" and 6 turns to the leaderboard
        assert [r["initials"] for r in board.getTop(2)] == ["BBB", "CCC"], "getTop(2) should give the best two." # Assert that getTop(2) returns the initials of the best two results in the expected order
        assert len(board.getTop(10)) == 3, "Asking for more than there are should give them all." # Assert that calling getTop with a number larger than the number of entries in the leaderboard returns all available entries confirming that the method handles such cases correctly

    def testLoadEntriesKeepsOnlyGoodRecords(self): # A function to test that loadEntries only adds valid records to the leaderboard and skips invalid ones
        
        """Tests that loadEntries only adds valid records to the leaderboard and skips invalid ones."""
        
        board = Leaderboard(insertionSorter()) # Create a new Leaderboard instance using the insertionSorter for sorting
        saved = [humanRecord("AAA", 5), makeRecord("BOT", 3, "2026-11-20T10:00:00", "bot"), humanRecord("", 4), humanRecord("BBB", 2)] # Define a list of saved records including valid human records and invalid records (bot and empty initials)
        board.loadEntries(saved) # Load a list of saved records into the leaderboard including valid human records and invalid records (bot and empty initials)
        assert [r["initials"] for r in board.entries] == ["AAA", "BBB"], "Only the good records should be loaded." # Assert that the initials of the entries in the leaderboard after loading only include the valid human records confirming that invalid records were skipped during the loading process
