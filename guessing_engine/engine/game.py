# game.py: judges player guesses against a secret number and runs one round

import random # Import the random module to generate a secret number

from engine.validator import minValue, maxValue, validateGuess # Import the number range and the validator function from the validator module

# Constants for the game
tooLow = "Too low!" # Message for a guess that is too low
tooHigh = "Too high!" # Message for a guess that is too high
correct = "Correct!" # Message for a correct guess

class Game: # The game class holding the functions that run a round of the game and validate guesses against the secret number
    
    """The game class holds the secret number and the rules. It can validate guesses and run a full round of the game."""

    def __init__(self, secretNumber = None, attemptLimit = None): # A function to initialize the game class with a secret number and an attempt limit. The values after = are used when nothing is given
        
        """Sets the secret number and attempt limit for the game."""
    
        if secretNumber is not None: # If a secret number is provided use it
            self.secretNumber = secretNumber # Set the secret number to the provided value
        else: # Otherwise pick one at random
            self.secretNumber = random.randint(minValue, maxValue) # Generate a random secret number within the range (randint includes both values)
        
        self.turns = 0 # Set the number of turns taken by the player to 0
        self.finished = False # Set the finished status of the game to False
        self.attemptLimit = attemptLimit # Store the attempt limit where None means unlimited attempts
    
    def validateUserGuess(self, userGuess): # A function to compare a valid guess with the secret number and return a message indicating if it is too low, too high or correct
        
        """Compares a valid guess with the secret number and returns a message saying if it is too low, too high or correct."""
    
        self.turns += 1 # Add 1 to the number of turns taken by the player
    
        if userGuess < self.secretNumber: # If the user's guess is less than the secret number
            return tooLow # Return the message indicating the guess is too low
        elif userGuess > self.secretNumber: # If the user's guess is greater than the secret number
            return tooHigh # Return the message indicating the guess is too high
        else: # If the user's guess is equal to the secret number
            self.finished = True # Set the finished status of the game to True
            return correct # Return the message indicating the guess is correct
    
    def attemptLimitReached(self): # A function to check if the player has reached the attempt limit and return True if they have or False if they have not
        
        """Checks if the player has reached the attempt limit."""
    
        if self.attemptLimit is None: # If there is no attempt limit set
            return False # Return False because the player can never run out
        elif self.turns >= self.attemptLimit: # If the turns taken are greater than or equal to the attempt limit
            return True # Return True indicating the attempt limit has been reached
        else: # Otherwise there are still attempts left
            return False # Return False indicating the attempt limit has not been reached
    
    def playRound(self, screen): # A function to play one full round of the game by asking for guesses until the number is found, returning the turns taken or None if the player quit or ran out of attempts
        
        """Plays one full round by asking for guesses until the number is found. It returns the turns taken or None if the player quit or ran out of attempts."""
    
        while self.finished == False: # Keep going until the secret number is found
            rawText = screen.getGuess() # Get the user's guess from the display object
        
            if rawText is None: # If the input was closed or Ctrl+C was pressed
                return None # Give up on this round
        
            check = validateGuess(rawText) # Validate the user's guess using the validator function
        
            if check.ok == False: # If the validation check is not okay
                screen.showError(check.message) # Show an error message using the display object
                continue # Go back to the top and ask again (no turn is counted)
        
            outcome = self.validateUserGuess(check.value) # Compare the valid number with the secret number
        
            if outcome == correct: # If the player guessed the number
                break # Leave the loop (a correct last guess still counts as a win)
        
            screen.showHint(outcome) # Show the too low or too high hint
        
            if self.attemptLimitReached(): # If the attempt limit has been reached
                screen.showMessage(f"Attempt limit reached. The secret number was {self.secretNumber}.") # Show a message that reveals the secret number
                return None # Return None because there is no win and so no score
            
        screen.showWin(self.turns) # Show the win message with the number of turns taken
        return self.turns # Return the number of turns taken by the player
