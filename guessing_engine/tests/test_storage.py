# test_storage.py: tests the storage functionality for saving and loading game data.

import os # Import the os module to interact with the operating system, such as checking for file existence and handling file paths.
import json # Import the json module to handle reading and writing JSON data for storing player data and leaderboard information.
from guessing_engine.engine.storage import Storage # Import the Storage class from the storage module

class Test_storage:
    
    """A test class to validate the functionality of the Storage class including loading, saving and clearing player data as well as converting data to a raw text format."""

    def setup_method(self, method): # Define a setup method that runs before each test method to prepare the test environment.
        
        """Setup method to initialize the Storage class and prepare the test environment before each test method."""
        
        self.test_filename = "test_leaderboard.json" # Define a test filename for the leaderboard JSON file to avoid issues with the actual game data.
        self.storage = Storage(self.test_filename) # Create an instance of the Storage class using the test filename.
        self.storage.clear_leaderboard_data() # Clear any existing data (Which shouldn't be present) in the test leaderboard file to ensure a clean state for testing.
    
    def cleanup_method(self, method): # Define a cleaning method that runs after each test method to clean up the test environment.
        
        """Method to clean up the test save file after each test method."""
        
        if os.path.exists(self.test_filename): # Check if the test leaderboard JSON file exists.
            os.remove(self.test_filename) # Remove the test leaderboard JSON file to clean up after tests.
    
    def test_load_data_empty(self): # Define a test method to validate loading data from an empty leaderboard file.
        
        """Test loading data from an empty leaderboard file."""
        
        data = self.storage.load_leaderboard_data() # Load leaderboard data from the test leaderboard file.
        assert data == [], "Loading from an empty file should return an empty list." # Assert that the loaded data are an empty list indicating no data are present.
    
    def test_save_and_load_data(self): # Define a test method to validate saving and loading data to and from the leaderboard file.
        
        """Test saving and loading data to and from the leaderboard file."""
        
        test_data = [{"name": "Alice", "turns taken": 10}, {"name": "Bob", "turns taken": 20}] # Define a list of test data to save.
        self.storage.save_leaderboard_data(test_data) # Save the test data to the leaderboard file.
        loaded_data = self.storage.load_leaderboard_data() # Load the data back from the leaderboard file.
        assert loaded_data == test_data, "Loaded data should match the saved data." # Assert that the loaded data match the originally saved test data.
    
    def test_clear_data(self): # Define a test method to validate clearing data from the leaderboard file.
        
        """Test clearing data from the leaderboard file."""
        
        test_data = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save.
        self.storage.save_leaderboard_data(test_data) # Save the test data to the leaderboard file.
        self.storage.clear_leaderboard_data() # Clear the data from the leaderboard file.
        loaded_data = self.storage.load_leaderboard_data() # Load the data back from the leaderboard file.
        assert loaded_data == [], "After clearing, loading should return an empty list." # Assert that the loaded data are an empty list, indicating that the data were successfully cleared.
    
    def test_convert_to_raw_text(self): # Define a test method to validate converting data to a raw text format.
        
        """Test converting data to a raw text format."""
        
        test_data = [{"name": "Alice", "turns taken": 10}, {"name": "Bob", "turns taken": 20}] # Define a list of test data to convert.
        raw_text = self.storage.convert_to_raw_text(test_data) # Convert the test data to a raw text format.
        expected_text = "Alice: 10\nBob: 20" # Define the expected raw text output for the test data.
        assert raw_text == expected_text, "Raw text conversion should match the expected format." # Assert that the converted raw text matches the expected output format.
    
    def test_load_data_nonexistent_file(self): # Define a test method to validate loading data from a nonexistent leaderboard file.
        
        """Test loading data from a nonexistent leaderboard file."""
        
        non_existent_storage = Storage("nonexistent_file.json") # Create an instance of the Storage class with a filename that does not exist.
        data = non_existent_storage.load_leaderboard_data() # Attempt to load data from the nonexistent file.
        assert data == [], "Loading from a nonexistent file should return an empty list." # Assert that the loaded data is an empty list, indicating that no data is present in a nonexistent file.
    
    def test_save_data_overwrite(self): # Define a test method to validate that saving data overwrites existing data in the leaderboard file.
        
        """Test that saving data overwrites existing data in the leaderboard file."""
        
        initial_data = [{"name": "Alice", "turns taken": 10}] # Define an initial list of test data to save.
        self.storage.save_leaderboard_data(initial_data) # Save the initial test data to the leaderboard file.
        new_data = [{"name": "Bob", "turns taken": 20}] # Define a new list of test data to overwrite the initial data.
        self.storage.save_leaderboard_data(new_data) # Save the new test data to the leaderboard file, overwriting the initial data.
        loaded_data = self.storage.load_leaderboard_data() # Load the data back from the leaderboard file.
        assert loaded_data == new_data, "Loaded data should match the newly saved data after overwrite." # Assert that the loaded data match the newly saved test data, confirming that the overwrite was successful.
    
    def test_convert_to_raw_text_empty(self): # Define a test method to validate converting an empty list of data to a raw text format.
        
        """Test converting an empty list of data to a raw text format."""
        
        empty_data = [] # Define an empty list of data.
        raw_text = self.storage.convert_to_raw_text(empty_data) # Convert the empty list of data to a raw text format.
        assert raw_text == "", "Converting an empty list should return an empty string." # Assert that the converted raw text is an empty string, indicating that there is no data to display.
    
    def test_convert_to_raw_text_single_entry(self): # Define a test method to validate converting a single player entry to a raw text format.
        
        """Test converting a single player entry to a raw text format."""
        
        single_player_data = [{"name": "Alice", "turns taken": 10}] # Define a list containing a single player entry.
        raw_text = self.storage.convert_to_raw_text(single_player_data) # Convert the single player entry to a raw text format.
        expected_text = "Alice: 10" # Define the expected raw text output for the single player entry.
        assert raw_text == expected_text, "Raw text conversion for a single entry should match the expected format." # Assert that the converted raw text matches the expected output format for a single player entry.
    
    def test_load_data_invalid_json(self): # Define a test method to validate loading data from a leaderboard file containing invalid JSON data.
        
        """Test loading data from a leaderboard file containing invalid JSON data."""
        
        with open(self.test_filename, "w") as file: # Open the test leaderboard JSON file in write mode.
            file.write("Invalid JSON content") # Write invalid JSON content to the file.
        try: # Attempt to load data from the file containing invalid JSON data.
            self.storage.load_leaderboard_data() # Load data from the test leaderboard file.
            assert False, "Loading from a file with invalid JSON should raise a JSONDecodeError." # If no exception is raised, assert False to indicate the test failed.
        except json.JSONDecodeError: # Catch the expected JSONDecodeError exception.
            pass # If the exception is raised, pass the test as it is the expected behavior.
    
    def test_save_data_creates_file(self): # Define a test method to validate that saving data creates the leaderboard file if it does not exist.
        
        """Test that saving data creates the leaderboard file if it does not exist."""
        
        if os.path.exists(self.test_filename): # Check if the test leaderboard JSON file exists.
            os.remove(self.test_filename) # Remove the test leaderboard JSON file to ensure it does not exist before the test.
        test_data = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save.
        self.storage.save_leaderboard_data(test_data) # Save the test data to the leaderboard file.
        assert os.path.exists(self.test_filename), "Saving data should create the leaderboard file if it does not exist." # Assert that the leaderboard file now exists, confirming that saving data created the file.
    
    def test_clear_data_creates_file(self): # Define a test method to validate that clearing data creates the leaderboard file if it does not exist.
        
        """Test that clearing data creates the leaderboard file if it does not exist."""
        
        if os.path.exists(self.test_filename): # Check if the test leaderboard JSON file exists.
            os.remove(self.test_filename) # Remove the test leaderboard JSON file to ensure it does not exist before the test.
        self.storage.clear_leaderboard_data() # Clear the data from the leaderboard file.
        assert os.path.exists(self.test_filename), "Clearing data should create the leaderboard file if it does not exist." # Assert that the leaderboard file now exists, confirming that clearing data created the file.
    
    def test_save_data_invalid_data(self): # Define a test method to validate that saving invalid data raises an appropriate exception.
        
        """Test that saving invalid data raises an appropriate exception."""
        
        invalid_data = "This is not a valid list" # Define invalid data that is not a list of data.
        try: # Attempt to save the invalid data to the leaderboard file.
            self.storage.save_leaderboard_data(invalid_data) # Save the invalid data to the leaderboard file.
            assert False, "Saving invalid data should raise a TypeError." # If no exception is raised, assert False to indicate the test failed.
        except TypeError: # Catch the expected TypeError exception.
            pass # If the exception is raised, pass the test as it is the expected behavior.
    
    def test_load_data_after_clear(self): # Define a test method to validate that loading data after clearing returns an empty list.
        
        """Test that loading data after clearing returns an empty list."""
        
        test_data = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save.
        self.storage.save_leaderboard_data(test_data) # Save the test data to the leaderboard file.
        self.storage.clear_leaderboard_data() # Clear the data from the leaderboard file.
        loaded_data = self.storage.load_leaderboard_data() # Load the data back from the leaderboard file.
        assert loaded_data == [], "After clearing, loading should return an empty list." # Assert that the loaded data is an empty list, indicating that the data was successfully cleared.
    
    def test_save_data_multiple_times(self): # Define a test method to validate that saving data multiple times overwrites the previous data.
        
        """Test that saving data multiple times overwrites the previous data."""
        
        first_data = [{"name": "Alice", "turns taken": 10}] # Define the first list of test data to save.
        self.storage.save_leaderboard_data(first_data) # Save the first test data to the leaderboard file.
        second_data = [{"name": "Bob", "turns taken": 20}] # Define the second list of test data to save.
        self.storage.save_leaderboard_data(second_data) # Save the second test data to the leaderboard file, overwriting the first data.
        loaded_data = self.storage.load_leaderboard_data() # Load the data back from the leaderboard file.
        assert loaded_data == second_data, "Loaded data should match the last saved data after multiple saves." # Assert that the loaded data match the last saved test data, confirming that multiple saves overwrite previous data.
    
    def test_clear_leaderboard_data_multiple_times(self): # Define a test method to validate that clearing data multiple times does not cause errors and always results in an empty list.
        
        """Test that clearing data multiple times does not cause errors and always results in an empty list."""
        
        test_data = [{"name": "Alice", "turns taken": 10}] # Define a list of test data to save.
        self.storage.save_leaderboard_data(test_data) # Save the test data to the leaderboard file.
        self.storage.clear_leaderboard_data() # Clear the data from the leaderboard file.
        self.storage.clear_leaderboard_data() # Clear the data again to test multiple clears.
        loaded_data = self.storage.load_leaderboard_data() # Load the data back from the leaderboard file.
        assert loaded_data == [], "After multiple clears, loading should return an empty list." # Assert that the loaded data is an empty list, indicating that multiple clears do not cause errors and result in an empty state.
    
    def test_convert_to_raw_text_special_characters(self): # Define a test method to validate converting data with special characters to a raw text format.
        
        """Test converting data with special characters to a raw text format."""
        
        special_data = [{"name": "Al!ce", "turns taken": 10}, {"name": "B@b", "turns taken": 20}] # Define a list of test data with special characters in player names.
        raw_text = self.storage.convert_to_raw_text(special_data) # Convert the test data with special characters to a raw text format.
        expected_text = "Al!ce: 10\nB@b: 20" # Define the expected raw text output for the test data with special characters.
        assert raw_text == expected_text, "Raw text conversion should correctly handle special characters in names." # Assert that the converted raw text matches the expected output format, confirming that special characters are handled correctly.
    
    def test_convert_to_raw_text_large_numbers(self): # Define a test method to validate converting data with large numbers to a raw text format.
        
        """Test converting data with large numbers to a raw text format."""
        
        large_turns = [{"name": "Alice", "turns taken": 1000000}, {"name": "Bob", "turns taken": 2000000}] # Define a list of test data with large turns taken values.
        raw_text = self.storage.convert_to_raw_text(large_turns) # Convert the test data with large numbers to a raw text format.
        expected_text = "Alice: 1000000\nBob: 2000000" # Define the expected raw text output for the test data with large numbers.
        assert raw_text == expected_text, "Raw text conversion should correctly handle large numbers." # Assert that the converted raw text matches the expected output format, confirming that large numbers are handled correctly.
    
    def test_convert_to_raw_text_special_characters_in_names(self): # Define a test method to validate converting data with special characters in player names to a raw text format.
        
        """Test converting data with special characters in player names to a raw text format."""
        
        special_char_data = [{"name": "Al!ce", "turns taken": 10}, {"name": "B@b", "turns taken": 20}] # Define a list of test data with special characters in player names.
        raw_text = self.storage.convert_to_raw_text(special_char_data) # Convert the test data with special characters to a raw text format.
        expected_text = "Al!ce: 10\nB@b: 20" # Define the expected raw text output for the test data with special characters.
        assert raw_text == expected_text, "Raw text conversion should correctly handle special characters in player names." # Assert that the converted raw text matches the expected output format, confirming that special characters in player names are handled correctly.
    
    def test_convert_to_raw_text_unicode_names(self): # Define a test method to validate converting data with Unicode characters in player names to a raw text format.
        
        """Test converting data with Unicode characters in player names to a raw text format."""
        
        unicode_data = [{"name": "Alïce", "turns taken": 10}, {"name": "Bøb", "turns taken": 20}] # Define a list of test data with Unicode characters in player names.
        raw_text = self.storage.convert_to_raw_text(unicode_data) # Convert the test data with Unicode characters to a raw text format.
        expected_text = "Alïce: 10\nBøb: 20" # Define the expected raw text output for the test data with Unicode characters.
        assert raw_text == expected_text, "Raw text conversion should correctly handle Unicode characters in player names." # Assert that the converted raw text matches the expected output format, confirming that Unicode characters in player names are handled correctly.
    
    def test_convert_to_raw_text_empty_names(self): # Define a test method to validate converting data with empty player names to a raw text format.
        
        """Test converting data with empty player names to a raw text format."""
        
        empty_name_data = [{"name": "", "turns taken": 10}, {"name": "", "turns taken": 20}] # Define a list of test data with empty player names.
        raw_text = self.storage.convert_to_raw_text(empty_name_data) # Convert the test data with empty names to a raw text format.
        expected_text = ": 10\n: 20" # Define the expected raw text output for the test data with empty names.
        assert raw_text == expected_text, "Raw text conversion should correctly handle empty player names." # Assert that the converted raw text matches the expected output format, confirming that empty player names are handled correctly.
    
    def test_convert_to_raw_text_mixed_name_lengths(self): # Define a test method to validate converting data with mixed name lengths to a raw text format.
        
        """Test converting data with mixed name lengths to a raw text format."""
        
        mixed_length_data = [{"name": "A", "turns taken": 10}, {"name": "Bob", "turns taken": 20}, {"name": "Charlie", "turns taken": 30}] # Define a list of test data with mixed name lengths.
        raw_text = self.storage.convert_to_raw_text(mixed_length_data) # Convert the test data with mixed name lengths to a raw text format.
        expected_text = "A: 10\nBob: 20\nCharlie: 30" # Define the expected raw text output for the test data with mixed name lengths.
        assert raw_text == expected_text, "Raw text conversion should correctly handle mixed name lengths." # Assert that the converted raw text matches the expected output format, confirming that mixed name lengths are handled correctly.
    
    def test_convert_to_raw_text_special_characters_and_unicode(self): # Define a test method to validate converting data with both special characters and Unicode characters in player names to a raw text format.
        
        """Test converting data with both special characters and Unicode characters in player names to a raw text format."""
        
        special_unicode_data = [{"name": "Al!ce", "turns taken": 10}, {"name": "Bøb", "turns taken": 20}] # Define a list of test data with both special characters and Unicode characters in player names.
        raw_text = self.storage.convert_to_raw_text(special_unicode_data) # Convert the test data with special and Unicode characters to a raw text format.
        expected_text = "Al!ce: 10\nBøb: 20" # Define the expected raw text output for the test data with special and Unicode characters.
        assert raw_text == expected_text, "Raw text conversion should correctly handle both special and Unicode characters in player names." # Assert that the converted raw text matches the expected output format, confirming that both special and Unicode characters in player names are handled correctly.
    
    def test_convert_to_raw_text_large_turns_taken_values(self): # Define a test method to validate converting data with large turns taken values to a raw text format.
        
        """Test converting data with large turns taken values to a raw text format."""
        
        large_data_values = [{"name": "Alice", "turns taken": 999999999}, {"name": "Bob", "turns taken": 888888888}] # Define a list of test data with large turns taken values.
        raw_text = self.storage.convert_to_raw_text(large_data_values) # Convert the test data with large turns taken values to a raw text format.
        expected_text = "Alice: 999999999\nBob: 888888888" # Define the expected raw text output for the test data with large turns taken values.
        assert raw_text == expected_text, "Raw text conversion should correctly handle large turns taken values." # Assert that the converted raw text matches the expected output format, confirming that large turns taken values are handled correctly.
    
    def test_convert_to_raw_text_mixed_turns_taken_and_names(self): # Define a test method to validate converting data with mixed turns taken values and player names to a raw text format.
        
        """Test converting data with mixed turns taken values and player names to a raw text format."""
        
        mixed_turns_taken_and_names = [{"name": "Alice", "turns taken": 10}, {"name": "Bøb", "turns taken": 5}, {"name": "", "turns taken": 0}] # Define a list of test data with mixed turns taken values and player names.
        raw_text = self.storage.convert_to_raw_text(mixed_turns_taken_and_names) # Convert the test data with mixed values and names to a raw text format.
        expected_text = "Alice: 10\nBøb: 5\n: 0" # Define the expected raw text output for the test data with mixed values and names.
        assert raw_text == expected_text, "Raw text conversion should correctly handle mixed turns taken values and player names." # Assert that the converted raw text matches the expected output format, confirming that mixed turns taken values and player names are handled correctly.
    
    def test_convert_to_raw_text_special_characters_in_data(self): # Define a test method to validate converting data with special characters in turns taken values to a raw text format.
        
        """Test converting data with special characters in turns taken values to a raw text format."""
        
        special_char_data = [{"name": "Alice", "turns taken": 10}, {"name": "Bob", "turns taken": -20}] # Define a list of test data with special characters in turns taken values (negative sign).
        raw_text = self.storage.convert_to_raw_text(special_char_data) # Convert the test data with special characters in turns taken values to a raw text format.
        expected_text = "Alice: 10\nBob: -20" # Define the expected raw text output for the test data with special characters in turns taken values.
        assert raw_text == expected_text, "Raw text conversion should correctly handle special characters in turns taken values." # Assert that the converted raw text matches the expected output format, confirming that special characters in turns taken values are handled correctly. 
    
    def test_convert_to_raw_text_large_and_small_turns_taken(self): # Define a test method to validate converting data with both large and small turns taken values to a raw text format.
        
        """Test converting data with both large and small turns taken values to a raw text format."""
        
        large_small_turns_taken = [{"name": "Alice", "turns taken": 1000000}, {"name": "Bob", "turns taken": 1}] # Define a list of test data with both large and small turns taken values.
        raw_text = self.storage.convert_to_raw_text(large_small_turns_taken) # Convert the test data with large and small values to a raw text format.
        expected_text = "Alice: 1000000\nBob: 1" # Define the expected raw text output for the test data with large and small values.
        assert raw_text == expected_text, "Raw text conversion should correctly handle both large and small turns taken values." # Assert that the converted raw text matches the expected output format, confirming that both large and small turns taken values are handled correctly.
    
    def test_convert_to_raw_text_mixed_special_characters_and_unicode(self): # Define a test method to validate converting data with mixed special characters and Unicode characters in player names to a raw text format.
        
        """Test converting data with mixed special characters and Unicode characters in player names to a raw text format."""
        
        mixed_special_unicode_data = [{"name": "Al!ce", "turns taken": 10}, {"name": "Bøb", "turns taken": 20}] # Define a list of test data with mixed special characters and Unicode characters in player names.
        raw_text = self.storage.convert_to_raw_text(mixed_special_unicode_data) # Convert the test data with mixed special and Unicode characters to a raw text format.
        expected_text = "Al!ce: 10\nBøb: 20" # Define the expected raw text output for the test data with mixed special and Unicode characters.
        assert raw_text == expected_text, "Raw text conversion should correctly handle mixed special and Unicode characters in player names." # Assert that the converted raw text matches the expected output format, confirming that mixed special and Unicode characters in player names are handled correctly.
    
    def test_convert_to_raw_text_empty_and_nonempty_names(self): # Define a test method to validate converting data with both empty and non-empty player names to a raw text format.
        
        """Test converting data with both empty and non-empty player names to a raw text format."""
        
        empty_nonempty_name_data = [{"name": "", "turns taken": 10}, {"name": "Bob", "turns taken": 20}] # Define a list of test data with both empty and non-empty player names.
        raw_text = self.storage.convert_to_raw_text(empty_nonempty_name_data) # Convert the test data with empty and non-empty names to a raw text format.
        expected_text = ": 10\nBob: 20" # Define the expected raw text output for the test data with empty and non-empty names.
        assert raw_text == expected_text, "Raw text conversion should correctly handle both empty and non-empty player names." # Assert that the converted raw text matches the expected output format, confirming that both empty and non-empty player names are handled correctly.
    
    def test_convert_to_raw_text_mixed_name_lengths_and_turns_taken(self): # Define a test method to validate converting data with mixed name lengths and turns taken values to a raw text format.
        
        """Test converting data with mixed name lengths and turns taken values to a raw text format."""
        
        mixed_name_length_turns_taken_values = [{"name": "A", "turns taken": 10}, {"name": "Bob", "turns taken": -5}, {"name": "Charlie", "turns taken": 0}] # Define a list of test data with mixed name lengths and turns taken values.
        raw_text = self.storage.convert_to_raw_text(mixed_name_length_turns_taken_values) # Convert the test data with mixed name lengths and turns taken values to a raw text format.
        expected_text = "A: 10\nBob: -5\nCharlie: 0" # Define the expected raw text output for the test data with mixed name lengths and turns taken values.
        assert raw_text == expected_text, "Raw text conversion should correctly handle mixed name lengths and turns taken values." # Assert that the converted raw text matches the expected output format, confirming that mixed name lengths and turns taken values are handled correctly.
    
    def test_convert_to_raw_text_special_characters_in_names_and_turns_taken(self): # Define a test method to validate converting data with special characters in both player names and turns taken values to a raw text format.
        """Test converting data with special characters in both player names and turns taken values to a raw text format."""
        
        special_char_name_data_values = [{"name": "Al!ce", "turns taken": 10}, {"name": "B@b", "turns taken": -20}] # Define a list of test data with special characters in both player names and turns taken values.
        raw_text = self.storage.convert_to_raw_text(special_char_name_data_values) # Convert the test data with special characters in names and turns taken values to a raw text format.
        expected_text = "Al!ce: 10\nB@b: -20" # Define the expected raw text output for the test data with special characters in names and turns taken values.
        assert raw_text == expected_text, "Raw text conversion should correctly handle special characters in both player names and turns taken values." # Assert that the converted raw text matches the expected output format, confirming that special characters in both player names and turns taken values are handled correctly.
    
    def test_convert_to_raw_text_unicode_in_names_and_turns_taken(self): # Define a test method to validate converting data with Unicode characters in both player names and turns taken values to a raw text format.
        """Test converting data with Unicode characters in both player names and turns taken values to a raw text format."""
        
        unicode_name_turns_taken_values = [{"name": "Alïce", "turns taken": 10}, {"name": "Bøb", "turns taken": -20}] # Define a list of test data with Unicode characters in both player names and turns taken values.
        raw_text = self.storage.convert_to_raw_text(unicode_name_turns_taken_values) # Convert the test data with Unicode characters in names and turns taken values to a raw text format.
        expected_text = "Alïce: 10\nBøb: -20" # Define the expected raw text output for the test data with Unicode characters in names and turns taken values.
        assert raw_text == expected_text, "Raw text conversion should correctly handle Unicode characters in both player names and turns taken values." # Assert that the converted raw text matches the expected output format, confirming that Unicode characters in both player names and turns taken values are handled correctly.
    
    def test_convert_to_raw_text_mixed_special_unicode_and_empty_names(self): # Define a test method to validate converting data with mixed special characters, Unicode characters, and empty player names to a raw text format.
        
        """Test converting data with mixed special characters, Unicode characters and empty player names to a raw text format."""
        
        mixed_special_unicode_empty_names = [{"name": "Al!ce", "turns taken": 10}, {"name": "Bøb", "turns taken": -20}, {"name": "", "turns taken": 0}] # Define a list of test data with mixed special characters, Unicode characters, and empty player names.
        raw_text = self.storage.convert_to_raw_text(mixed_special_unicode_empty_names) # Convert the test data with mixed special, Unicode, and empty names to a raw text format.
        expected_text = "Al!ce: 10\nBøb: -20\n: 0" # Define the expected raw text output for the test data with mixed special, Unicode, and empty names.
        assert raw_text == expected_text, "Raw text conversion should correctly handle mixed special characters, Unicode characters, and empty player names." # Assert that the converted raw text matches the expected output format, confirming that mixed special characters, Unicode characters, and empty player names are handled correctly.
    