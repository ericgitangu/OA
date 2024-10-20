from collections import deque
from termcolor import colored

class Graph:
    def __init__(self, adjacency_list):
        self.graph = adjacency_list
        """
        Graph Representation:
        
        The graph is represented as an adjacency list, which is a dictionary where the keys are the nodes
        and the values are lists of neighboring nodes. For example, the following graph:
        
            A
           / \
          B   C
         / \   \
        D   E   F
             \
              G
        
        Can be represented as:
        
        {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['G'],
            'F': []
        }
        """

    def bfs(self, start):
        """
        Problem Type: Graph Traversal, Breadth-First Search (BFS)
        
        Problem Statement:
        Given a graph represented as an adjacency list and a starting node, perform a breadth-first search (BFS) traversal of the graph.
        
        Parameters:
        start (Any): The starting node for the BFS traversal.
        
        Returns:
        None: The function prints the nodes in the order they are visited during the BFS traversal.
        
        Example:
        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['F'],
            'F': []
        }
        graph.bfs('A') -> A B C D E F
        """
        visited = set()
        queue = deque([start])
        
        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                print(colored(vertex, 'green'), end=", ", sep="", flush=True)
                visited.add(vertex)
                queue.extend([neighbor for neighbor in self.graph[vertex] if neighbor not in visited])
        print(f"\nTraversal Complete: {visited} \n")
        
    def __repr__(self):
        return f"Graph(adjacency_list={self.graph})"

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': []
}

g = Graph(graph)
print(colored("\nGraph Structure:", 'magenta'))
print(colored(repr(g), 'cyan'))
print(colored("\nBFS Traversal:", 'magenta'))
g.bfs('B')  # Output: B D E G
