# test_sorting.py: tests the sorting functionality for the leaderboard and other components

from engine.sorting import Sorter, insertionSorter, mergeSorter, getSorter # Import the necessary classes and functions from the sorting module
from engine.leaderboard import getTurns # Import the getTurns function from the leaderboard module to be used as a key for sorting records

def justTheNumber(item): # A simple key function that returns the item itself used for sorting numbers
    
    """This function is used as a key for sorting numbers. It simply returns the item itself."""
    
    return item # Return the item itself which is used as the key for sorting numbers in the tests


def isInOrder(items, key): # A utility function to check if a list of items is in order based on a provided key function
    
    """This function checks if the given list of items is in order based on the provided key function."""
    
    for i in range(1, len(items)): # Iterate through the list of items starting from the second item
        if key(items[i - 1]) > key(items[i]): # If the key of the previous item is greater than the key of the current item the list is not in order
            return False # Return False indicating that the list is not in order
    return True # Return True indicating that the list is in order


def bothSorters(): # A utility function that returns a list of both sorting algorithm instances (insertion sort and merge sort) to be used in the tests
    
    """This function returns a list containing instances of both the insertionSorter and mergeSorter classes. It is used to test both sorting algorithms in the test cases."""
    
    return [insertionSorter(), mergeSorter()] # Return a list containing instances of both the insertionSorter and mergeSorter classes which will be used in the test cases to ensure that both sorting algorithms are tested for correctness and consistency
    
