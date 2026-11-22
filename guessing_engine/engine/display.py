# display.py: handles all text printing and all player input for the game

# Constants for display classes for easy modification

guessPrompt = "Please enter your guess (a whole number between 1 and 100): " # Prompt for the user to enter their guess.
menuPrompt = "Please enter your choice (1 to 7): " # Prompt for the user to select a menu option.
initialsPrompt = "Please enter your initials (up to 3 letters): " # Prompt for the user to enter their initials.
winMessage = "Congratulations! You've guessed the correct number in {turns} turns!" # Message for when the user guesses the correct number.
thankYouMessage = "Thank you for playing! Goodbye!" # Message to thank the user for playing the game.
emptyLeaderboardMessage = "The leaderboard is currently empty. Be the first to set a record!" # Message for when the leaderboard is empty.

rankWidth = 6 # Width for displaying the rank column in the leaderboard.
initialsWidth = 10 # Width for displaying the initials column in the leaderboard.
turnsWidth = 6 # Width for displaying the turns column in the leaderboard.

class Display: # Base class to handle all methods related to displaying text and getting user input for the game
    
    """Base class to handle all methods related to displaying text and getting user input for the game."""

    def showMenu(self, options): # Displays the main menu with the given options
        """Displays the main menu with the given options."""
        pass # will use child class to implement this and all other methods due to possible Rich text formatting that may be added in the future

    def showMessage(self, message): # Displays a message to the user
        """Displays a message to the user."""
        pass # will use child class

    def showError(self, errorMessage): # Displays an error message to the user
        """Displays an error message to the user."""
        pass # will use child class

    def showHint(self, hintMessage): # Displays a hint message to the user
        """Displays a hint message to the user."""
        pass # will use child class

    def showWin(self, turns): # Displays a win message to the user with the number of turns taken
        """Displays a win message to the user with the number of turns taken."""
        pass # will use child class

    def showThankYou(self): # Displays a thank you message to the user
        """Displays a thank you message to the user."""
        pass # will use child class

    def showLeaderboard(self, leaderboard, title): # Displays the leaderboard with the given records
        """Displays the leaderboard with the given records."""
        pass # will use child class

    def getGuess(self): # Prompts the user to enter their guess and returns it
        """Prompts the user to enter their guess and returns it."""
        pass # will use child class

    def getMenuChoice(self): # Prompts the user to select a menu option and returns their choice
        """Prompts the user to select a menu option and returns their choice."""
        pass # will use child class

    def getInitials(self): # Prompts the user to enter their initials and returns them
        """Prompts the user to enter their initials and returns them."""
        pass # will use child class

class basicDisplay(Display): # A basic display class that implements the methods from the Display base class for console output and input without any additional formatting.
    
    """The basic inbuilt text formatting that will hold the child class methods for the display class. This class will be used to display text in the console without any additional formatting than the inbuilt formatting."""

    def showMenu(self, options): # Displays the main menu with the given options
        
        """Displays the main menu with the given options."""

        number = 1 # Start a counter for numbering the menu options
        for label in options: # Loop through each option label in the options list
            print(f"{number}. {label}") # Print the option number and label
            number += 1 # Increment the counter for the next option

    def showMessage(self, message): # Displays a message to the user
    
        """Displays a message to the user."""
        
        print(message) # Print the message to the console

    def showError(self, errorMessage): # Displays an error message to the user
        
        """Displays an error message to the user."""
        
        print(f"Error: {errorMessage}") # Print the error message to the console with an "Error:" prefix

    def showHint(self, hintMessage): # Displays a hint message to the user
        
        """Displays a hint message to the user."""
        
        print(f"Hint: {hintMessage}") # Print the hint message to the console with a "Hint:" prefix

    def showWin(self, turns): # Displays a win message to the user with the number of turns taken
        
        """Displays a win message to the user with the number of turns taken."""
        
        print(winMessage.format(turns=turns)) # Print the win message to the console formatting it with the number of turns taken

    def showThankYou(self): # Displays a thank you message to the user
        
        """Displays a thank you message to the user."""
        
        print(thankYouMessage) # Print the thank you message to the console

    def showLeaderboard(self, leaderboard, title): # Displays the leaderboard with the given records
        
        """Displays the leaderboard with the given records."""
        
        print(f"--- {title} ---") # Print a header for the leaderboard
        if len(leaderboard) == 0: # Check if the leaderboard is empty
            print(emptyLeaderboardMessage) # Print a message indicating that the leaderboard is empty
            return # Exit the method if the leaderboard is empty
        
        rank = 1 # Start the rank counter
        for entry in leaderboard: # Loop through each entry in the leaderboard
            line = str(rank).ljust(rankWidth) # Format the rank with left justification based on the rankWidth
            line += entry['initials'].ljust(initialsWidth) # Format the initials with left justification based on the initialsWidth
            line += str(entry['turns']).ljust(turnsWidth) # Format the number of turns with left justification based on the turnsWidth
            print(line) # Print the formatted leaderboard entry
            rank += 1 # Increment the rank counter for the next entry

    def getGuess(self): # Prompts the user to enter their guess and returns it
        
        """Prompts the user to enter their guess and returns it."""
        
        return self.ask(guessPrompt) # Prompt the user for their guess using the ask method and return the input

    def getMenuChoice(self): # Prompts the user to select a menu option and returns their choice
        
        """Prompts the user to select a menu option and returns their choice."""
        
        return self.ask(menuPrompt) # Prompt the user for their menu choice using the ask method and return the input

    def getInitials(self): # Prompts the user to enter their initials and returns them
        
        """Prompts the user to enter their initials and returns them."""
        
        return self.ask(initialsPrompt) # Prompt the user for their initials using the ask method and return the input

    def ask(self, prompt): # Prompts the user with the given prompt and returns their input. Handles EOFError and KeyboardInterrupt exceptions
        
        """Prompts the user with the given prompt and returns their input. Handles EOFError and KeyboardInterrupt exceptions."""
        
        try: # Try to get input from the user using the built-in input function
            return input(prompt) # Prompt the user with the given prompt and return the input
        except (EOFError, KeyboardInterrupt): # Handle EOFError (input closed) and KeyboardInterrupt (Ctrl+C) exceptions
            print("\nInput interrupted. Exiting the game.") # Print a message indicating that the input was interrupted
            return None # Return None to indicate that the input was interrupted


# Optional add the Rich library and create a RichDisplay class if i have enough time to implement it.











# Utility function to create a display object based on the specified type

def createDisplay(displayType): # Creates a display object based on the specified type
    
    """Creates a display object based on the specified type."""
    
    if displayType == "basic": # Check if the specified display type is "basic"
        return basicDisplay() # Return an instance of the basicDisplay class
    elif displayType == "rich": # Check if the specified display type is "rich"
        return basicDisplay() # Return an instance of the basicDisplay class (as a placeholder for RichDisplay if implemented)
    # elif displayType == "rich": # Check if the specified display type is "rich"
    #     return RichDisplay() # Return an instance of the RichDisplay class (if implemented
    else: # If the specified display type is not recognized
        raise ValueError(f"Unknown display type: {displayType}") # Raise a ValueError indicating that the display type is unknown