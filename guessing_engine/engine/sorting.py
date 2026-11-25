# sorting.py: sorts lists by key using insertion sort or merge sort. No using .sort or sorted() functions.

class Sorter: # Base class for the sorting algorithms
    
    """Base class for sorting algorithms"""

    def orderItems(self, items, key): # A Function to sort a list of items based on a specified key. This method is intended to be overridden by subclasses that implement specific sorting algorithms

        """Sorts a list of items based on a specified key called by child classes"""
        
        raise NotImplementedError("Subclasses should implement this method.") # Raises a NotImplementedError if the method is called directly from the base class indicating that subclasses should provide their own implementation of the orderItems method

# Insertion Sort

class insertionSorter(Sorter): # A subclass of Sorter that implements the insertion sort

    """Implements the insertion sort algorithm"""

    def orderItems(self, items, key): # A function to sort a list of items using the insertion sort algorithm based on a specified key. This method overrides the orderItems method from the Sorter base class

        """Sorts a list of items using insertion sort"""

        result = list(items) # Create a copy of the input list to avoid modifying the original list during sorting
        i = 1 # Initialize the index for the current element to be inserted into the sorted portion of the list
        
        while i < len(result): # Loop through the list starting from the second element (index 1) to the end of the list
            current = result[i] # Store the current element to be inserted into the sorted portion of the list
            j = i - 1 # Initialize the index for the last element in the sorted portion of the list
        
            while j >= 0 and key(result[j]) > key(current): # Compare the current element with elements in the sorted portion of the list using the specified key function. If the current element is smaller than the compared element shift the compared element to the right to make space for the current element
                result[j + 1] = result[j] # Shift the compared element to the right to make space for the current element
                j -= 1 # Decrement the index to continue comparing with the previous elements in the sorted portion of the list
            
            result[j + 1] = current # Insert the current element into its correct position in the sorted portion of the list
            i += 1 # Increment the index to move to the next element in the list for sorting
        
        return result # Return the sorted list after all elements have been processed and inserted into their correct positions

# Merge Sort

class mergeSorter(Sorter): # A subclass of Sorter that implements the merge sort
    
    """Implements the merge sort algorithm"""

    def orderItems(self, items, key): # A function to sort a list of items using the merge sort algorithm based on a specified key. This method overrides the orderItems method from the Sorter base class

        """Sorts a list of items using merge sort"""
    
        if len(items) <= 1: # If the list has one or zero elements it is already sorted so return a copy of the list
            return list(items) # Return a copy of the input list to avoid modifying the original list during sorting
        
        middle = len(items) // 2 # Find the middle index of the list to divide it into two halves
        left = self.orderItems(items[:middle], key) # Recursively sort the left half of the list using merge sort
        right = self.orderItems(items[middle:], key) # Recursively sort the right half of the list using merge sort

        return self.merge(left, right, key) # Merge the two sorted halves into a single sorted list using the merge function

    def merge(self, left, right, key): # A function to merge two sorted lists into a single sorted list based on a specified key. This method is used by the orderItems method to combine the sorted halves of the list

        """Merges two sorted lists into a single sorted list"""
    
        merged = [] # Initialize an empty list to hold the merged result of the two sorted lists
        i = 0 # Initialize the index for the left list to keep track of the current element being compared
        j = 0 # Initialize the index for the right list to keep track of the current element being compared
        
        while i < len(left) and j < len(right): # While there are still elements in both the left and right lists to be compared
            if key(left[i]) <= key(right[j]): # Compare the current elements from both lists using the specified key function. If the current element from the left list is less than or equal to the current element from the right list append it to the merged list
                merged.append(left[i]) # Append the current element from the left list to the merged list
                i += 1 # Increment the index for the left list to move to the next element for comparison
            else: # If the current element from the right list is less than the current element from the left list append it to the merged list
                merged.append(right[j]) # Append the current element from the right list to the merged list
                j += 1 # Increment the index for the right list to move to the next element for comparison
            
        merged.extend(left[i:]) # If there are any remaining elements in the left list after the main comparison loop append them to the merged list
        merged.extend(right[j:]) # If there are any remaining elements in the right list after the main comparison loop append them to the merged list
        
        return merged # Return the merged list which is now sorted based on the specified key function

def getSorter(name): # A function to return an instance of the specified sorter class based on the name provided. If the name is "merge" it returns an instance of MergeSorter otherwise it returns an instance of InsertionSorter
    
    """Returns an instance of the specified sorter class based on the name"""
    
    if name == "merge": # If the name provided is "merge" return an instance of MergeSorter
        return mergeSorter() # Return an instance of MergeSorter
    return insertionSorter() # Return an instance of InsertionSorter for any other name (default behavior)
