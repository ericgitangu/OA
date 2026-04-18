from termcolor import colored

class DFS:
    """
    Problem Type: Graph Traversal, Depth-First Search (DFS)
    
    Problem Statement:
    Given a graph represented as an adjacency list and a starting node, perform a depth-first search (DFS) traversal of the graph.
    
    Parameters:
    graph (Dict[Any, List[Any]]): The graph represented as an adjacency list.
    start (Any): The starting node for the DFS traversal.
    visited (Set[Any], optional): The set of already visited nodes. Defaults to None.
    
    Returns:
    None: The function prints the nodes in the order they are visited during the DFS traversal.
    
    Example:
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['G'],
        'F': []
    }
    dfs = DFS(graph)
    dfs.dfs('A') -> A B D E F C
    
    Diagram:
    
        A
       / \
      B   C
     / \   \
    D   E   F
         \
          G
    """
    
    def __init__(self, graph):
        # Initialize the graph and the visited set
        self.graph = graph
        self.visited = set()
    
    def __iter__(self):
        # Initialize the stack with the starting node
        self.stack = [self.start]
        return self

    def __next__(self):
        # If the stack is empty, stop the iteration
        if not self.stack:
            raise StopIteration
        # Pop a node from the stack
        node = self.stack.pop()
        # If the node has not been visited, mark it as visited and add its neighbors to the stack
        if node not in self.visited:
            self.visited.add(node)
            self.stack.extend(reversed(self.graph[node]))
            return node
        # If the node has already been visited, continue to the next node
        return self.__next__()

    def dfs(self, start):
        """
        Problem Type: Graph Traversal, Depth-First Search (DFS)
        
        Depth-First Search (DFS) is an algorithm for traversing or searching tree or graph data structures. 
        The algorithm starts at the root node (selecting some arbitrary node as the root in the case of a graph) 
        and explores as far as possible along each branch before backtracking.
        
        The DFS algorithm works as follows:
        1. Initialize a stack and add the starting node to it.
        2. Initialize a set to keep track of visited nodes.
        3. Loop until the stack is empty:
            a. Pop a node from the stack.
            b. If the node has not been visited:
                i. Print the node.
                ii. Mark the node as visited.
                iii. Add all unvisited neighbors of the node to the stack.
        
        Problem Statement:
        Given a graph represented as an adjacency list and a starting node, perform a depth-first search (DFS) traversal of the graph.
        
        Parameters:
        start (Any): The starting node for the DFS traversal.
        
        Returns:
        None: The function prints the nodes in the order they are visited during the DFS traversal.
        
        Example:
        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['G'],
            'F': []
        }
        dfs.dfs('A') -> A B D E G C F
        """
        # Set the starting node
        
        self.start = start
        # Iterate through the nodes using the custom iterator
        for node in self:
            # Print the visited node
            if node != self.start:
                print(",", end="", flush=True)
            print(colored(node, 'blue'), end="", flush=True)
        print()

    def __repr__(self):
        # Return a string representation of the DFS object
        return f"\n{colored('DFS', 'red')}\n{colored('-'*100, 'red')}\n{colored('graph', 'red')}= {self.graph},\n{colored('visited', 'red')}= {self.visited},\n{colored('start', 'red')}= {self.start}\n{colored('-'*100, 'red')}"

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

print(colored("\nDFS Traversal:", 'green'))
dfs = DFS(graph)
dfs.dfs('A')
print(f"\n{colored('Representation:', 'magenta')} {dfs}")