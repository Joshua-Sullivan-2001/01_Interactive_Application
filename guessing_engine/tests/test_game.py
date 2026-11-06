# test_game.py: tests the game logic and flow.

from engine.display import display # Import the display base class that the fake display will copy.
from engine.game import game, too_low, too_high, correct # Import the game class and the constants from the game module.

class fakeDisplay(display): # A pretend display that gives scripted answers and remembers what it was asked to show.
    """A fake display for testing the game logic. It takes a list of answers to give when asked for a guess, and remembers any messages it was asked to show."""
    
    def __init__(self, answers):
        """Creates the fake display with a list of typed answers."""
        
        self.answers = answers # The list of typed answers to hand out.
        self.errors = [] # The error messages shown.
        self.hints = [] # The hint messages shown.
        self.wins = [] # The turn counts shown in win messages.
        self.messages = [] # Any other messages shown.
    
    def get_guess(self):
        """Returns the next scripted answer or None when there are none left."""
        
        if len(self.answers) == 0: # If there are no more answers left in the list.
            return None # None means the player quit.
        return self.answers.pop(0) # The pop(0) removes and returns the first answer.
    
    def show_error(self, error_message):
        """Remembers an error message."""
        
        self.errors.append(error_message) # Append the error message to the errors list.
    
    def show_hint(self, hint_message):
        """Remembers a hint message."""
        
        self.hints.append(hint_message) # Append the hint message to the hints list.
    
    def show_win(self, turns):
        """Remembers the turns shown in a win message."""
        
        self.wins.append(turns) # Append the number of turns to the wins list.
    
    def show_message(self, message):
        """Remembers any other message."""
        
        self.messages.append(message) # Append the message to the messages list.

class Test_Game: # The name must start with Test so pytest finds it.
    """Tests for the game class."""
    
    def test_low_guess(self):
        """Tests the game logic for a low guess."""
        
        test_game = game(secret_number=50, attempt_limit=5) # Create a game with a secret number of 50.
        assert test_game.validate_user_guess(30) == too_low, "A guess of 30 should be too low" # 30 is below 50.
    
    def test_high_guess(self):
        """Tests the game logic for a high guess."""
        
        test_game = game(secret_number=50, attempt_limit=5) # Create a game with a secret number of 50.
        assert test_game.validate_user_guess(70) == too_high, "A guess of 70 should be too high" # 70 is above 50.
    
    def test_correct_guess_and_finish(self):
        """Tests the game logic for a correct guess and finishing the game."""
        
        test_game = game(secret_number=50, attempt_limit=5) # Create a game with a secret number of 50.
        assert test_game.validate_user_guess(50) == correct, "A guess of 50 should be correct" # The right number.
        assert test_game.finished == True, "The game should be finished after a correct guess" # The game is over.
    
    def test_turns_increment(self):
        """Tests that the turns go up by one for each guess."""
        
        test_game = game(secret_number=50, attempt_limit=5) # Create a game with a secret number of 50.
        test_game.validate_user_guess(30) # Make a guess of 30.
        assert test_game.turns == 1, "One guess should use one turn" # One turn used.
        test_game.validate_user_guess(40) # Make a guess of 40.
        assert test_game.turns == 2, "Two guesses should use two turns" # Two turns used.
    
    def test_random_secret_is_in_range(self):
        """Tests that a random secret is always from 1 to 100."""
        
        for _ in range(200): # Make many games because the secret is random.
            test_game = game() # Create a game with a random secret.
            assert 1 <= test_game.secret_number <= 100, "The secret number should be from 1 to 100" # The secret must be inside the range.
    
    def test_attempt_limit_reached(self):
        """Tests that the attempt limit is reached after the right number of turns."""
        
        test_game = game(secret_number=50, attempt_limit=2) # Create a game that allows only two guesses.
        test_game.validate_user_guess(30) # Make the first guess.
        assert test_game.attempt_limit_reached() == False, "One guess is left so the limit is not reached" # One guess is left.
        test_game.validate_user_guess(40) # Make the second guess.
        assert test_game.attempt_limit_reached() == True, "No guesses are left so the limit is reached" # None are left.
    
    def test_no_attempt_limit_never_runs_out(self):
        """Tests that None means unlimited attempts."""
        
        test_game = game(secret_number=50) # Create a game with no attempt limit.
        for _ in range(500): # Make many wrong guesses.
            test_game.validate_user_guess(1) # Guess 1 every time.
        assert test_game.attempt_limit_reached() == False, "With no limit the player never runs out" # The player never runs out.
        
    def test_round_ignores_invalid_input(self):
        """Tests that bad input is explained and does not use a turn."""
    
        screen = fakeDisplay(["abc", "", "50"]) # Two bad answers then the right one.
        test_game = game(secret_number=50) # Create a game with a secret number of 50.
        turns = test_game.play_round(screen) # Play the round.
        assert turns == 1, "Only the good guess should count as a turn" # Only the good guess counted.
        assert len(screen.errors) == 2, "Two errors should have been shown" # Two errors were shown.
    
    def test_round_shows_hints_and_win(self):
        """Tests that hints are shown in order and the win is shown once."""
        
        screen = fakeDisplay(["10", "90", "50"]) # Low then high then correct.
        test_game = game(secret_number=50) # Create a game with a secret number of 50.
        turns = test_game.play_round(screen) # Play the round.
        assert turns == 3, "Three guesses should give three turns" # Three guesses.
        assert screen.hints == [too_low, too_high], "The hints should be shown in order" # The hints in order.
        assert screen.wins == [3], "The win should be shown once with 3 turns" # The win was shown once.
    
    def test_quit_returns_none(self):
        """Tests that the round returns None when the player quits."""
        
        test_game = game(secret_number=50) # Create a game with a secret number of 50.
        assert test_game.play_round(fakeDisplay([])) is None, "No answers means the player quit" # No answers means quit.
    
    def test_attempt_limit_ends_round(self):
        """Tests that the round ends with no score when the attempts run out."""
        
        screen = fakeDisplay(["1", "2", "3"]) # Plenty of wrong answers.
        test_game = game(secret_number=50, attempt_limit=2) # Create a game that allows only two guesses.
        assert test_game.play_round(screen) is None, "The round should end early with no score" # The round ends early.
        assert len(screen.messages) == 1, "One message should reveal the secret number" # The message was shown once.
        assert "50" in screen.messages[0], "The message should include the secret number" # The secret is revealed.
    
    def test_correct_last_guess_still_wins(self):
        """Tests that a correct guess on the last allowed attempt counts as a win."""
        
        screen = fakeDisplay(["1", "50"]) # A wrong guess then the right one.
        test_game = game(secret_number=50, attempt_limit=2) # Create a game that allows only two guesses.
        assert test_game.play_round(screen) == 2, "A correct last guess should still win" # It is a win with 2 turns.
