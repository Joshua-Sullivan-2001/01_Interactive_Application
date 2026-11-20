# storage.py: manages the storage of player turns taken and the leaderboard

import json # Import the json module to handle reading and writing JSON data for storing player data and leaderboard information
import os # Import the os module to interact with the operating system, such as checking for file existence and handling file paths
from datetime import datetime # Import the datetime module to handle timestamps for when player data is recorded allowing for tracking of when turns were taken

class Storage: # Define the Storage class to encapsulate methods for managing player data and leaderboard data

    """The base Storage class provides methods to manage the storage of player turns taken and leaderboard data. It handles reading from and writing to a JSON file ensuring that the data is persisted across game sessions. The class includes methods for loading turns taken, saving turns taken and managing the leaderboard."""

    def __init__(self, filename = "leaderboard.json"): # Start the constructor method for the Storage class, initializing the filename for storing leaderboard data
        
        """Start the Storage class with a filename for the leaderboard JSON file. If no filename is provided, it defaults to 'leaderboard.json'."""
        
        self.filename = filename # Store the provided filename as an instance variable for later use in reading and writing data
        self.problems = [] # Initialize an empty list to hold any problems encountered during storage operations. This can be used for error handling or logging purposes
        # TODO: Add file path later to ensure all data is stored in "guessing_engine/engine/data" folder

    def loadLeaderboardData(self): # Define the method to load player turns taken from the JSON file
        
        """Loads the player turns taken from the JSON file. If the file does not exist it returns an empty list."""
        
        self.problems = [] # Reset the problems list to ensure it only contains issues from the current load operation
        
        if not os.path.exists(self.filename): # Check if the leaderboard JSON file exists
            return [] # If the file does not exist return an empty list indicating no turns taken are available
        try: # Try to open the leaderboard JSON file and read its contents
            with open(self.filename, "r", encoding = "utf-8") as file: # Open the leaderboard JSON file in read mode
                text = file.read() # Read the entire contents of the file into a string variable
        except os.error: # Catch any OS-related errors that occur while trying to open or read the file
                self.problems.append("History file not found") # Append the error message to the problems list for logging or debugging purposes
                return [] # Return an empty list indicating that no valid turns taken data could be loaded from the file due to the read error
        if text.strip() == "": # Check if the file is empty or contains only whitespace
            return [] # If the file is empty return an empty list indicating no turns taken are available
        
        try: # Try to parse the JSON data from the file contents
            data = json.loads(text) # Attempt to parse the JSON data from the file contents
        except ValueError: # Catch any ValueError that occurs during JSON parsing which indicates that the file contents are not valid JSON
            data = None # Set data to None to indicate that parsing failed
        
        if not isinstance(data, list): # Check if the parsed data is not a list which is the expected format for player turns taken
            self.problems.append("Data is not a list.") # Append an error message to the problems list indicating that the data format is incorrect
            return [] # Return an empty list indicating that no valid turns taken data could be loaded from the file due to incorrect data format
        
        good = [] # Initialize an empty list to hold valid player data entries
        for entry in data: # Iterate over each entry in the parsed data list
            if self.isGoodEntry(entry): # Check if the current entry is a valid player data entry using the isGoodEntry method
                good.append(entry) # If the entry is valid, append it to the good list
            else: # If the entry is not valid, it is ignored and not added to the good list
                self.problems.append(f"Invalid entry: {entry}") # Append an error message to the problems list indicating that the entry is invalid
        return good # Return the list of valid player data entries that were successfully loaded from the JSON
    
    def isGoodEntry(self, entry): # Define the method to check if a given entry is a valid player data entryy
        
        """Checks if the given entry is a valid player data entry. A valid entry is a dictionary that contains the keys 'initials', 'turns' and 'timestamp' with appropriate data types"""
        
        return isinstance(entry, dict) and isinstance(entry.get("initials"), str) and isinstance(entry.get("turns"), int) and isinstance(entry.get("timestamp"), str) # Check if the entry is a dictionary and contains the required keys with the correct data types. The 'initials' key should be a string, 'turns' should be an integer and 'timestamp' should be a string. Return True if all conditions are met otherwise return False

    def saveLeaderboardData(self, data): # Define the method to save player turns taken to the JSON file
        
        """Saves the leaderboard data to a JSON file."""
        
        if not isinstance(data,list): # Check if the provided data is not a list which is the expected format for player turns taken
            return False # If the data is not a list return False indicating that the save operation failed due to incorrect data format
        
        temp_filename = self.filename + ".tmp" # Create a temporary filename by appending ".tmp" to the original filename. This is used to write the data to a temporary file before replacing the original file to ensure data integrity
        try: # Try to write the data to the temporary file and then replace the original file with the temporary file
            folder = os.path.dirname(self.filename) # Get the directory path of the original filename to ensure that the directory exists before writing the temporary file
            if folder != "": # Check if the folder path is not empty which indicates that the file is not in the current working directory
                os.makedirs(folder, exist_ok = True) # Create the directory path if it does not exist. The exist_ok parameter is set to True to avoid raising an error if the directory already exists
            with open(temp_filename, "w", encoding = "utf-8") as file: # Open the temporary file in write mode with UTF-8 encoding to write the leaderboard data
                json.dump(data, file, indent = 4) # Write the provided data to the temporary file in JSON format with an indentation of 4 spaces for readability
            os.replace(temp_filename, self.filename) # Replace the original leaderboard JSON file with the temporary file to ensure that the data is saved atomically. This helps prevent data corruption in case of a failure during the write operation
            return True # Return True indicating that the save operation was successful
        except (os.error, TypeError, ValueError): # Catch any OS-related errors, TypeErrors or ValueErrors that occur during the file write operation or JSON creation
            self.problems.append("Failed to save leaderboard data.") # Append an error message to the problems list indicating that the save operation failed due to an error during file write or JSON creation
            return False # Return False indicating that the save operation failed due to an error during file write or JSON creation

    # Utility methods for managing the leaderboard data
    
    def clearLeaderboardData(self): # Define the method to clear the leaderboard data by saving an empty list to the JSON file
        
        """Clears the leaderboard data by saving an empty list to the JSON file."""
        
        self.saveLeaderboardData([]) # Save an empty list to the JSON file to clear the leaderboard data

    def convertToRawText(self, data): # Define the method to convert the leaderboard data to a raw text format for displaying the leaderboard
        
        """Converts the leaderboard data to a raw text format. Each entry's initials, turns and timestamp are joined with a newline character to create a human-readable format for displaying the leaderboard."""
        
        return "\n".join([f"{entry['initials']} - {entry['turns']} turns - {entry['timestamp']}" for entry in data]) # Convert the leaderboard data to a raw text format by joining each entry's initials, turns and timestamp with a newline character. This can be used for displaying the leaderboard in a human-readable format
    
    def logEvent(self, text): # Define the method to log an event to a log file with a timestamp
        
        """Logs an event to a log file with a timestamp. The log file is created if it does not exist and the event is appended to the file. If there is an error while logging the event it is recorded in the problems list."""
        
        try: # Try to log the event to the log file with a timestamp
            folder = os.path.dirname(self.filename) # Get the directory path of the log file to ensure that the directory exists before writing the log entry
            if folder != "": # Check if the folder path is not empty which indicates that the log file is not in the current working directory
                os.makedirs(folder, exist_ok = True) # Create the directory path if it does not exist. The exist_ok parameter is set to True to avoid raising an error if the directory already exists
            stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Get the current timestamp in the format "YYYY-MM-DD HH:MM:SS" to prepend to the log entry for tracking when the event occurred
            with open(self.filename, "a", encoding = "utf-8") as file: # Open the log file in append mode with UTF-8 encoding to add the new log entry without overwriting existing entries
                file.write(f"[{stamp}] {text}\n") # Write the log entry to the log file with the timestamp prepended. Each log entry is written on a new line for readability
        except os.error: # Catch any OS-related errors that occur while trying to open or write to the log file
            self.problems.append("Failed to log event.") # Append an error message to the problems list indicating that the log operation failed due to an error during file write
            pass # Pass to continue execution without raising an exception allowing the program to continue running even if logging fails
