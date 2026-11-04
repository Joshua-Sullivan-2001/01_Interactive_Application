# game.py: judges player guesses against a secret number and runs one round.

import random # importing the random module to generate a secret number

from guessing_engine.engine.display import display as Display # importing the display class from the display module
from guessing_engine.engine.validator import min_value, max_value, validate_Guess # importing the validator functions from the validator module

display = Display()

# constants for the game
too_low = "Too low!" # message for a guess that is too low
too_high = "Too high!" # message for a guess that is too high
correct = "Correct!" # message for a correct guess

class game:

    """The game class to handle the game logic and manage the secret number"""

    def __init__(self, secret_number, attempt_limit): # setting the game parameters

        """Sets the secret number and attempt limit for the game"""

        if secret_number is not None: # if a secret number is provided, use it
            self.secret_number = secret_number # setting the secret number to the provided value
        else:
            self.secret_number = random.randint(min_value, max_value) # generating a random secret number within the specified range

        self.turns = 0 # setting the number of turns taken by the player to 0
        self.finished = False # setting the finished status of the game to False

        if attempt_limit is not None: # if an attempt limit is provided, use it
            self.attempt_limit =  attempt_limit # setting the attempt limit to the provided value
        else:
            self.attempt_limit = None # setting the attempt limit to None if not provided

    def validate_User_Guess(self, user_guess): # method to validate the user's guess

        """Validates the user's guess and returns a message indicating if it is too low, too high, or correct"""

        self.turns += 1 # incrementing the number of turns taken by the player

        if user_guess < self.secret_number: # if the user's guess is less than the secret number
            return too_low # return the message indicating the guess is too low
        elif user_guess > self.secret_number: # if the user's guess is greater than the secret number
            return too_high # return the message indicating the guess is too high
        else: # if the user's guess is equal to the secret number
            self.finished = True # set the finished status of the game to True
            return correct # return the message indicating the guess is correct

    def attempt_limit_reached(self): # method to check if the attempt limit has been reached

        """Checks if the player has reached the attempt limit"""

        if self.attempt_limit is None: # if there is no attempt limit set
            return False # return False indicating the attempt limit has not been reached
        elif self.turns >= self.attempt_limit: # if the number of turns taken is greater than or equal to the attempt limit
            return True # return True indicating the attempt limit has been reached
        else:
            return False # return False indicating the attempt limit has not been reached

    def play_round(self, user_guess): # method to play one round of the game

        """plays one round of the game by getting the user's guess, validating it and providing feedback"""

        raw_text = display.get_guess() # get the user's guess from the display class

        if raw_text is None: # if the user input is None, return None
            return None

        check = validate_Guess(raw_text) # validate the user's guess using the validator function

        if not check.ok: # if the validation check is not okay
            display.show_error(check.message) # show an error message using the display class
            return None

        outcome = self.validate_User_Guess(check.value) # validate the user's guess against the secret number using the game class method

        if outcome == correct: # if the outcome is correct
            display.show_hint(outcome) # show a hint message using the display class
        else: # if the outcome is not correct
            display.show_hint(outcome) # show a hint message using the display class

        if self.attempt_limit_reached(): # if the attempt limit has been reached
            display.show_message(f"Attempt limit reached. The secret number was {self.secret_number}.") # show a message indicating the attempt limit has been reached
            return None # return None indicating the game is over

        if outcome == correct:
            display.show_win(self.turns) # show a win message using the display class with the number of turns taken
            return self.turns # return the number of turns taken by the player
        return None