class TestSorting: # A test class that contains various test cases to validate the sorting functionality of the Sorter classes and their behavior with different types of input data
    
    """This class contains test cases to validate the sorting functionality of the Sorter classes and their behavior with different types of input data. It tests various scenarios including empty lists, single items, already sorted lists, reversed lists, duplicates and sorting records by turns. It also checks that both sorting algorithms give the same result and that the base Sorter class raises a NotImplementedError when its orderItems method is called."""
    
    def testEmptyList(self): # A test case that checks the behavior of the sorting algorithms when given an empty list as input
        
        """This test case checks the behavior of the sorting algorithms when given an empty list as input. It ensures that both sorting algorithms return an empty list when provided with an empty input list confirming that they handle this edge case correctly."""
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with an empty list
            assert sorter.orderItems([], justTheNumber) == [], "An empty list should stay empty." # Assert that the result of calling the orderItems method on the sorter with an empty list and the justTheNumber key function returns an empty list confirming that both sorting algorithms handle this edge case correctly

    def testSingleItem(self): # A test case that checks the behavior of the sorting algorithms when given a list containing a single item as input
        
        """This test case checks the behavior of the sorting algorithms when given a list containing a single item as input. It ensures that both sorting algorithms return the same single item in a list when provided with a list containing one item confirming that they handle this edge case correctly."""
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with a list containing a single item
            assert sorter.orderItems([7], justTheNumber) == [7], "A single item should stay as it is." # Assert that the result of calling the orderItems method on the sorter with a list containing a single item (7) and the justTheNumber key function returns the same single item in a list confirming that both sorting algorithms handle this edge case correctly

    def testAlreadySorted(self): # A test case that checks the behavior of the sorting algorithms when given a list that is already sorted in ascending order as input
        
        """This test case checks the behavior of the sorting algorithms when given a list that is already sorted in ascending order as input. It ensures that both sorting algorithms return the same sorted list when provided with an already sorted list confirming that they handle this case correctly and do not alter the order of the items."""
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with a list that is already sorted in ascending order
            assert sorter.orderItems([1, 2, 3, 4, 5], justTheNumber) == [1, 2, 3, 4, 5], "A sorted list should stay sorted." # Assert that the result of calling the orderItems method on the sorter with a list that is already sorted in ascending order ([1, 2, 3, 4, 5]) and the justTheNumber key function returns the same sorted list confirming that both sorting algorithms handle this case correctly and do not alter the order of the items

    def testReversed(self): # A test case that checks the behavior of the sorting algorithms when given a list that is sorted in descending order (reversed) as input
        
        """This test case checks the behavior of the sorting algorithms when given a list that is sorted in descending order (reversed) as input. It ensures that both sorting algorithms return the same sorted list in ascending order when provided with a reversed list confirming that they handle this case correctly and can sort the items into the correct order."""
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with a list that is sorted in descending order (reversed)
            assert sorter.orderItems([5, 4, 3, 2, 1], justTheNumber) == [1, 2, 3, 4, 5], "A reversed list should be put in order." # Assert that the result of calling the orderItems method on the sorter with a list that is sorted in descending order ([5, 4, 3, 2, 1]) and the justTheNumber key function returns the same sorted list in ascending order confirming that both sorting algorithms handle this case correctly and can sort the items into the correct order

    def testDuplicates(self): # A test case that checks the behavior of the sorting algorithms when given a list containing duplicate items as input
        
        """This test case checks the behavior of the sorting algorithms when given a list containing duplicate items as input. It ensures that both sorting algorithms return the same sorted list with all duplicates preserved when provided with a list containing duplicate items confirming that they handle this case correctly and do not remove or alter the duplicates."""
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with a list containing duplicate items
            assert sorter.orderItems([3, 1, 3, 2, 1], justTheNumber) == [1, 1, 2, 3, 3], "Duplicates should all be kept." # Assert that the result of calling the orderItems method on the sorter with a list containing duplicate items ([3, 1, 3, 2, 1]) and the justTheNumber key function returns the same sorted list with all duplicates preserved ([1, 1, 2, 3, 3]) confirming that both sorting algorithms handle this case correctly and do not remove or alter the duplicates

    def testOriginalListIsNotChanged(self): # A test case that checks that the original list passed to the sorting algorithms is not modified after sorting
        
        """This test case checks that the original list passed to the sorting algorithms is not modified after sorting. It ensures that both sorting algorithms return a new sorted list and do not alter the original list confirming that they handle this case correctly and maintain the integrity of the input data."""
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test that the original list passed to the sorting algorithms is not modified after sorting
            original = [3, 1, 2] # Define the original list to be sorted
            sorter.orderItems(original, justTheNumber) # Call the orderItems method on the sorter with the original list and the justTheNumber key function to sort the list
            assert original == [3, 1, 2], "The original list should not be changed." # Assert that the original list remains unchanged ([3, 1, 2]) after calling the orderItems method confirming that both sorting algorithms return a new sorted list and do not alter the original list maintaining the integrity of the input data

    def testSortsRecordsByTurns(self): # A test case that checks the behavior of the sorting algorithms when given a list of records (dictionaries) containing player initials and their corresponding number of turns taken as input
        
        """This test case checks the behavior of the sorting algorithms when given a list of records (dictionaries) containing player initials and their corresponding number of turns taken as input. It ensures that both sorting algorithms return the same sorted list of records ordered by the number of turns taken in ascending order when provided with a list of records confirming that they handle this case correctly and can sort complex data structures based on a specific key."""
        
        records = [{"initials": "AAA", "turns": 9}, {"initials": "BBB", "turns": 3}, {"initials": "CCC", "turns": 6}] # Define a list of records (dictionaries) containing player initials and their corresponding number of turns taken to be sorted
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with a list of records containing player initials and their corresponding number of turns taken
            ranked = sorter.orderItems(records, getTurns) # Call the orderItems method on the sorter with the list of records and the getTurns key function to sort the records by the number of turns taken
            assert [r["initials"] for r in ranked] == ["BBB", "CCC", "AAA"], "Records should be ordered by turns." # Assert that the result of calling the orderItems method on the sorter with the list of records and the getTurns key function returns the same sorted list of records ordered by the number of turns taken in ascending order (["BBB", "CCC", "AAA"]) confirming that both sorting algorithms handle this case correctly and can sort complex data structures based on a specific key

    def testTiesKeepTheirOriginalOrder(self): # A test case that checks the behavior of the sorting algorithms when given a list of records (dictionaries) containing player initials and their corresponding number of turns taken as input where some records have the same number of turns taken (ties)
        
        """This test case checks the behavior of the sorting algorithms when given a list of records (dictionaries) containing player initials and their corresponding number of turns taken as input, where some records have the same number of turns taken (ties). It ensures that both sorting algorithms return the same sorted list of records ordered by the number of turns taken in ascending order while preserving the original order of tied records when provided with a list of records containing ties confirming that they handle this case correctly and maintain the stability of the sorting algorithm."""
        
        records = [{"initials": "AAA", "turns": 5}, {"initials": "BBB", "turns": 5}, {"initials": "CCC", "turns": 2}, {"initials": "DDD", "turns": 5}] # Define a list of records (dictionaries) containing player initials and their corresponding number of turns taken to be sorted, where some records have the same number of turns taken (ties)
        
        for sorter in bothSorters(): # Iterate through both sorting algorithm instances (insertion sort and merge sort) to test their behavior with a list of records containing player initials and their corresponding number of turns taken where some records have the same number of turns taken (ties)
            ranked = sorter.orderItems(records, getTurns) # Call the orderItems method on the sorter with the list of records and the getTurns key function to sort the records by the number of turns taken while preserving the original order of tied records
            assert [r["initials"] for r in ranked] == ["CCC", "AAA", "BBB", "DDD"], "Tied records should keep their original order." # Assert that the result of calling the orderItems method on the sorter with the list of records and the getTurns key function returns the same sorted list of records ordered by the number of turns taken in ascending order while preserving the original order of tied records (["CCC", "AAA", "BBB", "DDD"]) confirming that both sorting algorithms handle this case correctly and maintain the stability of the sorting algorithm

    def testBothSortersGiveTheSameAnswer(self): # A test case that checks that both sorting algorithms (insertion sort and merge sort) give the same sorted result when given the same list of random numbers as input
        
        """This test case checks that both sorting algorithms (insertion sort and merge sort) give the same sorted result when given the same list of random numbers as input. It ensures that both sorting algorithms return the same sorted list when provided with a list of random numbers confirming that they handle this case correctly and produce consistent results across different sorting algorithms."""
        
        import random # Import the random module to generate a list of random numbers for testing the sorting algorithms
        generator = random.Random(1) # Create a random number generator with a fixed seed (1) to ensure reproducibility of the random numbers generated for testing the sorting algorithms
        data = [] # Initialize an empty list to hold the random numbers generated for testing the sorting algorithms
        
        for _ in range(300): # Generate 300 random numbers between 1 and 50 and append them to the data list for testing the sorting algorithms
            data.append(generator.randint(1, 50)) # Append a random integer between 1 and 50 generated by the random number generator to the data list for testing the sorting algorithms
        
        insertionResult = insertionSorter().orderItems(data, justTheNumber) # Call the orderItems method on the insertionSorter instance with the list of random numbers and the justTheNumber key function to sort the random numbers using insertion sort
        mergeResult = mergeSorter().orderItems(data, justTheNumber) # Call the orderItems method on the mergeSorter instance with the list of random numbers and the justTheNumber key function to sort the random numbers using merge sort
        
        assert insertionResult == mergeResult, "Both sorters should agree." # Assert that the result of calling the orderItems method on both sorting algorithms with the same list of random numbers and the justTheNumber key function returns the same sorted list confirming that both sorting algorithms handle this case correctly and produce consistent results across different sorting algorithms.
        assert isInOrder(insertionResult, justTheNumber), "The answer should be in order." # Assert that the result of calling the orderItems method on both sorting algorithms with the same list of random numbers and the justTheNumber key function returns the same sorted list confirming that both sorting algorithms handle this case correctly and produce consistent results across different sorting algorithms. Also assert that the sorted result is in order and that no numbers are lost or added during the sorting process.
        assert len(insertionResult) == len(data), "No numbers should be lost or added." # Assert that the result of calling the orderItems method on both sorting algorithms with the same list of random numbers and the justTheNumber key function returns the same sorted list confirming that both sorting algorithms handle this case correctly and produce consistent results across different sorting algorithms. Also assert that the sorted result is in order and that no numbers are lost or added during the sorting process.

    def testBaseSorterCannotSort(self): # A test case that checks that the base Sorter class raises a NotImplementedError when its orderItems method is called as it is an abstract class and should not be instantiated directly
        
        """This test case checks that the base Sorter class raises a NotImplementedError when its orderItems method is called as it is an abstract class and should not be instantiated directly. It ensures that the base Sorter class cannot be used to sort items and that any attempt to do so raises the appropriate exception confirming that the class is designed to be subclassed and that its orderItems method must be implemented in the subclasses."""
        
        try: # Attempt to call the orderItems method on an instance of the base Sorter class with a list containing a single item and the justTheNumber key function to test that it raises a NotImplementedError as expected
            Sorter().orderItems([1], justTheNumber) # Call the orderItems method on an instance of the base Sorter class with a list containing a single item and the justTheNumber key function to test that it raises a NotImplementedError as expected
            raised = False # Initialize a variable to track whether the NotImplementedError was raised during the attempt to call the orderItems method on the base Sorter class
        except NotImplementedError: # Catch the NotImplementedError exception raised when attempting to call the orderItems method on the base Sorter class and set the raised variable to True indicating that the exception was raised as expected
            raised = True # Set the raised variable to True indicating that the NotImplementedError exception was raised as expected when attempting to call the orderItems method on the base Sorter class
            
        assert raised, "The base class should raise NotImplementedError." #

    def testGetSorter(self): # A test case that checks the behavior of the getSorter function when given different sorting algorithm names as input ensuring that it returns the correct sorter instance based on the provided name
        
        """This test case checks the behavior of the getSorter function when given different sorting algorithm names as input ensuring that it returns the correct sorter instance based on the provided name. It tests that the function returns an instance of the mergeSorter class when given the name "merge" an instance of the insertionSorter class when given the name "insertion" and defaults to returning an instance of the insertionSorter class for any unknown names confirming that the function handles these cases correctly and returns the appropriate sorter instance based on the provided name."""
        
        assert isinstance(getSorter("merge"), mergeSorter), "merge should give the merge sorter." # Assert that the result of calling the getSorter function with the name "merge" returns an instance of the mergeSorter class confirming that the function handles this case correctly and returns the appropriate sorter instance based on the provided name.
        assert isinstance(getSorter("insertion"), insertionSorter), "insertion should give the insertion sorter." # Assert that the result of calling the getSorter function with the name "insertion" returns an instance of the insertionSorter class confirming that the function handles this case correctly and returns the appropriate sorter instance based on the provided name.
        assert isinstance(getSorter("anything else"), insertionSorter), "Unknown names should give the insertion sorter." # Assert that the result of calling the getSorter function with an unknown name (anything else) returns an instance of the insertionSorter class confirming that the function handles this case correctly and defaults to returning the appropriate sorter instance for any unknown names.
