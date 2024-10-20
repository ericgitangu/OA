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
        
        Breadth-First Search (BFS) is an algorithm for traversing or searching tree or graph data structures. 
        It starts at the tree root (or some arbitrary node of a graph, sometimes referred to as a 'search key') 
        and explores the neighbor nodes at the present depth prior to moving on to nodes at the next depth level.
        
        The BFS algorithm works as follows:
        1. Initialize a queue and add the starting node to it.
        2. Initialize a set to keep track of visited nodes.
        3. Loop until the queue is empty:
            a. Pop a node from the left side of the queue.
            b. If the node has not been visited:
                i. Print the node.
                ii. Mark the node as visited.
                iii. Add all unvisited neighbors of the node to the queue.

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
        # Initialize a set to keep track of visited nodes
        visited = set()
        # Initialize a queue and add the starting node to it
        queue = deque([start])
        
        # Loop until the queue is empty
        while queue:
            # Pop a node from the left side of the queue
            vertex = queue.popleft()
            # If the node has not been visited
            if vertex not in visited:
                # Print the node
                print(colored(vertex, 'green'), end=", ", sep="", flush=True)
                # Mark the node as visited
                visited.add(vertex)
                # Add all unvisited neighbors of the node to the queue
                queue.extend([neighbor for neighbor in self.graph[vertex] if neighbor not in visited])
        
        # Reinitialize the visited set and queue for a second traversal
        visited = set()
        queue = deque([start])
        
        # Loop until the queue is empty
        while queue:
            # Pop a node from the left side of the queue
            vertex = queue.popleft()
            # If the node has not been visited
            if vertex not in visited:
                # Print the node
                print(colored(vertex, 'green'), end=", ", sep="", flush=True)
                # Mark the node as visited
                visited.add(vertex)
                # Add all unvisited neighbors of the node to the queue
                queue.extend([neighbor for neighbor in self.graph[vertex] if neighbor not in visited])
        # Print the set of visited nodes after the second traversal
        print(f"\n{colored('Nodes Visited:', 'red')} {colored(visited, 'green')}")
        
    def __repr__(self):
        return f"{colored('Graph:', 'green')} {colored(self.graph, 'green')}"

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
print(f"{colored('-'*100, 'red')}")
print(colored(repr(g), 'cyan'))
print(f"{colored('-'*100, 'red')}")
print(colored("\nBFS Traversal:", 'magenta'))
print(f"{colored('-'*100, 'red')}")
g.bfs('B')  # Output: B D E G
print(f"{colored('-'*100, 'red')}")
