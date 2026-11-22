# main.py: entry point for the guessing engine application

from datetime import datetime # Import the datetime module to work with date and time for logging purposes

from engine.bot import binaryBot, randomBot # Import the binaryBot and randomBot classes from the bot module in the engine package to create bot instances for gameplay
from engine.config import loadConfig # Import the loadConfig function from the config module in the engine package to load configuration settings for the application
from engine.display import createDisplay # Import the createDisplay function from the display module in the engine package to create a display object for user interface
from engine.game import Game # Import the Game class from the game module in the engine package to create and manage game instances
from engine.leaderboard import Leaderboard, makeRecord # Import the Leaderboard class and makeRecord function from the leaderboard module in the engine package to manage and create leaderboard records
from engine.simulation import runSimulation, summarizeResults, timeSort # Import the runSimulation, summarizeResults and timeSort functions from the simulation module in the engine package to run game simulations and analyze sorting performance
from engine.sorting import getSorter # Import the getSorter function from the sorting module in the engine package to retrieve sorting algorithms for leaderboard management
from engine.storage import Storage # Import the Storage class from the storage module in the engine package to manage persistent storage of game data and leaderboard records

simulationGames = 1000000 # Define a constant for the number of games to be played during the simulation for performance testing and analysis
simulationSeed = 1 # Define a constant for the random seed to ensure reproducibility of the simulation results by initializing the random number generator with a fixed value


def menuOptions(settings): # A function that generates a list of menu options based on the provided settings dictionary. It returns a list of strings representing the available options for the user to choose from
    
    """This function generates a list of menu options based on the provided settings dictionary. It returns a list of strings representing the available options for the user to choose from."""
    
    options = ["Play a Game", "Session Leaderboard", "All-Time Leaderboard"] # Initialize the options list with default menu options for playing a game and viewing leaderboards
    
    if settings["bot_mode"]: # Check if bot mode is enabled in the settings dictionary
        options.append("Watch a Bot Game") # If bot mode is enabled, add the option to watch a bot game to the options list
    else: # If bot mode is disabled
        options.append("Bot mode is disabled in the config file. To enable it set 'bot_mode' to True in the config file.") # Add a message indicating that bot mode is disabled and instructions to enable it in the config file
    
    if settings["simulation_mode"]: # Check if simulation mode is enabled in the settings dictionary
        options.append("Run Bot Simulation") # If simulation mode is enabled add the option to run a bot simulation to the options list
        options.append("Compare Sort Algorithms") # If simulation mode is enabled add the option to compare sorting algorithms to the options list
    else: # If simulation mode is disabled
        options.append("Simulation mode is disabled in the config file.") # Add a message indicating that simulation mode is disabled in the config file
        options.append("Compare Sort Algorithms is disabled. To enable both set 'simulation_mode' to True in the config file.") # Add a message indicating that the compare sort algorithms option is disabled and instructions to enable it in the config file
    
    options.append("Exit Program") # Add the option to exit the program to the options list
    return options # Return the final list of menu options to be displayed to the user

def askValidInitials(screen): # A function that prompts the user to enter their initials and validates the input.
    
    """This function prompts the user to enter their initials and validates the input. It ensures that the initials are between 1 and 3 characters long, consist of ASCII letters only and are not empty. If the input is valid it returns the initials in uppercase. If the user cancels the input it returns None."""
    
    while True: # Start an infinite loop
        text = screen.getInitials() # Call the getInitials method of the screen object to prompt the user for their initials and store the input in the text variable
        
        if text is None: # Check if the user canceled the input (text is None)
            return None # If the user canceled the input return None to indicate that no initials were provided
        
        text = text.strip() # Remove any leading or trailing whitespace from the input text to ensure accurate validation
        
        if 1 <= len(text) <= 3 and text.isascii() and text.isalpha(): # Check if the length of the input text is between 1 and 3 characters and if it consists of ASCII letters only (no numbers or special characters)
            return text.upper() # If the input is valid return the initials in uppercase to maintain consistency in the leaderboard records
        
        screen.showError("Initials must be 1-3 letters and no numbers or special characters. Please retry.") # If the input is invalid display an error message to the user indicating that the initials must be 1-3 letters and prompt them to retry

def playHumanGame(screen, sessionBoard, allTimeBoard, settings, historyStorage, logStorage): # A function that manages the gameplay for a human player
    
    """This function manages the gameplay for a human player. It creates a new game instance, plays a round of the game, collects the player's initials, creates a record of the game played, and updates the session and all-time leaderboards. It also handles saving leaderboard data and logging events related to the game played."""
    
    currentGame = Game(attemptLimit = ["attempt_limit"]) # Create a new instance of the Game class with the attempt limit specified in the settings dictionary
    turns = currentGame.playRound(screen) # Call the playRound method of the currentGame instance to start a round of the game and store the number of turns taken by the player in the turns variable
    
    if turns is None: # Check if the player canceled the game (turns is None)
        return # If the player canceled the game return from the function without proceeding further
    
    initials = askValidInitials(screen) # Call the askValidInitials function to prompt the player for their initials and store the input in the initials variable
    
    if initials is None: # Check if the player canceled the input for initials (initials is None)
        return # If the player canceled the input for initials return from the function without proceeding further
    
    now = datetime.now().isoformat(timespec='seconds') # Get the current date and time in ISO 8601 format with seconds precision and store it in the now variable
    record = makeRecord(initials, turns, now, "human") # Call the makeRecord function to create a record of the game played with the player's initials, number of turns taken, current date and time and the player type ("human") and store it in the record variable
    
    sessionBoard.addRecord(record) # Call the addRecord method of the sessionBoard instance to add the newly created record to the session leaderboard
    allTimeBoard.addRecord(record) # Call the addRecord method of the allTimeBoard instance to add the newly created record to the all-time leaderboard
    
    if not historyStorage.saveLeaderboardData(allTimeBoard.entries): # Call the saveLeaderboardData method of the historyStorage instance to save the all-time leaderboard data and check if the operation was successful (returns False if it failed)
        screen.showError("Failed to save leaderboard data. Please check the storage settings.") # If the save operation failed display an error message to the user indicating that the leaderboard data could not be saved and suggest checking the storage settings
    
    logStorage.logEvent(f"Game played by {initials} in {turns} turns at {now}. Record added to leaderboards.") # Call the logEvent method of the logStorage instance to log an event indicating that a game was played by the player with their initials, number of turns taken, current date and time and that the record was added to the leaderboards

def playBotGame(screen):
    
    """0"""
    
    
    
    
    
    
    

def runSimulationOption(screen):
    
    """0"""
    
    
    
    
    
    

def runSortComparison(screen):
    
    """0"""
    
    
    
    
    
    
    

def main():
    
    """0"""
    
    
    
    
    
    
    
    
    

if __name__ == "__main__":
    main() 