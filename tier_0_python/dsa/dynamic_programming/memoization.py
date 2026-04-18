from termcolor import colored
import time

class UniquePaths:
    """
    Problem Type: Dynamic Programming, Memoization
    
    Problem Statement:
    A robot is located at the top-left corner of a m x n grid (marked 'Start' in the diagram below).
    The robot can only move either down or right at any point in time. The robot is trying to reach the bottom-right corner of the grid (marked 'Finish' in the diagram below).
    How many possible unique paths are there?
    
    Parameters:
    m (int): Number of rows in the grid.
    n (int): Number of columns in the grid.
    
    Methods:
    unique_paths(m, n): Returns the number of unique paths from the top-left to the bottom-right corner of the grid.
    
    Example:
    unique_paths = UniquePaths()
    unique_paths.unique_paths(3, 7) -> 28
    
    Diagram:
    
    The grid:
    
    S -> * -> * -> * -> * -> * -> *
    *    *    *    *    *    *    *
    *    *    *    *    *    *    F
    
    The robot can move either down or right at any point in time.
    """
    
    def __init__(self):
        self.memo = {}

    def __call__(self, m, n):
        return self.unique_paths(m, n)

    def unique_paths(self, m, n):
        """
        Calculate the number of unique paths from the top-left to the bottom-right corner of the grid using memoization.
        
        Parameters:
        m (int): Number of rows in the grid.
        n (int): Number of columns in the grid.
        
        Returns:
        int: The number of unique paths from the top-left to the bottom-right corner of the grid.
        """
        if (m, n) in self.memo:
            return self.memo[(m, n)]
        
        if m == 1 or n == 1:
            return 1
        
        self.memo[(m, n)] = self.unique_paths(m - 1, n) + self.unique_paths(m, n - 1)
        return self.memo[(m, n)]

    def unique_paths_no_memo(self, m, n):
        """
        Calculate the number of unique paths from the top-left to the bottom-right corner of the grid without using memoization.
        
        Parameters:
        m (int): Number of rows in the grid.
        n (int): Number of columns in the grid.
        
        Returns:
        int: The number of unique paths from the top-left to the bottom-right corner of the grid.
        """
        if m == 1 or n == 1:
            return 1
        
        return self.unique_paths_no_memo(m - 1, n) + self.unique_paths_no_memo(m, n - 1)

    def __repr__(self):
        print(colored('-' * 100, 'red'))
        memo_repr = "\n".join([f"{key}: {value}" for key, value in self.memo.items()])
        return f"UniquePaths(memo={{\n{memo_repr}\n}})"

def benchmark_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    duration = end_time - start_time
    return result, duration

# Example usage:
unique_paths = UniquePaths()

# Benchmark with memoization
result_memo, duration_memo = benchmark_function(unique_paths, 10, 10)
print(colored("Unique Paths for a 10x10 grid with memoization:", 'blue'), colored(result_memo, 'green'))
print(colored(f"Time taken with memoization: {duration_memo:.6f} seconds", 'yellow'))

print('-' * 100)

# Benchmark without memoization
result_no_memo, duration_no_memo = benchmark_function(unique_paths.unique_paths_no_memo, 10, 10)
print(colored("Unique Paths for a 10x10 grid without memoization:", 'blue'), colored(result_no_memo, 'green'))
print(colored(f"Time taken without memoization: {duration_no_memo:.6f} seconds", 'yellow'))

print(colored(repr(unique_paths), 'magenta'))
