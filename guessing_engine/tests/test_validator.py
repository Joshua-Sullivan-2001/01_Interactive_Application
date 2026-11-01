# test_validator.py: tests the input validation logic for the game.

from pathlib import Path # Import the Path class from the pathlib module to handle file paths.

from engine.validator import validate_Guess # Import the validate_Guess function from the validator module.

def test_validate_Guess():
    """ A function to test the validate_Guess function with various input cases. """
    
    # Test valid input
    result = validate_Guess("50") # Test the function with a valid input string representing a whole number within the valid range.
    assert result.ok == True, "Valid input should return ok=True" # Assert that the result indicates the input is valid.
    assert result.value == 50, "Valid input should return the correct value" # Assert that the result contains the correct value for the valid input.
    assert result.message is None, "Valid input should not return an error message" # Assert that the result does not contain an error message for valid input.

    # Test none string input
    result = validate_Guess(50) # Test the function with a none string input (integer) to check how it handles invalid types.
    assert result.ok == False, "Non-string input should return ok=False" # Assert that the result indicates the input is invalid.
    assert result.value is None, "Non-string input should not return a value" # Assert that the result does not contain a value for non-string input.
    assert result.message == "Input is not a text string.", "Non-string input should return the correct error message" # Assert that the result contains the correct error message for non-string input.

    # Test empty string
    result = validate_Guess("") # Test the function with an empty string to check how it handles empty input.
    assert result.ok == False, "Empty string should return ok=False" # Assert that the result indicates the input is invalid for an empty string.
    assert result.value is None, "Empty string should not return a value" # Assert that the result does not contain a value for an empty string.
    assert result.message == "Input is empty.", "Empty string should return the correct error message" # Assert that the result contains the correct error message for an empty string.

    # Test too long input
    long_input = "1" * 11  # 11 characters long 
    result = validate_Guess(long_input) # Test the function with an input string that exceeds the maximum allowed length to check how it handles overly long input.
    assert result.ok == False, "Too long input should return ok=False" # Assert that the result indicates the input is invalid for an overly long string.
    assert result.value is None, "Too long input should not return a value" # Assert that the result does not contain a value for an overly long string.
    assert result.message == f"Input is too long. Maximum length is 10 characters.", "Too long input should return the correct error message" # Assert that the result contains the correct error message for an overly long string.

    # Test negative number
    result = validate_Guess("-5") # Test the function with a negative number input to check how it handles invalid negative values.
    assert result.ok == False, "Negative number should return ok=False" # Assert that the result indicates the input is invalid for a negative number.
    assert result.value is None, "Negative number should not return a value" # Assert that the result does not contain a value for a negative number.
    assert result.message == "Input cannot be negative.", "Negative number should return the correct error message" # Assert that the result contains the correct error message for a negative number.

    # Test decimal number
    result = validate_Guess("5.5") # Test the function with a decimal number input to check how it handles invalid decimal values.
    assert result.ok == False, "Decimal number should return ok=False" # Assert that the result indicates the input is invalid for a decimal number.
    assert result.value is None, "Decimal number should not return a value" # Assert that the result does not contain a value for a decimal number.
    assert result.message == "Input cannot be a decimal number.", "Decimal number should return the correct error message" # Assert that the result contains the correct error message for a decimal number.

    # Test out of range
    result = validate_Guess("0") # Test the function with an input string representing a whole number that is below the valid range to check how it handles out-of-range values.
    assert result.ok == False, "Out of range should return ok=False" # Assert that the result indicates the input is invalid for a number below the valid range.
    assert result.value is None, "Out of range should not return a value" # Assert that the result does not contain a value for a number below the valid range.
    assert result.message == "Input is out of range. Please enter a whole number between 1 and 100.", "Out of range should return the correct error message"  # Assert that the result contains the correct error message for a number below the valid range.
    