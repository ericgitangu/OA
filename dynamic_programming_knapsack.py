from termcolor import colored

class Knapsack:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.dp = self._knapsack()

    def _knapsack(self):
        """Standard O(n*W) space 2D DP table approach."""
        n = len(self.values)
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(1, self.capacity + 1):
                if self.weights[i - 1] <= w:
                    dp[i][w] = max(dp[i - 1][w], self.values[i - 1] + dp[i - 1][w - self.weights[i - 1]])
                else:
                    dp[i][w] = dp[i - 1][w]

        return dp

    def _knapsack_optimized(self):
        """Space-optimized O(W) 1D rolling array approach."""
        dp = [0 for _ in range(self.capacity + 1)]
        for i in range(len(self.values)):
            # Traverse backwards to avoid using the same item multiple times
            for w in range(self.capacity, self.weights[i] - 1, -1):
                dp[w] = max(dp[w], self.values[i] + dp[w - self.weights[i]])
        return dp

    def __repr__(self):
        result = self._knapsack_optimized()[-1]
        dp_table = "\n".join([colored(f"{row}", 'yellow') for row in self.dp])
        return colored(
            f"Knapsack Problem:\nWeights: {self.weights}\nValues: {self.values}\n"
            f"Capacity: {self.capacity}\n"
            f"DP Table (2D - Educational): \n{dp_table}\n"
            f"Optimized DP (1D): {self._knapsack_optimized()}\n"
            f"Maximum Value: {result}",
            'cyan'
        )

    def __call__(self):
        return self._knapsack_optimized()[-1]

# Example usage:
weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7
knapsack = Knapsack(weights, values, capacity)
print(colored("Maximum value in Knapsack:", 'green'), colored(knapsack(), 'yellow'))
print(knapsack)
