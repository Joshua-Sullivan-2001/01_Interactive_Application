# validator.py: checks that typed text is a whole number from 1 to 100

# Constants for validation
minValue = 1 # Define the minimum value for the valid range of whole numbers
maxValue = 100 # Define the maximum value for the valid range of whole numbers
maxInputLength = 10 # Define the maximum length of the input string

# Error messages for invalid input
notATextMessage = "Input is not a text string." # Error message for non-string input
emptyMessage = "Input is empty." # Error message for empty input
messageTooLong = f"Input is too long. Maximum length is {maxInputLength} characters." # Error message for input that exceeds the maximum length
noNegativeNumbersMessage = "Input cannot be negative." # Error message for negative input
noDecimalNumbersMessage = "Input cannot be a decimal number." # Error message for decimal input
notANumberMessage = "Input is not a number." # Error message for non-numeric input
outOfRangeMessage = f"Input is out of range. Please enter a whole number between {minValue} and {maxValue}." # Error message for input that is out of the valid range

class validationResult: # The class to hold the result of the validation process including whether the input is valid, the value of the input and any error message
    
    """ A class to hold the result of the validation process including whether the input is valid, the value of the input and any error message. """


    def __init__(self, ok, value, message): # The initial startup function for the validationResult class that takes in three parameters: ok, value, and message
        
        """ A function to create a validationResult object with the specified parameters."""

        self.ok = ok # A boolean indicating whether the input is valid
        self.value = value # The value of the input if valid
        self.message = message # An error message if the input is invalid

def outputError(message): # A function to create a validationResult object for an invalid input with the specified error message
    
    """ A function to create a validationResult object for an invalid input with the specified error message. """

    return validationResult(False, None, message) # Return a validationResult object indicating invalid input

def validateGuess(inputText): # A function to validate the user's guess input ensuring it is a whole number between 1 and 100
    
    """A function to validate the user's guess input ensuring it is a whole number between 1 and 100."""

    if type(inputText) is not str: # Check if the input is not a string
        return outputError(notATextMessage) # Return an error message for non-string input

    cleanedInput = inputText.strip() # Remove leading and trailing whitespace from the input

    if len(cleanedInput) == 0: # Check if the input is empty
        return outputError(emptyMessage) # Return an error message for empty input

    if len(cleanedInput) > maxInputLength: # Check if the input is too long
        return outputError(messageTooLong) # Return an error message for input that exceeds the maximum length

    if "." in cleanedInput: # Check if the text contains a decimal point
        return outputError(noDecimalNumbersMessage) # Return an error message for decimal input

    digitsOnly = cleanedInput.lstrip("-") # Remove any minus signs from the front of the string to check for digits only
    
    if digitsOnly.isdigit() == False or digitsOnly.isascii() == False: # Check for letters and symbols (isascii blocks odd digits)
        return outputError(notANumberMessage) # Return an error message for non-numeric input

    try: # Try block to convert the cleaned input to an integer
        value = int(cleanedInput) # Attempt to convert the input to an integer
    except ValueError: # If the conversion fails, it's not a valid number
        return outputError(notANumberMessage) # Return an error message for non-numeric input

    if value < 0: # Check if the input is negative
        return outputError(noNegativeNumbersMessage) # Return an error message for negative input

    if value < minValue or value > maxValue: # Check if the input is out of range
        return outputError(outOfRangeMessage) # Return an error message for input that is out of the valid range

    return validationResult(True, value, None) # Return a validationResult object indicating valid input
