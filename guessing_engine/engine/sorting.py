# sorting.py: sorts lists by key using insertion sort or merge sort. No using .sort or sorted() functions.

class Sorter:
    
    """Base class for sorting algorithms"""

    def orderItems(self, items, key):

        """Sorts a list of items based on a specified key called by child classes"""
        
        raise NotImplementedError("Subclasses should implement this method.")

# Insertion Sort

class InsertionSorter(Sorter):

    """Implements the insertion sort algorithm"""

    def orderItems(self, items, key):

        """Sorts a list of items using insertion sort"""

        result = list(items)
        i = 1
        
        while i < len(result):
            current = result[i]
            j = i - 1
        
        while j >= 0 and key(result[j]) > key(current):
            result[j + 1] = result[j]
            j -= 1
        
        result[j + 1] = current
        i += 1 
        
        return result


# Merge Sort

class MergeSorter(Sorter):
    
    """Implements the merge sort algorithm"""

    def orderItems(self, items, key):

        """Sorts a list of items using merge sort"""
    
        if len(items) <= 1:
            return list(items)
        
        middle = len(items) // 2
        left = self.orderItems(items[:middle], key)
        right = self.orderItems(items[middle:], key)

        return self.merge(left, right, key)

    def merge(self, left, right, key):

        """Merges two sorted lists into a single sorted list"""
    
        merged = []
        i = 0
        j = 0
        
        while i < len(left) and j < len(right):
            if key(left[i]) <= key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            
        merged.extend(left[i:])
        merged.extend(right[j:])
        
        return merged
    
    def getSorter(name):
        
        """Returns an instance of the specified sorter class based on the name"""
        
        if name == "merge":
            return MergeSorter()
        return InsertionSorter()