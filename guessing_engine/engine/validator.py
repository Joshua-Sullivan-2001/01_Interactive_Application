# validator.py: checks that typed text is a whole number from 1 to 100.

from dataclasses import dataclass # Define a data class to hold the validation result.

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

@dataclass
class ValidationResult:
    