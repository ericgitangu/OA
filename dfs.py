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
        'E': ['F'],
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
          F
    """
    
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
    
    def __iter__(self):
        self.stack = [self.start]
        return self

    def __next__(self):
        if not self.stack:
            raise StopIteration
        node = self.stack.pop()
        if node not in self.visited:
            self.visited.add(node)
            self.stack.extend(reversed(self.graph[node]))
            return node
        return self.__next__()

    def dfs(self, start):
        """
        Perform a depth-first search (DFS) traversal of the graph.
        
        Parameters:
        start (Any): The starting node for the DFS traversal.
        
        Returns:
        None: The function prints the nodes in the order they are visited during the DFS traversal.
        """
        self.start = start
        for node in self:
            print(colored(node, 'blue'), end=",", sep=",", flush=True)
    
    def __repr__(self):
        return f"DFS(graph={self.graph}, visited={self.visited})"

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

print("DFS Traversal:")
dfs = DFS(graph)
dfs.dfs('A')
print(f"\nRepresentation: {dfs}")