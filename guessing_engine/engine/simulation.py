# simulation.py: runs multiple rounds of the game and manages the overall flow

import random # Import the random module to generate random numbers for the simulation
import time # Import the time module to introduce delays in the simulation for better visualization

from engine.game import Game # Import the Game class from the game module in the engine package to create and manage game instances
from engine.leaderboard import getTurns # Import the getTurns function from the leaderboard module in the engine package to retrieve the number of turns taken by players
from engine.sorting import insertionSorter, mergeSorter # Import the insertionSort and mergeSort functions from the sorting module in the engine package to sort the leaderboard data

sortSizes = [10, 100, 500, 1000, 2000, 4000, 6000, 8000, 10000] # Define a list of sizes for the leaderboard data to be sorted during the simulation. These sizes represent the number of entries in the leaderboard that will be sorted using different sorting algorithms
repeats = 5 # Define the number of times each sorting algorithm will be run for each size in sortSizes to get an average performance measurement


def runSimulation(botClass, games, seed):
    
    """0"""
    
    
    
    

def summarizeResults(results):
    
    """0"""
    
    
    
    

def timeSort():
    
    """0"""
    
    
    
    
