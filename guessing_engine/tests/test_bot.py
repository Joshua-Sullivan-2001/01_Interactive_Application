# test_bot.py: tests the bot's guessing logic and strategy

from engine.bot import binaryBot, randomBot, loopStop # Import the binaryBot and randomBot classes as well as the loopStop constant from the engine.bot module
from engine.game import Game, tooLow, tooHigh # Import the Game class and the tooLow and tooHigh constants from the engine.game module
from engine.simulation import runSimulation, summarizeResults # Import the runSimulation and summarizeResults functions from the engine.simulation module
from engine.validator import minValue, maxValue # Import the minValue and maxValue constants from the engine.validator module

class recordingGame(Game): # A function that creates a subclass of Game to record the guesses made by the bot
    
    """A subclass of Game that records the guesses made by the bot."""
    
    def __init__(self, secretNumber = None): # Initialize the recordingGame with a secret number and an empty list of guesses
        
        """Initializes the recordingGame with a secret number and an empty list of guesses."""
        
        super().__init__(secretNumber) # Call the class Game constructor to initialize the secret number and other attributes
        self.guessList = [] # Initialize an empty list to store the guesses made by the bot

    def validateUserGuess(self, userGuess): # Override the validateUserGuess method to record the guess and then call the parent class's method to judge it
        
        """Records the guess and then calls the parent class's method to judge it."""
        
        self.guessList.append(userGuess) # Append the user's guess to the guessList to keep track of all guesses made during the game
        return super().validateUserGuess(userGuess) # Call the parent class's validateUserGuess method to determine if the guess is too low, too high or correct

class neverCorrectGame(Game): # A subclass of Game that always returns too low for any guess simulating a game where the bot can never finish
    
    """A subclass of Game that always returns too low for any guess simulating a game where the bot can never finish."""
    
    def validateUserGuess(self, userGuess): # Override the validateUserGuess method to always return too low simulating a game where the bot can never finish
        
        """Always returns too low simulating a game where the bot can never finish."""
        
        self.turns += 1 # Increment the turns counter to keep track of how many guesses have been made even though the bot will never guess correctly.
        return tooLow # Always return tooLow to simulate a game where the bot can never finish regardless of the guess made

class TestBinaryBot: # Tests for the binaryBot class
    
    """Tests for the binaryBot class."""
    
    def testPickGuessIsTheMiddle(self): # Test that the pickGuess method returns the middle of the range
        
        """Test that the pickGuess method returns the middle of the range."""
        
        assert binaryBot().pickGuess(1, 100) == 50, "The middle of 1 to 100 is 50." # Assert that the pickGuess method returns 50 when given the range 1 to 100 which is the middle of that range
        assert binaryBot().pickGuess(1, 49) == 25, "The middle of 1 to 49 is 25." # Assert that the pickGuess method returns 25 when given the range 1 to 49 which is the middle of that range
        assert binaryBot().pickGuess(7, 7) == 7, "With one number left the guess is that number." # Assert that the pickGuess method returns 7 when given the range 7 to 7 which is the only number left in that range.

    def testFindsEveryNumberInSevenGuessesOrFewer(self): # Test that the binaryBot can find any number from 1 to 100 in at most 7 guesses
        
        """Test that the binaryBot can find any number from 1 to 100 in at most 7 guesses."""
        
        for secret in range(minValue, maxValue + 1): # Loop through every number from minValue to maxValue (inclusive) to test that the binaryBot can find each number in at most 7 guesses
            guesses = binaryBot().play(Game(secretNumber = secret)) # Play a game with the binaryBot using the current secret number and store the number of guesses it took to find the secret number
            assert guesses is not None, f"The bot should find {secret}." # Assert that the number of guesses is not None meaning the bot found the secret number and if it is None raise an assertion error with a message indicating that the bot should have found the secret number
            assert guesses <= 7, f"The bot took {guesses} guesses for {secret}." # Assert that the number of guesses is not None (meaning the bot found the secret number) and that it took 7 or fewer guesses to find the secret number as expected for a binary search strategy

    def testGuessCountMatchesTheGameTurns(self): # Test that the number of guesses returned by the binaryBot matches the number of turns counted by the Game
        
        """Test that the number of guesses returned by the binaryBot matches the number of turns counted by the Game."""
        
        currentGame = Game(secretNumber = 37) # Create a new instance of the Game class with a secret number of 37 to test that the number of guesses returned by the binaryBot matches the number of turns counted by the Game
        guesses = binaryBot().play(currentGame) # Play the game with the binaryBot and store the number of guesses it took to find the secret number in the variable guesses
        assert guesses == currentGame.turns, "The bot and the game should count the same turns." # Assert that the number of guesses returned by the binaryBot matches the number of turns counted by the Game and if they do not match raise an assertion error with a message indicating that the bot and the game should count the same turns
        assert currentGame.finished == True, "The game should be finished." # Assert that the game is finished after the binaryBot has found the secret number and if it is not finished raise an assertion error with a message indicating that the game should be finished

    def testGuessesStayInsideTheRange(self): # Test that every guess made by the binaryBot is within the valid range of 1 to 100
        
        """Test that every guess made by the binaryBot is within the valid range of 1 to 100."""
        
        for secret in (1, 50, 100): # Loop through a few secret numbers (1, 50 and 100) to test that every guess made by the binaryBot is within the valid range of 1 to 100
            currentGame = recordingGame(secret) # Create a new instance of the recordingGame class with the current secret number to record the guesses made by the binaryBot during the game
            binaryBot().play(currentGame) # Play the game with the binaryBot using the current secret number and record the guesses made by the bot in the currentGame instance
            for guess in currentGame.guessList: # Loop through each guess made by the binaryBot during the game and assert that it is within the valid range of 1 to 100 raising an assertion error with a message indicating that the guess is outside the range if it is not within the valid range
                assert minValue <= guess <= maxValue, f"{guess} is outside the range." # Assert that each guess made by the binaryBot is within the valid range of 1 to 100 and if it is not within the valid range raise an assertion error with a message indicating that the guess is outside the range

    def testStopsAtTheLoopLimit(self): # Test that the binaryBot stops after loopStop guesses if it never finds the correct number
        
        """Test that the binaryBot stops after loopStop guesses if it never finds the correct number."""
        
        currentGame = neverCorrectGame(secretNumber = 50) # Create a new instance of the neverCorrectGame class with a secret number of 50 to test that the binaryBot stops after loopStop guesses if it never finds the correct number
        assert binaryBot().play(currentGame) is None, "The bot should give up and return None." # Assert that the binaryBot returns None after loopStop guesses if it never finds the correct number and if it does not return None raise an assertion error with a message indicating that the bot should give up and return None
        assert currentGame.turns == loopStop, "The bot should stop at the loop limit." # Assert that the number of turns counted by the neverCorrectGame instance is equal to loopStop,indicating that the binaryBot stopped after loopStop guesses and if it does not equal loopStop raise an assertion error with a message indicating that the bot should stop at the loop limit

