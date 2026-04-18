from termcolor import colored

class Knapsack:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.dp = self._knapsack()

    def _knapsack(self):
        n = len(self.values)
        dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(1, self.capacity + 1):
                if self.weights[i - 1] <= w:
                    dp[i][w] = max(dp[i - 1][w], self.values[i - 1] + dp[i - 1][w - self.weights[i - 1]])
                else:
                    dp[i][w] = dp[i - 1][w]

        return dp

    def __repr__(self):
        result = self.dp[len(self.values)][self.capacity]
        dp_table = "\n".join([colored(f"{row}", 'yellow') for row in self.dp])
        return colored(f"Knapsack Problem:\nWeights: {self.weights}\nValues: {self.values}\nCapacity: {self.capacity}\nDP Table:\n{dp_table}\nMaximum Value: {result}", 'cyan')

    def __call__(self):
        return self.dp[len(self.values)][self.capacity]

# Example usage:
weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7
knapsack = Knapsack(weights, values, capacity)
print(colored("Maximum value in Knapsack:", 'green'), colored(knapsack(), 'yellow'))
print(knapsack)
