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

def playBotGame(screen): # A function that manages the gameplay for a bot player
    
    """This function manages the gameplay for a bot player. It creates a new instance of the Game class allows the bot to play the game and displays the number of turns taken by the bot to guess the number. If the bot is unable to guess the number within the allowed attempts it displays an appropriate message."""
    
    guesses = binaryBot().play(Game()) # Call the play method of a new instance of the binaryBot class to allow the bot to play a new instance of the Game class and store the number of turns taken by the bot to guess the number in the guesses variable
    
    if guesses is None: # Check if the bot was unable to guess the number within the allowed attempts (guesses is None)
        screen.showMessage("The bot was unable to guess the number within the allowed attempts.") # If the bot was unable to guess the number display an appropriate message to the user
    else: # If the bot successfully guessed the number within the allowed attempts
        screen.showMessage(f"The bot guessed the number in {guesses} turns.") # Display a message to the user indicating the number of turns taken by the bot to guess the number

def runSimulationOption(screen): # A function that runs a simulation of the guessing game using different bot classes and summarizes the results of the simulation by calculating the fewest guesses, most guesses, total guesses and average guesses taken by each bot across all games played
    
    """This function runs a simulation of the guessing game using different bot classes and summarizes the results of the simulation by calculating the fewest guesses, most guesses, total guesses and average guesses taken by each bot across all games played. It displays the summarized results for each bot class to the user."""
    
    for botClass in (binaryBot, randomBot): # Loop through each bot class (binaryBot and randomBot) to run a simulation of the guessing game using that bot class and summarize the results of the simulation
        
        results = runSimulation(botClass, simulationGames, simulationSeed) # Call the runSimulation function to run a simulation of the guessing game using the current bot class for the specified number of games and random seed and store the results in the results variable
        
        fewest, most, average = summarizeResults(results) # Call the summarizeResults function to summarize the results of the simulation by calculating the fewest guesses, most guesses, total guesses and average guesses taken by the current bot class across all games played and store the summarized results in the fewest, most and average variables
        
        screen.showMessage(f"Simulation results for {botClass.__name__}:\nFewest guesses: {fewest}\nMost guesses: {most}\nAverage guesses: {average}") # Display a message to the user showing the summarized results of the simulation for the current bot class including the fewest guesses, most guesses and average guesses taken by the bot across all games played
    

def runSortComparison(screen): # A function that measures the time taken by different sorting algorithms to sort leaderboard data of varying sizes and displays the results to the user
    
    """This function measures the time taken by different sorting algorithms to sort leaderboard data of varying sizes and displays the results to the user. It runs multiple rounds of sorting for each size and calculates the average time taken by each algorithm. The results are displayed in a formatted message to the user."""
    
    for size, insertionTime, mergeTime in timeSort(): # Loop through the results of the timeSort function which returns a generator yielding tuples containing the size of the leaderboard data, average time taken by insertion sort and average time taken by merge sort for that size
        screen.showMessage(f"{size:>6} records: Insertion Sort = {insertionTime:.5f} seconds, Merge Sort = {mergeTime:.5f} seconds") # Display a message to the user showing the size of the leaderboard data and the average time taken by insertion sort and merge sort for that size in a formatted manner
    

