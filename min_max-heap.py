import heapq

def min_heap_example(arr):
    """
    Problem Type: Heap, Min-Heap
    
    Problem Statement:
    Given an array of elements, convert it into a min-heap and perform basic heap operations such as pop and push.
    
    Parameters:
    arr (List[int]): The array of elements to be converted into a min-heap.
    
    Returns:
    None: The function prints the heap after each operation.
    
    Example:
    arr = [10, 1, 4, 6, 8, 5]
    min_heap_example(arr) -> Min-Heap: [1, 6, 4, 10, 8, 5]
                             Popped element: 1
                             Heap after push: [2, 4, 5, 10, 8, 6]
    
    Diagram:
    
        Initial array: [10, 1, 4, 6, 8, 5]
        
        Min-Heap: 
              1
            /   \
           6     4
          / \   /
         10  8  5
        
        After pop (1):
              4
            /   \
           6     5
          / \   
         10  8
        
        After push (2):
              2
            /   \
           4     5
          / \   /
         10  8  6
    """
    heapq.heapify(arr)
    print("Min-Heap:", arr)  # The smallest element is the root
    smallest = heapq.heappop(arr)  # Pops the smallest element
    print("Popped element:", smallest)
    heapq.heappush(arr, 2)  # Pushing new element into the heap
    print("Heap after push:", arr)

def max_heap_example(arr):
    """
    Problem Type: Heap, Max-Heap
    
    Problem Statement:
    Given an array of elements, convert it into a max-heap and perform basic heap operations such as pop.
    
    Parameters:
    arr (List[int]): The array of elements to be converted into a max-heap.
    
    Returns:
    None: The function prints the heap after each operation.
    
    Example:
    arr = [10, 1, 4, 6, 8, 5]
    max_heap_example(arr) -> Max-Heap: [10, 8, 5, 6, 1, 4]
                             Popped element: 10
    
    Diagram:
    
        Initial array: [10, 1, 4, 6, 8, 5]
        
        Max-Heap: 
              10
            /    \
           8      5
          / \    /
         6   1  4
        
        After pop (10):
              8
            /   \
           6     5
          / \   
         4   1
    """
    max_heap = [-num for num in arr]  # Convert to negative values
    heapq.heapify(max_heap)
    print("Max-Heap:", [-num for num in max_heap])  # Convert back to positive

    largest = -heapq.heappop(max_heap)  # Pops the largest element
    print("Popped element:", largest)

# Example usage:
arr = [10, 1, 4, 6, 8, 5]
min_heap_example(arr[:])
max_heap_example(arr[:])
