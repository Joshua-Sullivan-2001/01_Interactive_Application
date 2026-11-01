# validator.py: checks that typed text is a whole number from 1 to 100.

# constants for validation
min_value = 1 # Define the minimum value for the valid range of whole numbers.
max_value = 100 # Define the maximum value for the valid range of whole numbers.
max_input_length = 10 # Define the maximum length of the input string.

# error messages for invalid input
not_a_text_message = "Input is not a text string." # Error message for non-string input.
empty_message = "Input is empty." # Error message for empty input.
message_too_long = f"Input is too long. Maximum length is {max_input_length} characters." # Error message for input that exceeds the maximum length.
no_negative_numbers_message = "Input cannot be negative." # Error message for negative input.
no_decimal_numbers_message = "Input cannot be a decimal number." # Error message for decimal input.
not_a_number_message = "Input is not a number." # Error message for non-numeric input.
out_of_range_message = f"Input is out of range. Please enter a whole number between {min_value} and {max_value}." # Error message for input that is out of the valid range.

class validationResult:
    """ A class to hold the result of the validation process, including whether the input is valid, the value of the input, and any error message. """


    def __init__(self, ok, value, message):
        """ A function to create a validationResult object with the specified parameters."""
        
        self.ok = ok # A boolean indicating whether the input is valid.
        self.value = value # The value of the input if valid.
        self.message = message # An error message if the input is invalid.

def output_Error(message):
    """ A function to create a validationResult object for an invalid input with the specified error message. """
    
    return validationResult(False, None, message) # Return a validationResult object indicating invalid input.

def validate_Guess(input_text):
    """A function to validate the user's guess input ensuring it is a whole number between 1 and 100."""
    
    if type(input_text) is not str: # Check if the input is not a string.
        return output_Error(not_a_text_message) # Return an error message for non-string input.

    cleaned_input = input_text.strip() # Remove leading and trailing whitespace from the input.

    if len(cleaned_input) == 0: # Check if the input is empty.
        return output_Error(empty_message) # Return an error message for empty input.

    if len(cleaned_input) > max_input_length: # Check if the input is too long.
        return output_Error(message_too_long) # Return an error message for input that exceeds the maximum length.

    try:
        value = int(cleaned_input) # Attempt to convert the input to an integer.
    except ValueError: # If the conversion fails, it's not a valid number.
        return output_Error(not_a_number_message) # Return an error message for non-numeric input.

    if value < 0: # Check if the input is negative.
        return output_Error(no_negative_numbers_message) # Return an error message for negative input.

    if value != float(value): # Check if the input is a decimal number.
        return output_Error(no_decimal_numbers_message) # Return an error message for decimal input.

    if value < min_value or value > max_value: # Check if the input is out of range.
        return output_Error(out_of_range_message) # Return an error message for input that is out of the valid range.

    return validationResult(True, value, None) # Return a validationResult object indicating valid input.