def main(): # The main function that serves as the entry point for the guessing engine application
    
    """The main function serves as the entry point for the guessing engine application. It loads configuration settings, initializes display and storage objects, manages the main menu loop and handles user interactions for playing games, viewing leaderboards, running simulations and comparing sorting algorithms."""
    
    settings, problems = loadConfig("config.json") # Load configuration settings and problems from the config.json file using the loadConfig function and store them in the settings and problems variables respectively
    screen = createDisplay(settings["display_mode"]) # Create a display object based on the display mode specified in the settings dictionary. Plain or Rich
    historyStorage = Storage(settings["history_storage"]) # Create a storage object for managing persistent storage of game history and leaderboard records based on the history storage settings specified in the settings dictionary
    logStorage = Storage(settings["log_storage"]) # Create a storage object for managing persistent storage of log events based on the log storage settings specified in the settings dictionary
    history = historyStorage.loadLeaderboardData() # Load the all-time leaderboard data from the history storage using the loadLeaderboardData method of the historyStorage object and store it in the history variable
    sorter = getSorter(settings["leaderboard_sort"]) # Retrieve the sorting algorithm specified in the settings dictionary for managing leaderboard records using the getSorter function and store it in the sorter variable
    sessionBoard = Leaderboard(sorter) # Create a new instance of the Leaderboard class for managing the session leaderboard using the retrieved sorting algorithm and store it in the sessionBoard variable
    allTimeBoard = Leaderboard(sorter) # Create a new instance of the Leaderboard class for managing the all-time leaderboard using the retrieved sorting algorithm and store it in the allTimeBoard variable
    allTimeBoard.loadEntries(history) # Load the all-time leaderboard entries from the history variable into the allTimeBoard instance using the loadEntries method of the Leaderboard class
    
    for problem in problems + historyStorage.problems: # Loop through each problem in the problems list and the problems list from the history storage to log any issues or errors encountered during the loading of configuration settings and leaderboard data
        logStorage.logEvent(problem) # Call the logEvent method of the logStorage object to log each problem encountered during the loading of configuration settings and leaderboard data for debugging and troubleshooting purposes
    
    running = True # Initialize a variable to control the main menu loop. It will be set to False when the user chooses to exit the program
    
    while running: # Start the main menu loop which will continue until the running variable is set to False (when the user chooses to exit the program)
        screen.showMenu(menuOptions(settings)) # Call the showMenu method of the screen object to display the main menu options to the user based on the settings dictionary. The menuOptions function generates the list of available options for the user to choose from
        choice = screen.getMenuChoice() # Call the getMenuChoice method of the screen object to prompt the user for their menu choice and store the input in the choice variable. This will be used to determine which action to take based on the user's selection
        
        if choice is not None: # Check if the user provided a menu choice (choice is not None)
            choice = choice.strip() # Remove any leading or trailing whitespace from the user's menu choice to ensure accurate processing of the input
        
        if choice is None: # Check if the user canceled the menu choice input (choice is None)
            running = False # If the user canceled the menu choice input set the running variable to False to exit the main menu loop and terminate the program
        elif choice == "1": # Check if the user selected option 1 to play a game
            playHumanGame(screen, sessionBoard, allTimeBoard, settings, historyStorage, logStorage) # If the user selected option 1 call the playHumanGame function to manage the gameplay for a human player and pass in the necessary parameters including the screen object, session leaderboard, all-time leaderboard, settings dictionary, history storage and log storage
        elif choice == "2": # Check if the user selected option 2 to view the session leaderboard
            screen.showLeaderboard(sessionBoard.getRanked(), "Session Leaderboard") # If the user selected option 2 call the showLeaderboard method of the screen object to display the session leaderboard to the user. The getRanked method of the sessionBoard instance is called to retrieve the ranked entries for the session leaderboard
        elif choice == "3": # Check if the user selected option 3 to view the all-time leaderboard
            screen.showLeaderboard(allTimeBoard.getRanked(), "All-Time Leaderboard") # If the user selected option 3 call the showLeaderboard method of the screen object to display the all-time leaderboard to the user. The getRanked method of the allTimeBoard instance is called to retrieve the ranked entries for the all-time leaderboard
        elif choice == "4" and settings["bot_mode"]: # Check if the user selected option 4 to watch a bot game and if bot mode is enabled in the settings dictionary
            playBotGame(screen) # If the user selected option 4 and bot mode is enabled call the playBotGame function to manage the gameplay for a bot player and pass in the screen object
        elif choice == "5" and settings["simulation_mode"]: # Check if the user selected option 5 to run a bot simulation and if simulation mode is enabled in the settings dictionary
            runSimulationOption(screen) # If the user selected option 5 and simulation mode is enabled call the runSimulationOption function to run a simulation of the guessing game using different bot classes and summarize the results of the simulation by calculating the fewest guesses, most guesses, total guesses and average guesses taken by each bot across all games played. Pass in the screen object to display the summarized results to the user
        elif choice == "6" and settings["simulation_mode"]: # Check if the user selected option 6 to compare sorting algorithms and if simulation mode is enabled in the settings dictionary
            runSortComparison(screen) # If the user selected option 6 and simulation mode is enabled call the runSortComparison function to measure the time taken by different sorting algorithms to sort leaderboard data of varying sizes and display the results to the user. Pass in the screen object to display the results
        elif choice == "7": # Check if the user selected option 7 to exit the program
            running = False # If the user selected option 7 set the running variable to False to exit the main menu loop and terminate the program
        else: # If the user provided an invalid menu choice (not None, not 1-7, or not enabled based on settings)
            screen.showError("Please pick an option from the menu.") # Display an error message to the user indicating that they need to pick a valid option from the menu and prompt them to retry
        
    screen.showLeaderboard(sessionBoard.getRanked(), "Session Leaderboard") # After the user chooses to exit the program display the session leaderboard one last time to show the final results of the session. The getRanked method of the sessionBoard instance is called to retrieve the ranked entries for the session leaderboard
    logStorage.logEvent("Program exited. Session leaderboard displayed.") # Log an event indicating that the program has exited and the session leaderboard has been displayed for record-keeping and debugging purposes
    screen.showThankYou() # Display a thank you message to the user to express appreciation for using the guessing engine application and provide a positive user experience
    

if __name__ == "__main__": # Check if the script is being run as the main program (not imported as a module) to execute the main function and start the guessing engine application
    
    """This block checks if the script is being run as the main program (not imported as a module) to execute the main function and start the guessing engine application. It ensures that the main function is only called when the script is executed directly."""
    
    main() # Call the main function to start the guessing engine application and initiate the main menu loop for user interaction
