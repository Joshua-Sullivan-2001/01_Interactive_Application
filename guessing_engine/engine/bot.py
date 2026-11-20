# bot.py: manages the bot's guessing logic and strategy

import random # Import the random module to generate random guesses for the bot

from engine.game import tooHigh, tooLow, correct # Import the game module from the engine package to access the game's feedback functions
from engine.validator import minValue, maxValue # Import the validator module from the engine package to access the minimum and maximum value constraints for the bot's guesses

loopStop = 40 # Define a constant for the maximum number of attempts the bot can make before stopping its guessing loop so it doesn't run indefinitely

class binaryBot: # Implements a bot that uses a binary search strategy
    
    """This class implements a bot that uses a binary search strategy to guess the correct number in the game. The bot narrows down the range of possible numbers based on feedback from the game making it efficient in finding the correct answer within a limited number of guesses."""
    
    def pickGuess(self, low, high): # A function to pick a guess based on the current low and high range using a binary search strategy
        
        """This function picks a guess based on the current low and high range using a binary search strategy. It calculates the midpoint of the range and returns it as the bot's guess. This approach allows the bot to efficiently narrow down the possible numbers by halving the search space with each guess"""
        
        return(low + high) // 2 # Calculate the midpoint of the current range and return it as the bot's guess. This is done by adding the low and high values and performing division by 2 to get the average value which represents the middle of the range
        
    def play(self, currentGame): # A function to play the game using the binary search strategy until the correct number is guessed or the maximum number of attempts is reached
        
        """This function plays the game using the binary search strategy until the correct number is guessed or the maximum number of attempts is reached. It maintains a low and high range for possible guesses and updates these values based on feedback from the game. The bot continues to make guesses until it either finds the correct number or exhausts its allowed attempts at which point it returns the number of guesses made or None if unsuccessful."""
        
        low = minValue # Initialize the low range for possible guesses to the minimum value defined in the validator module
        high = maxValue # Initialize the high range for possible guesses to the maximum value defined in the validator module
        guesses = 0 # Initialize a counter to keep track of the number of guesses made by the bot
        
        while guesses < loopStop: # Continue making guesses until the maximum number of attempts is reached
            guess = self.pickGuess(low, high) # Use the pickGuess function to determine the next guess based on the current low and high range
            guesses += 1 # Increment the guess counter to reflect that a new guess has been made
            outcome = currentGame.validateUserGuess(guess) # Call the validateUserGuess function from the current game instance to check if the guess is too high, too low or correct and store the result in the outcome variable
        
        if outcome == correct: # Check if the outcome of the guess is correct
            return guesses # If the guess is correct return the total number of guesses made by the bot
        elif outcome == tooLow: # Check if the outcome of the guess is too low
            low = guess + 1 # If the guess is too low update the low range to be one more than the current guess to narrow down the search space
        else: # If the outcome of the guess is too high
            high = guess - 1 # If the guess is too high update the high range to be one less than the current guess to narrow down the search space
        
        return None # If the bot exhausts its allowed attempts without guessing the correct number return None to indicate that it was unsuccessful

class randomBot: # Implements a bot that makes random guesses within the valid range
    
    """This class implements a bot that makes random guesses within the valid range defined by the minimum and maximum values. The bot does not use any specific strategy to narrow down its guesses but instead relies on randomness to find the correct number. It continues to make random guesses until it either finds the correct number or exhausts its allowed attempts."""
    
    def pickGuess(self, low, high): # A function to pick a random guess within the current low and high range
        
        """This function picks a random guess within the current low and high range. It uses the random module to generate a random integer between the specified low and high values. This approach allows the bot to make unpredictable guesses without any specific strategy relying only on chance to find the correct number."""
        
        return random.randint(low, high) # Generate a random integer between the low and high values and return it as the bot's guess. This is done using the randint function from the random module which ensures that each guess is unpredictable and falls within the valid range of possible numbers

    def play(self, currentGame): # A function to play the game using random guesses until the correct number is guessed or the maximum number of attempts is reached
        
        """This function plays the game using random guesses until the correct number is guessed or the maximum number of attempts is reached. It maintains a low and high range for possible guesses and updates these values based on feedback from the game. The bot continues to make random guesses until it either finds the correct number or exhausts its allowed attempts at which point it returns the number of guesses made or None if unsuccessful."""
        
        low = minValue # Initialize the low range for possible guesses to the minimum value defined in the validator module
        high = maxValue # Initialize the high range for possible guesses to the maximum value defined in the validator module
        guesses = 0 # Initialize a counter to keep track of the number of guesses made by the bot
        
        while guesses < loopStop: # Continue making guesses until the maximum number of attempts is reached
            guess = self.pickGuess(low, high) # Use the pickGuess function to determine the next random guess based on the current low and high range
            guesses += 1 # Increment the guess counter to reflect that a new guess has been made
            outcome = currentGame.validateUserGuess(guess) # Call the validateUserGuess function from the current game instance to check if the guess is too high, too low or correct and store the result in the outcome variable
        
        if outcome == correct: # Check if the outcome of the guess is correct
            return guesses # If the guess is correct return the total number of guesses made by the bot
        elif outcome == tooLow: # Check if the outcome of the guess is too low
            low = guess + 1 # If the guess is too low update the low range to be one more than the current guess to narrow down the search space
        else: # If the outcome of the guess is too high
            high = guess - 1 # If the guess is too high update the high range to be one less than the current guess to narrow down the search space
        
        return None # If the bot exhausts its allowed attempts without guessing the correct number return None to indicate that it was unsuccessful
