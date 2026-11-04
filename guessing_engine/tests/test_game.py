# test_game.py: tests the game logic and flow.

from pathlib import Path # Import the Path class from the pathlib module to handle file paths.

from guessing_engine.engine.display import display as Display # importing the display class from the display module
from guessing_engine.engine.game import game, too_low, too_high, correct # importing the game class and constants from the game module

play_round = game.play_round

class Test_Game:

    """Tests for the Game class"""

    def ___init___(self, answers):
        """Initializes the test class with a list of answers"""

        self.answers = answers # setting the answers to the provided list
        self.errors = [] # initializing an empty list to store any errors encountered during testing
        self.hints = [] # initializing an empty list to store any hints provided during testing
        self.wins = [] # initializing an empty list to store any wins turn counts encountered during testing
        self.messages = [] # initializing an empty list to store any messages provided during testing

    def ask_Guess(self):
        """Asks the user for a guess and returns it"""

        if len(self.answers) == 0: # if there are no more answers left in the list
            return None # if there are no more answers, return None
        return self.answers.pop(0) # return the next answer from the list of answers

    def show_errors(self, message):
        """Shows an error message and appends it to the errors list"""

        self.errors.append(message) # append the error message to the errors list

    def show_hints(self, message):
        """Shows a hint message and appends it to the hints list"""

        self.hints.append(message) # append the hint message to the hints list

    def show_wins(self, turns):
        """Shows the number of turns taken to win and appends it to the wins list"""

        self.wins.append(turns) # append the number of turns taken to win to the wins list

    def show_messages(self, message):
        """Shows a message and appends it to the messages list"""

        self.messages.append(message) # append the message to the messages list

    def test_low_guess(self):
        """Tests the game logic for a low guess"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        guess = 30 # set the guess to 30
        result = test_game.validate_User_Guess(guess) # validate the guess using the game instance
        assert result == too_low # assert that the result is "Too low!"

    def test_high_guess(self):
        """Tests the game logic for a high guess"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        guess = 70 # set the guess to 70
        result = test_game.validate_User_Guess(guess) # validate the guess using the game instance
        assert result == too_high # assert that the result is "Too high!"

    def test_correct_guess_and_finish(self):
        """Tests the game logic for a correct guess and finishing the game"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        guess = 50 # set the guess to 50
        result = test_game.validate_User_Guess(guess) # validate the guess using the game instance
        assert result == correct # assert that the result is "Correct!"
        assert test_game.finished == True # assert that the game is finished after a correct guess

    def test_turns_increment(self):
        """Tests that the number of turns increments correctly after each guess"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        initial_turns = test_game.turns # store the initial number of turns
        test_game.validate_User_Guess(30) # make a guess of 30
        assert test_game.turns == initial_turns + 1 # assert that the number of turns has incremented by 1

    def test_attempt_limit_reached(self):
        """Tests that the attempt limit is reached correctly after the specified number of turns"""

        test_game = game(secret_number=50, attempt_limit=3) # create a new game instance with a secret number of 50 and an attempt limit of 3
        test_game.validate_User_Guess(30) # make a guess of 30
        test_game.validate_User_Guess(40) # make a guess of 40
        test_game.validate_User_Guess(60) # make a guess of 60
        assert test_game.attempt_limit_reached() == True # assert that the attempt limit has been reached after 3 guesses

    def test_round_ignores_invalid_input(self):
        """Tests that the play_round method ignores invalid input and does not increment turns"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        initial_turns = test_game.turns # store the initial number of turns
        test_game.play_round("invalid") # make an invalid guess
        assert test_game.turns == initial_turns # assert that the number of turns has not incremented after an invalid guess

    def test_round_show_hints_and_wins(self):
        """Tests that the play_round method shows hints and wins correctly"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        test_game.play_round(30) # make a guess of 30
        test_game.play_round(50) # make a guess of 50

    def test_quit_returns_none(self):
        """Tests that the play_round method returns None when the user chooses to quit"""

        test_game = game(secret_number=50, attempt_limit=5) # create a new game instance with a secret number of 50 and an attempt limit of 5
        result = test_game.play_round(None) # simulate the user choosing to quit
        assert result is None # assert that the result is None when the user quits

    def test_attempt_limit_ends_round(self):
        """Tests that the play_round method ends the round when the attempt limit is reached"""

        test_game = game(secret_number=50, attempt_limit=3) # create a new game instance with a secret number of 50 and an attempt limit of 3
        test_game.play_round(30) # make a guess of 30
        test_game.play_round(40) # make a guess of 40
        test_game.play_round(60) # make a guess of 60
        result = test_game.play_round(70) # make a guess of 70 after reaching the attempt limit
        assert result is None # assert that the result is None when the attempt limit is reached
