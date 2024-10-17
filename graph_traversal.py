import itertools
from termcolor import colored

class GraphTraversal:
    """
    Problem Type: Graph Traversal, Path Finding
    
    Problem Statement:
    Given a graph represented as an adjacency list, a starting node, and an ending node, find all possible paths from the start node to the end node.
    
    Parameters:
    graph (Dict[Any, List[Any]]): The graph represented as an adjacency list.
    
    Methods:
    find_paths(start, end): Finds all possible paths from the start node to the end node.
    __repr__(): Returns a string representation of the graph.
    """
    
    def __init__(self, graph):
        self.graph = graph

    def find_paths(self, start, end, path=[]):
        """
        Find all possible paths from the start node to the end node.
        
        Parameters:
        start (Any): The starting node for the path finding.
        end (Any): The ending node for the path finding.
        path (List[Any], optional): The current path being traversed. Defaults to an empty list.
        
        Returns:
        List[List[Any]]: A list of all possible paths from the start node to the end node.
        """
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.graph:
            return []
        paths = []
        for node in self.graph[start]:
            if node not in path:
                newpaths = self.find_paths(node, end, path)
                for p in newpaths:
                    paths.append(p)
        return paths

    def __repr__(self):
        graph_repr = "\n".join([colored(f"{key}: {value}", 'yellow') for key, value in self.graph.items()])
        return colored(f"GraphTraversal(graph={{\n{graph_repr}\n}})", 'cyan')

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}

graph_traversal = GraphTraversal(graph)
print(colored("All paths from A to F:", 'blue'), colored(graph_traversal.find_paths('A', 'F'), 'green'))  # Output: [['A', 'B', 'E', 'F'], ['A', 'C', 'F']]
print(colored(repr(graph_traversal), 'magenta'))
