# test_storage.py: tests the storage functionality for saving and loading game data

import os # Import the os module to interact with the operating system, such as checking for file existence and handling file paths
import json # Import the json module to handle reading and writing JSON data for storing player data and leaderboard information
from engine.storage import Storage # Import the Storage class from the storage module

class TestStorage: # Define a test class to validate the functionality of the Storage class including loading, saving and clearing player data as well as converting data to a raw text format
    
    """A test class to validate the functionality of the Storage class including loading, saving and clearing player data as well as converting data to a raw text format."""

    def setup_method(self, method): # Define a setup method that runs before each test method to prepare the test environment
        
        """Setup method to initialize the Storage class and prepare the test environment before each test method."""
        
        self.testFilename = "test_leaderboard.json" # Define a test filename for the leaderboard JSON file to avoid issues with the actual game data
        self.storage = Storage(self.testFilename) # Create an instance of the Storage class using the test filename
        self.storage.clearLeaderboardData() # Clear any existing data (Which shouldn't be present) in the test leaderboard file to ensure a clean state for testing
    
    def cleanupMethod(self, method): # Define a cleaning method that runs after each test method to clean up the test environment
        
        """Method to clean up the test save file after each test method."""
        
        if os.path.exists(self.testFilename): # Check if the test leaderboard JSON file exists
            os.remove(self.testFilename) # Remove the test leaderboard JSON file to clean up after tests
    
    def testLoadDataEmpty(self): # Define a test method to validate loading data from an empty leaderboard file
        
        """Test loading data from an empty leaderboard file."""
        
        data = self.storage.loadLeaderboardData() # Load leaderboard data from the test leaderboard file
        assert data == [], "Loading from an empty file should return an empty list." # Assert that the loaded data are an empty list indicating no data are present
    
    def testSaveAndLoadData(self): # Define a test method to validate saving and loading data to and from the leaderboard file
        
        """Test saving and loading data to and from the leaderboard file."""
        
        testData = [{"name": "Alice", "turns taken": 10}, {"name": "Bob", "turns taken": 20}] # Define a list of test data to save
        self.storage.saveLeaderboardData(testData) # Save the test data to the leaderboard file
        loadedData = self.storage.loadLeaderboardData() # Load the data back from the leaderboard file
        assert loadedData == testData, "Loaded data should match the saved data." # Assert that the loaded data match the originally saved test data
    
    def testClearData(self): # Define a test method to validate clearing data from the leaderboard file
        
        """Test clearing data from the leaderboard file."""
        
        testData = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save
        self.storage.saveLeaderboardData(testData) # Save the test data to the leaderboard file
        self.storage.clearLeaderboardData() # Clear the data from the leaderboard file
        loadedData = self.storage.loadLeaderboardData() # Load the data back from the leaderboard file
        assert loadedData == [], "After clearing, loading should return an empty list." # Assert that the loaded data are an empty list indicating that the data were successfully cleared
    
    def testConvertToRawText(self): # Define a test method to validate converting data to a raw text format
        
        """Test converting data to a raw text format."""
        
        testData = [{"name": "Alice", "turns taken": 10}, {"name": "Bob", "turns taken": 20}] # Define a list of test data to convert
        rawText = self.storage.convertToRawText(testData) # Convert the test data to a raw text format
        expectedText = "Alice: 10\nBob: 20" # Define the expected raw text output for the test data
        assert rawText == expectedText, "Raw text conversion should match the expected format." # Assert that the converted raw text matches the expected output format
    
    def testLoadDataNonexistentFile(self): # Define a test method to validate loading data from a nonexistent leaderboard file
        
        """Test loading data from a nonexistent leaderboard file."""
        
        nonExistentStorage = Storage("nonexistent_file.json") # Create an instance of the Storage class with a filename that does not exist
        data = nonExistentStorage.loadLeaderboardData() # Attempt to load data from the nonexistent file
        assert data == [], "Loading from a nonexistent file should return an empty list." # Assert that the loaded data is an empty list indicating that no data is present in a nonexistent file
    
    def testSaveDataOverwrite(self): # Define a test method to validate that saving data overwrites existing data in the leaderboard file
        
        """Test that saving data overwrites existing data in the leaderboard file."""
        
        initialData = [{"name": "Alice", "turns taken": 10}] # Define an initial list of test data to save
        self.storage.saveLeaderboardData(initialData) # Save the initial test data to the leaderboard file
        newData = [{"name": "Bob", "turns taken": 20}] # Define a new list of test data to overwrite the initial data
        self.storage.saveLeaderboardData(newData) # Save the new test data to the leaderboard file, overwriting the initial data
        loadedData = self.storage.loadLeaderboardData() # Load the data back from the leaderboard file
        assert loadedData == newData, "Loaded data should match the newly saved data after overwrite." # Assert that the loaded data match the newly saved test data confirming that the overwrite was successful
    
    def testConvertToRawTextEmpty(self): # Define a test method to validate converting an empty list of data to a raw text format
        
        """Test converting an empty list of data to a raw text format."""
        
        emptyData = [] # Define an empty list of data
        rawText = self.storage.convertToRawText(emptyData) # Convert the empty list of data to a raw text format
        assert rawText == "", "Converting an empty list should return an empty string." # Assert that the converted raw text is an empty string indicating that there is no data to display
    
    def testConvertToRawTextSingleEntry(self): # Define a test method to validate converting a single player entry to a raw text format
        
        """Test converting a single player entry to a raw text format."""
        
        singlePlayerData = [{"name": "Alice", "turns taken": 10}] # Define a list containing a single player entry
        rawText = self.storage.convertToRawText(singlePlayerData) # Convert the single player entry to a raw text format
        expectedText = "Alice: 10" # Define the expected raw text output for the single player entry
        assert rawText == expectedText, "Raw text conversion for a single entry should match the expected format." # Assert that the converted raw text matches the expected output format for a single player entry
    
    def testLoadDataInvalidJson(self): # Define a test method to validate loading data from a leaderboard file containing invalid JSON data
        
        """Test loading data from a leaderboard file containing invalid JSON data."""
        
        with open(self.testFilename, "w") as file: # Open the test leaderboard JSON file in write mode
            file.write("Invalid JSON content") # Write invalid JSON content to the file
        try: # Attempt to load data from the file containing invalid JSON data
            self.storage.loadLeaderboardData() # Load data from the test leaderboard file
            assert False, "Loading from a file with invalid JSON should raise a JSONDecodeError." # If no exception is raised assert False to indicate the test failed
        except json.JSONDecodeError: # Catch the expected JSONDecodeError exception
            pass # If the exception is raised, pass the test as it is the expected behavior
    
    def testSaveDataCreatesFile(self): # Define a test method to validate that saving data creates the leaderboard file if it does not exist
        
        """Test that saving data creates the leaderboard file if it does not exist."""
        
        if os.path.exists(self.testFilename): # Check if the test leaderboard JSON file exists
            os.remove(self.testFilename) # Remove the test leaderboard JSON file to ensure it does not exist before the test
        testData = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save
        self.storage.saveLeaderboardData(testData) # Save the test data to the leaderboard file
        assert os.path.exists(self.testFilename), "Saving data should create the leaderboard file if it does not exist." # Assert that the leaderboard file now exists confirming that saving data created the file
    
    def testClearDataCreatesFile(self): # Define a test method to validate that clearing data creates the leaderboard file if it does not exist
        
        """Test that clearing data creates the leaderboard file if it does not exist."""
        
        if os.path.exists(self.testFilename): # Check if the test leaderboard JSON file exists
            os.remove(self.testFilename) # Remove the test leaderboard JSON file to ensure it does not exist before the test
        self.storage.clearLeaderboardData() # Clear the data from the leaderboard file
        assert os.path.exists(self.testFilename), "Clearing data should create the leaderboard file if it does not exist." # Assert that the leaderboard file now exists, confirming that clearing data created the file
    
    def testLoadDataAfterClear(self): # Define a test method to validate that loading data after clearing returns an empty list
        
        """Test that loading data after clearing returns an empty list."""
        
        testData = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save
        self.storage.saveLeaderboardData(testData) # Save the test data to the leaderboard file
        self.storage.clearLeaderboardData() # Clear the data from the leaderboard file
        loadedData = self.storage.loadLeaderboardData() # Load the data back from the leaderboard file
        assert loadedData == [], "After clearing, loading should return an empty list." # Assert that the loaded data is an empty list indicating that the data was successfully cleared
    
    def testSaveDataMultipleTimes(self): # Define a test method to validate that saving data multiple times overwrites the previous data
        
        """Test that saving data multiple times overwrites the previous data."""
        
        firstData = [{"name": "Alice", "turns taken": 10}] # Define the first list of test data to save
        self.storage.saveLeaderboardData(firstData) # Save the first test data to the leaderboard file
        secondData = [{"name": "Bob", "turns taken": 20}] # Define the second list of test data to save
        self.storage.saveLeaderboardData(secondData) # Save the second test data to the leaderboard file overwriting the first data
        loadedData = self.storage.loadLeaderboardData() # Load the data back from the leaderboard file
        assert loadedData == secondData, "Loaded data should match the last saved data after multiple saves." # Assert that the loaded data match the last saved test data confirming that multiple saves overwrite previous data
    
    def testClearLeaderboardDataMultipleTimes(self): # Define a test method to validate that clearing data multiple times does not cause errors and always results in an empty list
        
        """Test that clearing data multiple times does not cause errors and always results in an empty list."""
        
        testData = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save
        self.storage.saveLeaderboardData(testData) # Save the test data to the leaderboard file
        self.storage.clearLeaderboardData() # Clear the data from the leaderboard file
        self.storage.clearLeaderboardData() # Clear the data again to test multiple clears
        loadedData = self.storage.loadLeaderboardData() # Load the data back from the leaderboard file
        assert loadedData == [], "After multiple clears, loading should return an empty list." # Assert that the loaded data is an empty list indicating that multiple clears do not cause errors and result in an empty state
    
    def testConvertToRawTextSpecialCharacters(self): # Define a test method to validate converting data with special characters to a raw text format
        
        """Test converting data with special characters to a raw text format."""
        
        specialData = [{"name": "Al!ce", "turns taken": 10}, {"name": "B@b", "turns taken": 20}] # Define a list of test data with special characters in player names
        rawText = self.storage.convertToRawText(specialData) # Convert the test data with special characters to a raw text format
        expectedText = "Al!ce: 10\nB@b: 20" # Define the expected raw text output for the test data with special characters
        assert rawText == expectedText, "Raw text conversion should correctly handle special characters in names." # Assert that the converted raw text matches the expected output format confirming that special characters are handled correctly
    
    def testConvertToRawTextLargeNumbers(self): # Define a test method to validate converting data with large numbers to a raw text format
        
        """Test converting data with large numbers to a raw text format."""
        
        largeTurns = [{"name": "Alice", "turns taken": 1000000}, {"name": "Bob", "turns taken": 2000000}] # Define a list of test data with large turns taken values
        rawText = self.storage.convertToRawText(largeTurns) # Convert the test data with large numbers to a raw text format
        expectedText = "Alice: 1000000\nBob: 2000000" # Define the expected raw text output for the test data with large numbers
        assert rawText == expectedText, "Raw text conversion should correctly handle large numbers." # Assert that the converted raw text matches the expected output format confirming that large numbers are handled correctly
    
    def testConvertToRawTextSpecialCharactersInNames(self): # Define a test method to validate converting data with special characters in player names to a raw text format
        
        """Test converting data with special characters in player names to a raw text format."""
        
        specialCharData = [{"name": "Al!ce", "turns taken": 10}, {"name": "B@b", "turns taken": 20}] # Define a list of test data with special characters in player names
        rawText = self.storage.convertToRawText(specialCharData) # Convert the test data with special characters to a raw text format
        expectedText = "Al!ce: 10\nB@b: 20" # Define the expected raw text output for the test data with special characters
        assert rawText == expectedText, "Raw text conversion should correctly handle special characters in player names." # Assert that the converted raw text matches the expected output format confirming that special characters in player names are handled correctly
    
    def testConvertToRawTextUnicodeNames(self): # Define a test method to validate converting data with Unicode characters in player names to a raw text format
        
        """Test converting data with Unicode characters in player names to a raw text format."""
        
        unicodeData = [{"name": "Alïce", "turns taken": 10}, {"name": "Bøb", "turns taken": 20}] # Define a list of test data with Unicode characters in player names
        rawText = self.storage.convertToRawText(unicodeData) # Convert the test data with Unicode characters to a raw text format
        expectedText = "Alïce: 10\nBøb: 20" # Define the expected raw text output for the test data with Unicode characters
        assert rawText == expectedText, "Raw text conversion should correctly handle Unicode characters in player names." # Assert that the converted raw text matches the expected output format confirming that Unicode characters in player names are handled correctly
    
    def testConvertToRawTextEmptyNames(self): # Define a test method to validate converting data with empty player names to a raw text format
        
        """Test converting data with empty player names to a raw text format."""
        
        emptyNameData = [{"name": "", "turns taken": 10}, {"name": "", "turns taken": 20}] # Define a list of test data with empty player names
        rawText = self.storage.convertToRawText(emptyNameData) # Convert the test data with empty names to a raw text format
        expectedText = ": 10\n: 20" # Define the expected raw text output for the test data with empty names
        assert rawText == expectedText, "Raw text conversion should correctly handle empty player names." # Assert that the converted raw text matches the expected output format confirming that empty player names are handled correctly
    
    def testConvertToRawTextMixedNameLengths(self): # Define a test method to validate converting data with mixed name lengths to a raw text format
        
        """Test converting data with mixed name lengths to a raw text format."""
        
        mixedLengthData = [{"name": "A", "turns taken": 10}, {"name": "Bob", "turns taken": 20}, {"name": "Charlie", "turns taken": 30}] # Define a list of test data with mixed name lengths
        rawText = self.storage.convertToRawText(mixedLengthData) # Convert the test data with mixed name lengths to a raw text format
        expectedText = "A: 10\nBob: 20\nCharlie: 30" # Define the expected raw text output for the test data with mixed name lengths
        assert rawText == expectedText, "Raw text conversion should correctly handle mixed name lengths." # Assert that the converted raw text matches the expected output format confirming that mixed name lengths are handled correctly
    
    def testConvertToRawTextSpecialCharactersAndUnicode(self): # Define a test method to validate converting data with both special characters and Unicode characters in player names to a raw text format
        
        """Test converting data with both special characters and Unicode characters in player names to a raw text format."""
        
        specialUnicodeData = [{"name": "Al!ce", "turns taken": 10}, {"name": "Bøb", "turns taken": 20}] # Define a list of test data with both special characters and Unicode characters in player names
        rawText = self.storage.convertToRawText(specialUnicodeData) # Convert the test data with special and Unicode characters to a raw text format
        expectedText = "Al!ce: 10\nBøb: 20" # Define the expected raw text output for the test data with special and Unicode characters
        assert rawText == expectedText, "Raw text conversion should correctly handle both special and Unicode characters in player names." # Assert that the converted raw text matches the expected output format confirming that both special and Unicode characters in player names are handled correctly
    
    def testConvertToRawTextLargeTurnsTakenValues(self): # Define a test method to validate converting data with large turns taken values to a raw text format
        
        """Test converting data with large turns taken values to a raw text format."""
        
        largeDataValues = [{"name": "Alice", "turns taken": 999999999}, {"name": "Bob", "turns taken": 888888888}] # Define a list of test data with large turns taken values
        rawText = self.storage.convertToRawText(largeDataValues) # Convert the test data with large turns taken values to a raw text format
        expectedText = "Alice: 999999999\nBob: 888888888" # Define the expected raw text output for the test data with large turns taken values
        assert rawText == expectedText, "Raw text conversion should correctly handle large turns taken values." # Assert that the converted raw text matches the expected output format confirming that large turns taken values are handled correctly
    
    def testConvertToRawTextMixedTurnsTakenAndNames(self): # Define a test method to validate converting data with mixed turns taken values and player names to a raw text format
        
        """Test converting data with mixed turns taken values and player names to a raw text format."""
        
        mixedTurnsTakenAndNames = [{"name": "Alice", "turns taken": 10}, {"name": "Bøb", "turns taken": 5}, {"name": "", "turns taken": 0}] # Define a list of test data with mixed turns taken values and player names
        rawText = self.storage.convertToRawText(mixedTurnsTakenAndNames) # Convert the test data with mixed values and names to a raw text format
        expectedText = "Alice: 10\nBøb: 5\n: 0" # Define the expected raw text output for the test data with mixed values and names
        assert rawText == expectedText, "Raw text conversion should correctly handle mixed turns taken values and player names." # Assert that the converted raw text matches the expected output format confirming that mixed turns taken values and player names are handled correctly
    
    def testConvertToRawTextSpecialCharactersInData(self): # Define a test method to validate converting data with special characters in turns taken values to a raw text format
        
        """Test converting data with special characters in turns taken values to a raw text format."""
        
        specialCharData = [{"name": "Alice", "turns taken": 10}, {"name": "Bob", "turns taken": -20}] # Define a list of test data with special characters in turns taken values (negative sign)
        rawText = self.storage.convertToRawText(specialCharData) # Convert the test data with special characters in turns taken values to a raw text format
        expectedText = "Alice: 10\nBob: -20" # Define the expected raw text output for the test data with special characters in turns taken values
        assert rawText == expectedText, "Raw text conversion should correctly handle special characters in turns taken values." # Assert that the converted raw text matches the expected output format confirming that special characters in turns taken values are handled correctly
    
    def testConvertToRawTextLargeAndSmallTurnsTaken(self): # Define a test method to validate converting data with both large and small turns taken values to a raw text format
        
        """Test converting data with both large and small turns taken values to a raw text format."""
        
        largeSmallTurnsTaken = [{"name": "Alice", "turns taken": 1000000}, {"name": "Bob", "turns taken": 1}] # Define a list of test data with both large and small turns taken values
        rawText = self.storage.convertToRawText(largeSmallTurnsTaken) # Convert the test data with large and small values to a raw text format
        expectedText = "Alice: 1000000\nBob: 1" # Define the expected raw text output for the test data with large and small values
        assert rawText == expectedText, "Raw text conversion should correctly handle both large and small turns taken values." # Assert that the converted raw text matches the expected output format confirming that both large and small turns taken values are handled correctly
    
    def testConvertToRawTextMixedSpecialCharactersAndUnicode(self): # Define a test method to validate converting data with mixed special characters and Unicode characters in player names to a raw text format
        
        """Test converting data with mixed special characters and Unicode characters in player names to a raw text format."""
        
        mixedSpecialUnicodeData = [{"name": "Al!ce", "turns taken": 10}, {"name": "Bøb", "turns taken": 20}] # Define a list of test data with mixed special characters and Unicode characters in player names
        rawText = self.storage.convertToRawText(mixedSpecialUnicodeData) # Convert the test data with mixed special and Unicode characters to a raw text format
        expectedText = "Al!ce: 10\nBøb: 20" # Define the expected raw text output for the test data with mixed special and Unicode characters
        assert rawText == expectedText, "Raw text conversion should correctly handle mixed special and Unicode characters in player names." # Assert that the converted raw text matches the expected output format confirming that mixed special and Unicode characters in player names are handled correctly
    
    def testConvertToRawTextEmptyAndNonemptyNames(self): # Define a test method to validate converting data with both empty and non-empty player names to a raw text format
        
        """Test converting data with both empty and non-empty player names to a raw text format."""
        
        emptyNonemptyNameData = [{"name": "", "turns taken": 10}, {"name": "Bob", "turns taken": 20}] # Define a list of test data with both empty and non-empty player names
        rawText = self.storage.convertToRawText(emptyNonemptyNameData) # Convert the test data with empty and non-empty names to a raw text format
        expectedText = ": 10\nBob: 20" # Define the expected raw text output for the test data with empty and non-empty names
        assert rawText == expectedText, "Raw text conversion should correctly handle both empty and non-empty player names." # Assert that the converted raw text matches the expected output format confirming that both empty and non-empty player names are handled correctly
    
    def testConvertToRawTextMixedNameLengthsAndTurnsTaken(self): # Define a test method to validate converting data with mixed name lengths and turns taken values to a raw text format
        
        """Test converting data with mixed name lengths and turns taken values to a raw text format."""
        
        mixedNameLengthTurnsTakenValues = [{"name": "A", "turns taken": 10}, {"name": "Bob", "turns taken": -5}, {"name": "Charlie", "turns taken": 0}] # Define a list of test data with mixed name lengths and turns taken values
        rawText = self.storage.convertToRawText(mixedNameLengthTurnsTakenValues) # Convert the test data with mixed name lengths and turns taken values to a raw text format
        expectedText = "A: 10\nBob: -5\nCharlie: 0" # Define the expected raw text output for the test data with mixed name lengths and turns taken values
        assert rawText == expectedText, "Raw text conversion should correctly handle mixed name lengths and turns taken values." # Assert that the converted raw text matches the expected output format confirming that mixed name lengths and turns taken values are handled correctly
    
    def testConvertToRawTextSpecialCharactersInNamesAndTurnsTaken(self): # Define a test method to validate converting data with special characters in both player names and turns taken values to a raw text format
        
        """Test converting data with special characters in both player names and turns taken values to a raw text format."""
        
        specialCharNameDataValues = [{"name": "Al!ce", "turns taken": 10}, {"name": "B@b", "turns taken": -20}] # Define a list of test data with special characters in both player names and turns taken values
        rawText = self.storage.convertToRawText(specialCharNameDataValues) # Convert the test data with special characters in names and turns taken values to a raw text format
        expectedText = "Al!ce: 10\nB@b: -20" # Define the expected raw text output for the test data with special characters in names and turns taken values
        assert rawText == expectedText, "Raw text conversion should correctly handle special characters in both player names and turns taken values." # Assert that the converted raw text matches the expected output format confirming that special characters in both player names and turns taken values are handled correctly
    
    def testConvertToRawTextUnicodeInNamesAndTurnsTaken(self): # Define a test method to validate converting data with Unicode characters in both player names and turns taken values to a raw text format
        
        """Test converting data with Unicode characters in both player names and turns taken values to a raw text format."""
        
        unicodeNameTurnsTakenValues = [{"name": "Alïce", "turns taken": 10}, {"name": "Bøb", "turns taken": -20}] # Define a list of test data with Unicode characters in both player names and turns taken values
        rawText = self.storage.convertToRawText(unicodeNameTurnsTakenValues) # Convert the test data with Unicode characters in names and turns taken values to a raw text format
        expectedText = "Alïce: 10\nBøb: -20" # Define the expected raw text output for the test data with Unicode characters in names and turns taken values
        assert rawText == expectedText, "Raw text conversion should correctly handle Unicode characters in both player names and turns taken values." # Assert that the converted raw text matches the expected output format confirming that Unicode characters in both player names and turns taken values are handled correctly
    
    def testConvertToRawTextMixedSpecialUnicodeAndEmptyNames(self): # Define a test method to validate converting data with mixed special characters, Unicode characters and empty player names to a raw text format
        
        """Test converting data with mixed special characters, Unicode characters and empty player names to a raw text format."""
        
        mixedSpecialUnicodeEmptyNames = [{"name": "Al!ce", "turns taken": 10}, {"name": "Bøb", "turns taken": -20}, {"name": "", "turns taken": 0}] # Define a list of test data with mixed special characters, Unicode characters and empty player names
        rawText = self.storage.convertToRawText(mixedSpecialUnicodeEmptyNames) # Convert the test data with mixed special, Unicode and empty names to a raw text format
        expectedText = "Al!ce: 10\nBøb: -20\n: 0" # Define the expected raw text output for the test data with mixed special, Unicode and empty names
        assert rawText == expectedText, "Raw text conversion should correctly handle mixed special characters, Unicode characters, and empty player names." # Assert that the converted raw text matches the expected output format confirming that mixed special characters, Unicode characters and empty player names are handled correctly
