class TravellingSalesman:
    """
    Problem Type: Graph, Travelling Salesman Problem (TSP)
    
    Problem Statement:
    Given a graph represented as an adjacency matrix and a starting node, find the shortest possible route that visits each node exactly once and returns to the starting node.
    
    Parameters:
    graph (List[List[int]]): The graph represented as an adjacency matrix.
    start (int): The starting node for the TSP.
    
    Methods:
    __init__(graph, start): Initializes the TSP with the given graph and starting node.
    __call__(): Solves the TSP and returns the minimum cost and the path.
    __repr__(): Returns a string representation of the TSP instance.
    
    Example:
    graph = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]
    tsp = TravellingSalesman(graph, 0)
    tsp() -> (80, [0, 1, 3, 2, 0])
    
    Diagram:
    
        0
       /|\
      10|15
     /  |  \
    1---|---2
     \  |  /
      25|30
       \|/
        3
    """
    
    def __init__(self, graph, start):
        # Initialize the TSP with the given graph and starting node
        self.graph = graph
        self.start = start
        # Number of nodes in the graph
        self.n = len(graph)
        # Bitmask representing all nodes visited
        self.all_visited = (1 << self.n) - 1
        # Memoization table to store the minimum cost for each state
        self.memo = [[None] * self.n for _ in range(1 << self.n)]

    def __call__(self):
        # Solve the TSP and get the minimum cost
        min_cost = self._tsp(1 << self.start, self.start)
        # Reconstruct the path from the memoization table
        path = [self.start] + self._find_path(1 << self.start, self.start)
        # Append the starting node to complete the cycle
        path.append(self.start)
        return min_cost, path

    def _tsp(self, mask, pos):
        """
        Helper function to solve the TSP using dynamic programming and bit masking.
        
        Parameters:
        mask (int): The bitmask representing the set of visited nodes.
        pos (int): The current node position.
        
        Returns:
        int: The minimum cost to complete the TSP from the current state.
        """
        # If all nodes have been visited, return the cost to return to the start node
        if mask == self.all_visited:
            return self.graph[pos][self.start]
        # If the result is already computed, return it
        if self.memo[mask][pos] is not None:
            return self.memo[mask][pos]

        # Initialize the minimum cost to infinity
        min_cost = float('inf')
        # Try to visit all unvisited nodes and calculate the minimum cost
        for city in range(self.n):
            if mask & (1 << city) == 0:
                new_cost = self.graph[pos][city] + self._tsp(mask | (1 << city), city)
                min_cost = min(min_cost, new_cost)

        # Store the result in the memoization table
        self.memo[mask][pos] = min_cost
        return min_cost

    def _find_path(self, mask, pos):
        """
        Helper function to reconstruct the path of the TSP from the memoization table.
        
        Parameters:
        mask (int): The bitmask representing the set of visited nodes.
        pos (int): The current node position.
        
        Returns:
        List[int]: The path of the TSP from the current state.
        """
        # If all nodes have been visited, return the start node
        if mask == self.all_visited:
            return [self.start]
        # Reconstruct the path by finding the next node that matches the minimum cost
        for city in range(self.n):
            if mask & (1 << city) == 0:
                if self.memo[mask][pos] == self.graph[pos][city] + self._tsp(mask | (1 << city), city):
                    return [city] + self._find_path(mask | (1 << city), city)
        return []

    def __repr__(self):
        return f"TravellingSalesman(graph={self.graph}, start={self.start})"

# Example usage:
graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
tsp = TravellingSalesman(graph, 0)
print("Travelling Salesman Problem:")
min_cost, path = tsp()
print(f"Minimum cost: {min_cost}")
print(f"Path: {path}")

