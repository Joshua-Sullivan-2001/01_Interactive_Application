# simulation.py: runs multiple rounds of the game and manages the overall flow

import random # Import the random module to generate random numbers for the simulation
import time # Import the time module to introduce delays in the simulation for better visualization

from engine.game import Game # Import the Game class from the game module in the engine package to create and manage game instances
from engine.leaderboard import getTurns # Import the getTurns function from the leaderboard module in the engine package to retrieve the number of turns taken by players
from engine.sorting import insertionSorter, mergeSorter # Import the insertionSort and mergeSort functions from the sorting module in the engine package to sort the leaderboard data

sortSizes = [10, 100, 500, 1000, 2000, 4000, 6000, 8000, 10000] # Define a list of sizes for the leaderboard data to be sorted during the simulation. These sizes represent the number of entries in the leaderboard that will be sorted using different sorting algorithms
repeats = 5 # Define the number of times each sorting algorithm will be run for each size in sortSizes to get an average performance measurement


def runSimulation(botClass, games, seed): # A function that runs a simulation of the guessing game using the specified bot class for a given number of games and a random seed
    
    """Runs a simulation of the guessing game using the specified bot class for a given number of games and a random seed."""
    
    random.seed(seed) # Set the random seed to ensure reproducibility of the simulation results. This allows for consistent behavior across different runs of the simulation
    results = [] # Initialize an empty list to store the results of each game played by the bot. Each entry in this list will represent the number of guesses taken by the bot to correctly guess the number in a single game
    
    for _ in range(games): # Loop through the specified number of games to be played in the simulation. For each iteration, a new game instance will be created and the bot will attempt to guess the number
        
        currentGame = Game() # Create a new instance of the Game class for the current game
        bot = botClass() # Create an instance of the specified bot class that will be used to play the current game
        guesses = bot.play(currentGame) # Call the play method of the bot instance, passing in the current game instance. The bot will attempt to guess the number and the number of guesses taken will be returned and stored in the variable guesses
        
        if guesses is not None: # Check if the bot successfully guessed the number (i.e., guesses is not None). If the bot failed to guess the number it will return None and it will not record that game in the results
            results.append(guesses) # Append the number of guesses taken by the bot to the results list
            
    return results # Return the list of results containing the number of guesses taken by the bot for each game played in the simulation

def summarizeResults(results): # A function that summarizes the results of the simulation by calculating the fewest guesses, most guesses, total guesses and average guesses taken by the bot across all games played.
    
    """Summarizes the results of the simulation by calculating the fewest guesses, most guesses, total guesses and average guesses taken by the bot across all games played."""
    
    if len(results) == 0: # Check if the results list is empty, indicating that no games were played or the bot failed to guess the number in all games.
        return 0, 0, 0 # Return a tuple of zeros to indicate that there were no valid results to summarize.
    
    fewestGuesses = results[0] # Initialize the fewestGuesses variable to the first result in the results list. This will be used to track the minimum number of guesses taken by the bot across all games played
    mostGuesses = results[0] # Initialize the mostGuesses variable to the first result in the results list. This will be used to track the maximum number of guesses taken by the bot across all games played
    totalGuesses = 0 # Initialize the totalGuesses variable to zero. This will be used to accumulate the total number of guesses taken by the bot across all games played
    
    for result in results: # Loop through each result in the results list to update the fewestGuesses, mostGuesses and totalGuesses variables based on the number of guesses taken by the bot in each game
        if result < fewestGuesses: # Check if the current result is less than the current fewestGuesses
            fewestGuesses = result # Update the fewestGuesses variable to the current result if it is less than the current fewestGuesses
        if result > mostGuesses: # Check if the current result is greater than the current mostGuesses
            mostGuesses = result # Update the mostGuesses variable to the current result if it is greater than the current mostGuesses
        totalGuesses += result # Add the current result to the totalGuesses variable to accumulate the total number of guesses taken by the bot across all games played
    
    return fewestGuesses, mostGuesses, totalGuesses / len(results) # Return a tuple containing the fewest guesses, most guesses and average guesses taken by the bot across all games played. The average is calculated by dividing the totalGuesses by the number of valid results in the results list

def timeSort(): # A function that measures the time taken by different sorting algorithms to sort leaderboard data of varying sizes. It runs multiple rounds of sorting for each size and calculates the average time taken by each algorithm
    
    """Measures the time taken by different sorting algorithms to sort leaderboard data of varying sizes. It runs multiple rounds of sorting for each size and calculates the average time taken by each algorithm."""
    
    seedGenerator = random.Random(1) # Create a new instance of the random.Random class with a fixed seed value of 1. This ensures that the random numbers generated for the simulation are consistent across different runs allowing for reproducibility of the results
    rows = [] # Initialize an empty list to store the results of the sorting time measurements for each size in sortSizes
    
    for size in sortSizes: # Loop through each size in the sortSizes list to measure the time taken by different sorting algorithms for that specific size of leaderboard data
        data = [] # Initialize an empty list to store the leaderboard data for the current size
    
        for _ in range(size): # Loop through the range of the current size to generate random leaderboard data entries for the current size
            data.append({"turns": seedGenerator.randint(1, 50)}) # Append a dictionary containing a random number of turns (between 1 and 50) to the data list
        
        row: list[float] = [size] # Initialize a new list to store the results for the current size
        
        for sorter in (insertionSorter(), mergeSorter()): # Loop through each sorting algorithm (insertionSorter and mergeSorter) to measure the time taken by each algorithm to sort the leaderboard data for the current size
            
            total = 0.0 # Initialize a variable to accumulate the total time taken by the current sorting algorithm across multiple rounds of sorting for the current size
            
            for _ in range(repeats): # Loop through the specified number of repeats to run the sorting algorithm multiple times for the current size and calculate the average time taken
                start = time.perf_counter() # Record the start time before running the sorting algorithm to measure the time taken for sorting
                sorter.orderItems(data, getTurns) # Call the orderItems method of the current sorting algorithm passing in the leaderboard data and the getTurns function to sort the data based on the number of turns taken by players
                total += time.perf_counter() - start # Calculate the time taken for sorting by subtracting the start time from the current time after sorting and accumulate it in the total variable
                
            row.append(total / repeats) # Calculate the average time taken by the current sorting algorithm for the current size by dividing the total time by the number of repeats and append it to the row list
        rows.append(tuple(row)) # Append the row list as a tuple to the rows list to store the results for the current size of leaderboard data. Each row will contain the size and the average time taken by each sorting algorithm for that size
    return rows # Return the list of rows containing the results of the sorting time measurements for each size in sortSizes. Each row will contain the size and the average time taken by each sorting algorithm for that size
