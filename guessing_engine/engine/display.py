# display.py: handles all text printing and all player input for the game.

# constants for display for easy modification

guess_prompt = "Please enter your guess (a whole number between 1 and 100): " # Prompt for the user to enter their guess.
menu_prompt = "Please select an option:\n1. Play the game\n2. View the rules\n3. Exit\nEnter your choice (1, 2, or 3): " # Prompt for the user to select a menu option.
initials_prompt = "Please enter your initials (up to 3 characters): " # Prompt for the user to enter their initials.
too_high_message = "Your guess is too high. Try again." # Message for when the user's guess is too high.
too_low_message = "Your guess is too low. Try again." # Message for when the user's guess is too low.
win_message = "Congratulations! You've guessed the correct number in {turns} turns!" # Message for when the user guesses the correct number.
thank_you_message = "Thank you for playing! Goodbye!" # Message to thank the user for playing the game.
empty_leaderboard_message = "The leaderboard is currently empty. Be the first to set a record!" # Message for when the leaderboard is empty.

rank_width = 6 # Width for displaying the rank column in the leaderboard.
initials_width = 10 # Width for displaying the initials column in the leaderboard.
turns_width = 6 # Width for displaying the turns column in the leaderboard.

class display:
    """Base class to handle all methods related to displaying text and getting user input for the game."""
    
    def show_menu(self, options): # Displays the main menu with the given options.
        """Displays the main menu with the given options."""
        pass # will use child class to implement this and all other methods due to possible Rich text formatting that may be added in the future.
    
    def show_message(self, message): # Displays a message to the user.
        """Displays a message to the user."""
        pass # will use child class
    
    def show_error(self, error_message): # Displays an error message to the user.
        """Displays an error message to the user."""
        pass # will use child class
    
    def show_hint(self, hint_message): # Displays a hint message to the user.
        """Displays a hint message to the user."""
        pass # will use child class
    
    def show_win(self, turns): # Displays a win message to the user with the number of turns taken.
        """Displays a win message to the user with the number of turns taken."""
        pass # will use child class
    
    def show_thank_you(self): # Displays a thank you message to the user.
        """Displays a thank you message to the user."""
        pass # will use child class
    
    def show_leaderboard(self, leaderboard): # Displays the leaderboard with the given records.
        """Displays the leaderboard with the given records."""
        pass # will use child class
    
    def get_guess(self): # Prompts the user to enter their guess and returns it.
        """Prompts the user to enter their guess and returns it."""
        pass # will use child class
    
    def get_menu_choice(self): # Prompts the user to select a menu option and returns their choice.
        """Prompts the user to select a menu option and returns their choice."""
        pass # will use child class
    
    def get_initials(self): # Prompts the user to enter their initials and returns them.
        """Prompts the user to enter their initials and returns them."""
        pass # will use child class
    
class basicDisplay(display):
    """The basic inbuilt text formatting that will hold the child class methods for the display class. This class will be used to display text in the console without any additional formatting than the inbuilt formatting."""
    
    def show_menu(self, options): # Displays the main menu with the given options.
        """Displays the main menu with the given options."""
        
        number = 1 # Start a counter for numbering the menu options.
        for label in options: # Loop through each option label in the options list.
            print(f"{number}. {label}") # Print the option number and label.
            number += 1 # Increment the counter for the next option.

    def show_message(self, message): # Displays a message to the user.
        """Displays a message to the user."""
        
        print(message) # Print the message to the console.
        
    def show_error(self, error_message): # Displays an error message to the user.
        """Displays an error message to the user."""
        
        print(f"Error: {error_message}") # Print the error message to the console with an "Error:" prefix.
        
    def show_hint(self, hint_message): # Displays a hint message to the user.
        """Displays a hint message to the user."""
        
        print(f"Hint: {hint_message}") # Print the hint message to the console with a "Hint:" prefix.
        
    def show_win(self, turns): # Displays a win message to the user with the number of turns taken.
        """Displays a win message to the user with the number of turns taken."""
        
        print(win_message.format(turns=turns)) # Print the win message to the console, formatting it with the number of turns taken.
        
    def show_thank_you(self): # Displays a thank you message to the user.
        """Displays a thank you message to the user."""
        
        print(thank_you_message) # Print the thank you message to the console.
    
    def show_leaderboard(self, leaderboard): # Displays the leaderboard with the given records.
        """Displays the leaderboard with the given records."""
        
        print(f"--- Leaderboard ---") # Print a header for the leaderboard.
        if len(leaderboard) == 0: # Check if the leaderboard is empty.
            print(empty_leaderboard_message) # Print a message indicating that the leaderboard is empty.
            return # Exit the method if the leaderboard is empty.
        
        rank = 1 # Start the rank counter.
        for entry in leaderboard: # Loop through each entry in the leaderboard.
            line = str(rank).ljust(rank_width) # Format the rank with left justification based on the rank_width.
            line += entry['initials'].ljust(initials_width) # Format the initials with left justification based on the initials_width.
            line += str(entry['turns']).ljust(turns_width) # Format the number of turns with left justification based on the turns_width.
            print(line) # Print the formatted leaderboard entry.
            rank += 1 # Increment the rank counter for the next entry.
            
    def get_guess(self): # Prompts the user to enter their guess and returns it.
        """Prompts the user to enter their guess and returns it."""
        
        return input(guess_prompt) # Prompt the user for their guess and return the input.
    
    def get_menu_choice(self): # Prompts the user to select a menu option and returns their choice.
        """Prompts the user to select a menu option and returns their choice."""
        
        return input(menu_prompt) # Prompt the user for their menu choice and return the input.
    
    def get_initials(self): # Prompts the user to enter their initials and returns them.
        """Prompts the user to enter their initials and returns them."""
        
        return input(initials_prompt) # Prompt the user for their initials and return the input.
    
    def ask(self, prompt):
        """Prompts the user with the given prompt and returns their input. Handles EOFError and KeyboardInterrupt exceptions."""
        
        try:
            return input(prompt) # Prompt the user with the given prompt and return the input.
        except (EOFError, KeyboardInterrupt): # Handle EOFError (input closed) and KeyboardInterrupt (Ctrl+C) exceptions.
            print("\nInput interrupted. Exiting the game.") # Print a message indicating that the input was interrupted.
            return None # Return None to indicate that the input was interrupted.
        

# Optional add the Rich library and create a RichDisplay class if i have enough time to implement it.
