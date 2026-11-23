# test_storage.py: tests the storage functionality for saving and loading game data

import os # Import the os module to interact with the operating system such as checking for file existence and handling file paths
import json # Import the json module to handle reading and writing JSON data for storing player data and leaderboard information
from engine.storage import Storage # Import the Storage class from the storage module

def goodEntry(initials = "ABC", turns = 5): # A function to create a valid leaderboard entry with default values for initials and turns
    
    """Return a valid leaderboard entry with the given initials and turns and a fixed timestamp for testing purposes."""
    
    return {"initials": initials, "turns": turns, "timestamp": "2026-11-20T10:00:00"} # Return a dictionary representing a valid leaderboard entry with the specified initials, turns and a fixed timestamp for testing
    

class TestStorage: # A class to test the Storage class functionality for saving and loading leaderboard data and logging events
    
    """A class to test the Storage class functionality for saving and loading leaderboard data and logging events."""
    
    def testMissingFileGivesEmptyList(self, tmp_path): # A test to check that a missing history file results in an empty list and no problems simulating a first run scenario
        
        """"Test that a missing history file results in an empty list and no problems simulating a first run scenario."""
        
        storage = Storage(str(tmp_path / "history.json")) # Create a Storage instance with a path to a non-existent history file in the temporary directory
        assert storage.loadLeaderboardData() == [], "A missing file should give an empty list." # Assert that loading leaderboard data from a missing file returns an empty list
        assert storage.problems == [], "A first run is not a problem." # Assert that there are no problems reported when loading from a missing file simulating a first run scenario

    def testEmptyFileGivesEmptyList(self, tmp_path): # A test to check that an empty history file results in an empty list simulating a first run scenario
        
        """Test that an empty history file results in an empty list simulating a first run scenario."""
        
        path = tmp_path / "history.json" # Create a path for the history file in the temporary directory
        path.write_text("   \n", encoding = "utf-8") # Write an empty string (with whitespace) to the history file to simulate an empty file
        storage = Storage(str(path)) # Create a Storage instance with the path to the empty history file
        assert storage.loadLeaderboardData() == [], "A blank file should give an empty list." # Assert that loading leaderboard data from an empty file returns an empty list

    def testBrokenJsonGivesEmptyListAndAProblem(self, tmp_path): # A test to check that a file with invalid JSON results in an empty list and a reported problem without crashing the program
        
        """Test that a file with invalid JSON results in an empty list and a reported problem without crashing the program."""
        
        path = tmp_path / "history.json" # Create a path for the history file in the temporary directory
        path.write_text("{ not json", encoding = "utf-8") # Write invalid JSON content to the history file to simulate a broken file
        storage = Storage(str(path)) # Create a Storage instance with the path to the broken history file
        assert storage.loadLeaderboardData() == [], "A broken file should give an empty list." # Assert that loading leaderboard data from a broken file returns an empty list
        assert len(storage.problems) == 1, "One problem should be reported." # Assert that one problem is reported when loading from a broken file indicating that the JSON is invalid

    def testJsonThatIsNotAListGivesAProblem(self, tmp_path): # A test to check that a file with valid JSON that is not a list results in an empty list and a reported problem without crashing the program
        
        """Test that a file with valid JSON that is not a list results in an empty list and a reported problem without crashing the program."""
        
        path = tmp_path / "history.json" # Create a path for the history file in the temporary directory
        path.write_text(json.dumps({"initials": "ABC"}), encoding = "utf-8") # Write valid JSON content that is not a list (a dictionary instead) to the history file to simulate an incorrect data structure
        storage = Storage(str(path)) # Create a Storage instance with the path to the history file containing JSON that is not a list
        assert storage.loadLeaderboardData() == [], "The wrong shape should give an empty list." # Assert that loading leaderboard data from a file with JSON that is not a list returns an empty list
        assert storage.problems == ["Data is not a list."], "The problem should say it is not a list." # Assert that the reported problem indicates that the data is not a list confirming that the Storage class correctly identifies the issue

    def testBadEntriesAreSkipped(self, tmp_path): # A test to check that bad entries in the leaderboard data are skipped and reported while good entries are still loaded correctly
        
        """Test that bad entries in the leaderboard data are skipped and reported while good entries are still loaded correctly."""
        
        path = tmp_path / "history.json" # Create a path for the history file in the temporary directory
        mixed = [goodEntry("AAA", 3), {"initials": "BBB"}, "text", goodEntry("CCC", 9)] # Create a list of mixed entries including good entries, a bad entry (missing timestamp) and a non-entry (string) to simulate a leaderboard file with both valid and invalid data
        path.write_text(json.dumps(mixed), encoding = "utf-8") # Write the mixed entries to the history file in JSON format
        storage = Storage(str(path)) # Create a Storage instance with the path to the history file containing mixed entries
        loaded = storage.loadLeaderboardData() # Load the leaderboard data from the history file which should skip bad entries and report problems
        assert [e["initials"] for e in loaded] == ["AAA", "CCC"], "Only the good entries should load." # Assert that only the good entries (with initials "AAA" and "CCC") are loaded confirming that bad entries are skipped
        assert len(storage.problems) == 2, "Each bad entry should be reported." # Assert that two problems are reported corresponding to the two bad entries in the mixed list confirming that the Storage class correctly identifies and reports issues with invalid data

    def testIsGoodEntry(self): # A test to check that the isGoodEntry method correctly identifies valid and invalid leaderboard entries based on the presence of required fields and their types
        
        """Test that the isGoodEntry method correctly identifies valid and invalid leaderboard entries based on the presence of required fields and their types."""
        
        storage = Storage("unused.json") # Create a Storage instance with a dummy path as the isGoodEntry method does not depend on the file path
        assert storage.isGoodEntry(goodEntry()) == True, "A complete entry is good." # Assert that a complete and valid entry is recognized as good by the isGoodEntry method
        assert storage.isGoodEntry({"initials": "ABC", "turns": 5}) == False, "A missing timestamp is bad." # Assert that an entry missing the timestamp field is recognized as bad by the isGoodEntry method
        assert storage.isGoodEntry({"initials": "ABC", "turns": "5", "timestamp": "x"}) == False, "Turns as text is bad." # Assert that an entry with the turns field as a string instead of an integer is recognized as bad by the isGoodEntry method
        assert storage.isGoodEntry([1, 2, 3]) == False, "A list is not an entry." # Assert that a list is not recognized as a valid entry by the isGoodEntry method confirming that the method correctly identifies invalid data types

    def testSaveAndLoadRoundTrip(self, tmp_path): # A test to check that saving and loading leaderboard data results in the same entries being returned confirming that the save and load methods work correctly together
        
        """Test that saving and loading leaderboard data results in the same entries being returned confirming that the save and load methods work correctly together."""
        
        storage = Storage(str(tmp_path / "history.json")) # Create a Storage instance with a path to the history file in the temporary directory
        entries = [goodEntry("AAA", 3), goodEntry("BBB", 8)] # Create a list of good entries to be saved to the history file
        assert storage.saveLeaderboardData(entries) == True, "A good save should return True." # Assert that saving the good entries returns True indicating a successful save operation
        assert storage.loadLeaderboardData() == entries, "The loaded entries should match the saved ones." # Assert that loading the leaderboard data returns the same entries that were saved confirming that the save and load methods work correctly together

    def testSaveOverwritesOldData(self, tmp_path): # A test to check that saving new leaderboard data overwrites old data instead of appending to it ensuring that only the most recent save is retained in the history file
        
        """Test that saving new leaderboard data overwrites old data instead of appending to it ensuring that only the most recent save is retained in the history file."""
        
        storage = Storage(str(tmp_path / "history.json")) # Create a Storage instance with a path to the history file in the temporary directory
        storage.saveLeaderboardData([goodEntry("AAA", 3)]) # Save an initial entry to the history file
        storage.saveLeaderboardData([goodEntry("BBB", 8)]) # Save a new entry to the history file which should overwrite the previous entry
        assert [e["initials"] for e in storage.loadLeaderboardData()] == ["BBB"], "Only the second save should remain." # Assert that loading the leaderboard data returns only the second entry, confirming that the old data was overwritten by the new save operation

    def testSaveCreatesTheFolderAndLeavesNoTempFile(self, tmp_path): # A test to check that saving leaderboard data creates the necessary folder if it does not exist and does not leave behind any temporary files after the save operation
        
        """Test that saving leaderboard data creates the necessary folder if it does not exist and does not leave behind any temporary files after the save operation."""
        
        path = tmp_path / "data" / "history.json" # Create a path for the history file in a subdirectory of the temporary directory simulating a scenario where the folder does not exist
        storage = Storage(str(path)) # Create a Storage instance with the path to the history file in the non-existent folder
        assert storage.saveLeaderboardData([goodEntry()]) == True, "The save should work." # Assert that saving the good entry returns True indicating a successful save operation
        assert path.exists(), "The history file should exist." # Assert that the history file now exists confirming that the necessary folder was created during the save operation
        assert not os.path.exists(str(path) + ".tmp"), "The temporary file should be gone." # Assert that no temporary file (with a .tmp extension) exists after the save operation confirming that the save method cleans up any temporary files it creates

    def testSaveRejectsANonList(self, tmp_path): # A test to check that saving something that is not a list returns False and does not write anything to the history file ensuring that only valid leaderboard data is accepted
        
        """Test that saving something that is not a list returns False and does not write anything to the history file ensuring that only valid leaderboard data is accepted."""
        
        path = tmp_path / "history.json" # Create a path for the history file in the temporary directory
        storage = Storage(str(path)) # Create a Storage instance with the path to the history file
        assert storage.saveLeaderboardData("not a list") == False, "A non list should be refused." # Assert that attempting to save a string (which is not a list) returns False indicating that the save operation was rejected
        assert not path.exists(), "Nothing should be written." # Assert that the history file does not exist after the failed save operation confirming that no data was written to the file when an invalid input was provided

    def testSaveFailureReturnsFalse(self, tmp_path): # A test to check that a save operation that cannot be written returns False and reports a problem ensuring that the Storage class handles write failures gracefully
        
        """Test that a save operation that cannot be written returns False and reports a problem ensuring that the Storage class handles write failures gracefully."""
        
        blocker = tmp_path / "blocker" # Create a path for a file that will block the save operation by being a directory instead of a file
        blocker.write_text("x", encoding = "utf-8") # Write some content to the blocker path making it a file that will prevent the save operation from creating a history.json file in the same location
        storage = Storage(str(blocker / "history.json")) # Create a Storage instance with a path that points to a file inside the blocker directory which will cause the save operation to fail because it cannot create a file in a non-directory path
        assert storage.saveLeaderboardData([goodEntry()]) == False, "The save should fail safely." # Assert that attempting to save the good entry returns False indicating that the save operation failed due to the inability to write to the specified path
        assert storage.problems == ["Failed to save leaderboard data."], "The problem should be reported." # Assert that the reported problem indicates that the save operation failed confirming that the Storage class correctly identifies and reports issues when it cannot write to the specified path

    def testClearLeavesAnEmptyList(self, tmp_path): # A test to check that clearing the leaderboard data results in an empty list being saved to the history file ensuring that the clear operation works correctly
        
        """Test that clearing the leaderboard data results in an empty list being saved to the history file ensuring that the clear operation works correctly."""
        
        storage = Storage(str(tmp_path / "history.json")) # Create a Storage instance with a path to the history file in the temporary directory
        storage.saveLeaderboardData([goodEntry()]) # Save an initial entry to the history file to ensure that there is data to clear
        storage.clearLeaderboardData() # Call the clearLeaderboardData method to clear the leaderboard data which should result in an empty list being saved to the history file
        assert storage.loadLeaderboardData() == [], "After clearing the list should be empty." # Assert that loading the leaderboard data after clearing returns an empty list confirming that the clear operation successfully removed all entries from the history file

    def testConvertToRawText(self): # A test to check that the convertToRawText method correctly converts a list of leaderboard entries into a formatted string representation with each entry on a separate line
        
        """Test that the convertToRawText method correctly converts a list of leaderboard entries into a formatted string representation with each entry on a separate line."""
        
        storage = Storage("unused.json") # Create a Storage instance with a dummy path as the convertToRawText method does not depend on the file path
        text = storage.convertToRawText([goodEntry("AAA", 3), goodEntry("BBB", 8)]) # Call the convertToRawText method with a list of good entries to convert them into a formatted string representation
        assert text == "AAA - 3 turns - 2026-11-20T10:00:00\nBBB - 8 turns - 2026-11-20T10:00:00", "Each entry should be one line." # Assert that the formatted string representation matches the expected output with each entry on a separate line
        assert storage.convertToRawText([]) == "", "No entries should give empty text." # Assert that the formatted string representation matches the expected output with each entry on a separate line and that an empty list of entries results in an empty string

    def testLogEventWritesATimestampedLine(self, tmp_path): # A test to check that the logEvent method correctly writes a timestamped line to the log file with each event being recorded on a separate line
        
        """Test that the logEvent method correctly writes a timestamped line to the log file with each event being recorded on a separate line."""
        
        path = tmp_path / "logs" / "game.log" # Create a path for the log file in a subdirectory of the temporary directory simulating a scenario where the folder does not exist
        logger = Storage(str(path)) # Create a Storage instance with the path to the log file in the non-existent folder
        logger.logEvent("First event") # Log the first event using the logEvent method which should write a timestamped line to the log file
        logger.logEvent("Second event") # Log the second event using the logEvent method which should write another timestamped line to the log file
        lines = path.read_text(encoding = "utf-8").splitlines() # Read the contents of the log file and split it into lines to verify that each event was recorded correctly
        assert len(lines) == 2, "There should be two lines." # Assert that there are two lines in the log file confirming that both events were logged successfully
        assert lines[0].startswith("[") and lines[0].endswith("] First event"), "The line should be a timestamp then the text." # Assert that the first line in the log file starts with a timestamp and ends with the text of the first event confirming that the logEvent method correctly formats the log entry
        assert lines[1].endswith("] Second event"), "The second event should be on the second line." # Assert that the second line in the log file ends with the text of the second event confirming that the logEvent method correctly formats the log entry for the second event
