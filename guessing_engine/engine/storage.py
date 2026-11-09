# storage.py: manages the storage of player scores and the leaderboard.

import json # Import the json module to handle reading and writing JSON data for storing player scores and leaderboard information.
import os # Import the os module to interact with the operating system, such as checking for file existence and handling file paths.

class Storage: # Define the Storage class to encapsulate methods for managing player scores and leaderboard data.
    