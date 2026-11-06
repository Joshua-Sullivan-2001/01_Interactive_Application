# game.py: judges player guesses against a secret number and runs one round.

import random # Import the random module to generate a secret number.

from engine.validator import min_value, max_value, validate_guess # Import the number range and the validator function from the validator module.

# constants for the game
too_low = "Too low!" # Message for a guess that is too low.
too_high = "Too high!" # Message for a guess that is too high.
correct = "Correct!" # Message for a correct guess.

class game:
    """The game class holds the secret number and the rules. It can validate guesses and run a full round of the game."""

    def __init__(self, secret_number = None, attempt_limit = None): # The values after = are used when nothing is given.
        """Sets the secret number and attempt limit for the game."""
    
        if secret_number is not None: # If a secret number is provided, use it.
            self.secret_number = secret_number # Set the secret number to the provided value.
        else: # Otherwise pick one at random.
            self.secret_number = random.randint(min_value, max_value) # Generate a random secret number within the range (randint includes both values).
        
        self.turns = 0 # Set the number of turns taken by the player to 0.
        self.finished = False # Set the finished status of the game to False.
        self.attempt_limit = attempt_limit # Store the attempt limit where None means unlimited attempts.
    
    def validate_user_guess(self, user_guess):
        """Compares a valid guess with the secret number and returns a message saying if it is too low, too high or correct."""
    
        self.turns += 1 # Add 1 to the number of turns taken by the player.
    
        if user_guess < self.secret_number: # If the user's guess is less than the secret number.
            return too_low # Return the message indicating the guess is too low.
        elif user_guess > self.secret_number: # If the user's guess is greater than the secret number.
            return too_high # Return the message indicating the guess is too high.
        else: # If the user's guess is equal to the secret number.
            self.finished = True # Set the finished status of the game to True.
            return correct # Return the message indicating the guess is correct.
    
    def attempt_limit_reached(self):
        """Checks if the player has reached the attempt limit."""
    
        if self.attempt_limit is None: # If there is no attempt limit set.
            return False # Return False because the player can never run out.
        elif self.turns >= self.attempt_limit: # If the turns taken are greater than or equal to the attempt limit.
            return True # Return True indicating the attempt limit has been reached.
        else: # Otherwise there are still attempts left.
            return False # Return False indicating the attempt limit has not been reached.
    
    def play_round(self, screen):
        """Plays one full round by asking for guesses until the number is found. It returns the turns taken or None if the player quit or ran out of attempts."""
    
        while self.finished == False: # Keep going until the secret number is found.
            raw_text = screen.get_guess() # Get the user's guess from the display object.
        
            if raw_text is None: # If the input was closed or Ctrl+C was pressed.
                return None # Give up on this round.
        
            check = validate_guess(raw_text) # Validate the user's guess using the validator function.
        
            if check.ok == False: # If the validation check is not okay.
                screen.show_error(check.message) # Show an error message using the display object.
                continue # Go back to the top and ask again (no turn is counted).
        
            outcome = self.validate_user_guess(check.value) # Compare the valid number with the secret number.
        
            if outcome == correct: # If the player guessed the number.
                break # Leave the loop (a correct last guess still counts as a win).
        
            screen.show_hint(outcome) # Show the too low or too high hint.
        
            if self.attempt_limit_reached(): # If the attempt limit has been reached.
                screen.show_message(f"Attempt limit reached. The secret number was {self.secret_number}.") # Show a message that reveals the secret number.
                return None # Return None because there is no win and so no score.
            
        screen.show_win(self.turns) # Show the win message with the number of turns taken.
        return self.turns # Return the number of turns taken by the player.
