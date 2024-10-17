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
        Calculate the number of unique paths from the top-left to the bottom-right corner of the grid.
        
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

    def __repr__(self):
        return f"UniquePaths(memo={self.memo})"

# Example usage:
unique_paths = UniquePaths()
print("Unique Paths for a 3x7 grid:", unique_paths(3, 7))  # Output: 28
print("Unique Paths for a 3x2 grid:", unique_paths(3, 2))  # Output: 3
print("Unique Paths for a 7x3 grid:", unique_paths(7, 3))  # Output: 28
print("Unique Paths for a 3x3 grid:", unique_paths(3, 3))  # Output: 6
