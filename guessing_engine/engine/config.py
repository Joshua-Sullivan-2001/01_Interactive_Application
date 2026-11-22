# config.py: stores configuration values for the game

import json # Import the json module to read and write JSON files
from pathlib import Path # Import the Path class from the pathlib module to handle file paths

defaults = { # Define the default configuration settings for the game
    "use_rich": False, # A boolean indicating whether to use the rich library for enhanced console output
    "bot_mode": False, # A boolean indicating whether the game is in bot mode (True) or human mode (False)
    "simulation": False, # A boolean indicating whether the game is running in simulation mode (True) or normal mode (False)
    "leaderboard_sort": "insertion", # A string indicating the sorting algorithm to use for the leaderboard (default is "insertion")
    "history_path": "data/history.json", # A string indicating the file path for storing the game history in JSON format
    "log_path": "data/game.log", # A string indicating the file path for storing the game log in text format
    "attempt_limit": None, # An integer indicating the maximum number of attempts allowed for a player (None means unlimited attempts)
}

def hasRightType(name, value): # A function to check if the value is of the right type for the given setting name
    
    """Check if the value is of the right type for the given setting name"""
    
    if name in ("use_rich", "bot_mode", "simulation"): # Check if the setting name is one of the boolean settings
        return isinstance(value, bool) # Return True if the value is a boolean otherwise return False
    
    if name in ("leaderboard_sort", "history_path", "log_path"): # Check if the setting name is one of the string settings
        return isinstance(value, str) # Return True if the value is a string otherwise return False
    
    if name == "attempt_limit": # Check if the setting name is "attempt_limit"
        if value is None: # If the value is None it is still valid
            return True # Return True if the value is None (indicating unlimited attempts)
        return isinstance(value, int) and not isinstance(value, bool) and value >= 1 # Return True if the value is an integer (not a boolean) and greater than or equal to 1 otherwise return False
    
    return False # Return False if the setting name is not recognized (not in the defaults dictionary)

def loadConfig(path): # A function to load the configuration from a JSON file returning the settings and any problems
    
    """Load the configuration from a JSON file returning the settings and any problems"""
    
    settings = dict(defaults) # Create a copy of the default settings to be used as the initial configuration
    problems = [] # Initialize an empty list to hold any problems encountered while loading the configuration

    if not Path(path).is_file(): # Check if the specified path is not a file (i.e., the config file does not exist)
        problems.append("config file missing so defaults used") # Append a message to the problems list indicating that the config file is missing and defaults will be used
        return settings, problems # Return the default settings and the problems list indicating that the config file was missing

    try: # Try to open the specified config file and load its contents as JSON data
        with open(path, "r", encoding = "utf-8") as file: # Open the config file in read mode with UTF-8 encoding
            data = json.load(file) # Load the contents of the config file as JSON data into the variable 'data'
    except (OSError, ValueError): # Catch any OSError (file access issues) or ValueError (invalid JSON) that occurs while trying to open or read the config file
        problems.append("config file broken so defaults used") # Append a message to the problems list indicating that the config file is broken and defaults will be used
        return settings, problems # Return the default settings and the problems list indicating that the config file was broken

    if not isinstance(data, dict): # Check if the loaded data is not a dictionary (i.e., the config file is not in the expected format)
        problems.append("config file broken so defaults used") # Append a message to the problems list indicating that the config file is broken and defaults will be used
        return settings, problems # Return the default settings and the problems list indicating that the config file was broken

    for name in defaults: # Iterate through each setting name in the defaults dictionary
        if name in data: # Check if the setting name is present in the loaded data from the config file
            if hasRightType(name, data[name]): # Check if the value for the setting name in the loaded data is of the right type using the hasRightType function
                settings[name] = data[name] # If the value is of the right type update the settings dictionary with the value from the loaded data
            else: # If the value is not of the right type append a message to the problems list
                problems.append("wrong type for " + name) # Append a message to the problems list indicating that the value is of the wrong type for the setting name

    return settings, problems # Return the final settings dictionary and the problems list indicating any issues encountered while loading the configuration
