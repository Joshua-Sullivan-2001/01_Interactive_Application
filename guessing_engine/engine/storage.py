# storage.py: manages the storage of player turns taken and the leaderboard.

import json # Import the json module to handle reading and writing JSON data for storing player data and leaderboard information.
import os # Import the os module to interact with the operating system, such as checking for file existence and handling file paths.

class Storage: # Define the Storage class to encapsulate methods for managing player data and leaderboard data.

    """The base Storage class provides methods to manage the storage of player turns taken and leaderboard data. It handles reading from and writing to a JSON file ensuring that the data is persisted across game sessions. The class includes methods for loading turns taken, saving turns taken and managing the leaderboard."""

    def __init__(self, filename = "leaderboard.json"): # Start the constructor method for the Storage class, initializing the filename for storing leaderboard data.
        
        """Start the Storage class with a filename for the leaderboard JSON file. If no filename is provided, it defaults to 'leaderboard.json'."""
        
        self.filename = filename # Store the provided filename as an instance variable for later use in reading and writing data.

    def load_leaderboard_data(self): # Define the method to load player turns taken from the JSON file.
        
        """Loads the player turns taken from the JSON file. If the file does not exist, it returns an empty list."""
        
        if not os.path.exists(self.filename): # Check if the leaderboard JSON file exists.
            return [] # If the file does not exist return an empty list indicating no turns taken are available.
        else: # If the file exists proceed to read the turns taken from it.
            with open(self.filename, "r") as file: # Open the leaderboard JSON file in read mode.
                return json.load(file) # Load and return the player turns taken from the JSON file.
            
    def save_leaderboard_data(self, scores): # Define the method to save player turns taken to the JSON file.
        
        """Saves the player initials and turns taken to the JSON file. It overwrites any existing data in the file."""
        
        with open(self.filename, "w") as file: # Open the leaderboard JSON file in write mode.
            json.dump(scores, file) # Write the provided player initials and turns taken to the JSON file in JSON format.
    
    # Utility methods for managing the leaderboard data.
    
    def clear_leaderboard_data(self): # Define the method to clear all player data from the JSON file.
        
        """Clears all player data from the JSON file by overwriting it with an empty list."""
        
        with open(self.filename, "w") as file: # Open the leaderboard JSON file in write mode.
            json.dump([], file) # Write an empty list to the JSON file clearing all data.
    
    def convert_to_raw_text(self, scores): # Define the method to convert the list of player data into a raw text format for display.
        
        """Converts the list of player data into a raw text format for display purposes."""
        
        return "\n".join([f"{score['name']}: {score['score']}" for score in scores]) # Join each player's name and turns taken into a single string separated by newlines.