class TestRandomBot: # Test the randomBot class
    
    """Tests for the randomBot class."""
    
    def testPickGuessIsInsideTheRange(self): # Test that every random guess made by the randomBot is within the valid range provided to it
        
        """Test that every random guess made by the randomBot is within the valid range provided to it."""
        
        bot = randomBot() # Create an instance of the randomBot class to test that every random guess made by the bot is within the valid range provided to it
        
        for _ in range(500): # Loop 500 times to test that every random guess made by the randomBot is within the valid range provided to it ensuring that the bot's guessing logic is functioning correctly and consistently
            guess = bot.pickGuess(20, 30) # Pick a random guess between 20 and 30 using the randomBot's pickGuess method and store it in the variable guess
            assert 20 <= guess <= 30, f"{guess} is outside 20 to 30." # Assert that the random guess made by the randomBot is within the valid range of 20 to 30 and if it is not within the valid range raise an assertion error with a message indicating that the guess is outside the range

    def testFindsTheNumberOrGivesUpCleanly(self): # Test that the randomBot either finds the secret number or gives up cleanly after loopStop guesses
        
        """Test that the randomBot either finds the secret number or gives up cleanly after loopStop guesses."""
        
        for secret in (1, 50, 100): # Loop through a few secret numbers (1, 50 and 100) to test that the randomBot either finds the secret number or gives up cleanly after loopStop guesses
            guesses = randomBot().play(Game(secretNumber = secret)) # Play a game with the randomBot using the current secret number and store the number of guesses it took to find the secret number or None if it gave up in the variable guesses
            assert guesses is None or 1 <= guesses <= loopStop, "The result should be None or from 1 to loopStop." # Assert that the number of guesses returned by the randomBot is either None (if it gave up) or between 1 and loopStop (inclusive) indicating that the bot either found the secret number or gave up cleanly after loopStop guesses and if it does not meet this condition raise an assertion error with a message indicating that the result should be None or from 1 to loopStop

class TestBotComparison: # Test that compares the performance of the binaryBot and randomBot over many games
    
    """Tests that compares the performance of the binaryBot and randomBot over many games."""
    
    def testBinaryBotBeatsRandomBotOnAverage(self): # Test that the binaryBot needs fewer guesses on average than the randomBot over many games
        
        """Test that the binaryBot needs fewer guesses on average than the randomBot over many games."""
        
        binaryResults = runSimulation(binaryBot, 300, 1) # Run a simulation of 300 games with the binaryBot and store the results in binaryResults
        randomResults = runSimulation(randomBot, 300, 1) # Run a simulation of 300 games with the randomBot and store the results in randomResults
        binaryAverage = summarizeResults(binaryResults)[2] # Calculate the average number of guesses for the binaryBot by summarizing the results and extracting the average value
        randomAverage = summarizeResults(randomResults)[2] # Calculate the average number of guesses for the randomBot by summarizing the results and extracting the average value
        assert binaryAverage < randomAverage, "Binary search should be better on average." # Assert that the average number of guesses for the binaryBot is less than the average number of guesses for the randomBot indicating that the binary search strategy is more efficient on average and if it is not less raise an assertion error with a message indicating that binary search should be better on average
        assert summarizeResults(binaryResults)[1] <= 7, "The binary bot should never need more than 7 guesses." # Assert that the maximum number of guesses for the binaryBot is less than or equal to 7 indicating that the binary search strategy should never need more than 7 guesses to find the secret number and if it is not less than or equal to 7 raise an assertion error with a message indicating that the binary bot should never need more than 7 guesses

    def testSummarizeResults(self): # Test that the summarizeResults function correctly summarizes a list of results by returning the minimum, maximum and average values
        
        """Test that the summarizeResults function correctly summarizes a list of results by returning the minimum, maximum and average values."""
        
        assert summarizeResults([4, 2, 6]) == (2, 6, 4.0), "The summary should be 2 and 6 and 4.0." # Assert that the summarizeResults function correctly summarizes the list of results [4, 2, 6] by returning a tuple containing the minimum value (2), maximum value (6) and average value (4.0) and if it does not return this tuple raise an assertion error with a message indicating what the summary should be
        assert summarizeResults([]) == (0, 0, 0.0), "An empty list should give zeros." # Assert that the summarizeResults function correctly summarizes an empty list by returning a tuple containing zeros for the minimum, maximum and average values (0, 0, 0.0) and if it does not return this tuple raise an assertion error with a message indicating that an empty list should give zeros
