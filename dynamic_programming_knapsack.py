def knapsack(weights, values, capacity):
    """
    Problem Type: Dynamic Programming, 0/1 Knapsack Problem
    
    Problem Statement:
    Given weights and values of n items, put these items in a knapsack of capacity W to get the maximum total value in the knapsack.
    
    Parameters:
    weights (List[int]): List of weights of the items.
    values (List[int]): List of values of the items.
    capacity (int): Maximum weight capacity of the knapsack.
    
    Returns:
    int: The maximum value that can be put in a knapsack of the given capacity.
    
    Example:
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    capacity = 7
    knapsack(weights, values, capacity) -> 9
    
    Diagram:
    
    Let's consider the example with weights = [1, 3, 4, 5], values = [1, 4, 5, 7], and capacity = 7.
    
    The DP table (dp) will be filled as follows:
    
        Capacity
        0  1  2  3  4  5  6  7
    0  [0, 0, 0, 0, 0, 0, 0, 0]
    1  [0, 1, 1, 1, 1, 1, 1, 1]
    2  [0, 1, 1, 4, 5, 5, 5, 5]
    3  [0, 1, 1, 4, 5, 6, 6, 9]
    4  [0, 1, 1, 4, 5, 7, 8, 9]
    
    The maximum value that can be put in the knapsack of capacity 7 is 9.
    """
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

# Example usage:
weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7
print("Maximum value in Knapsack:", knapsack(weights, values, capacity))
