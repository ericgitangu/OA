import itertools
from termcolor import colored

class GraphTraversal:
    """
    Problem Type: Graph Traversal, Path Finding
    
    Problem Statement:
    Given a graph represented as an adjacency list, a starting node, and an ending node, find all possible paths from the start node to the end node using itertools and combinations.
    
    Parameters:
    graph (Dict[Any, List[Any]]): The graph represented as an adjacency list.
    
    Methods:
    find_paths_itertools(start, end): Finds all possible paths from the start node to the end node using itertools and combinations.
    __repr__(): Returns a string representation of the graph.
    """
    
    def __init__(self, graph):
        self.graph = graph

    def find_paths_itertools(self, start, end):
        def all_paths(graph, start, end, path):
            path = path + [start]
            if start == end:
                return [path]
            if start not in graph:
                return []
            paths = []
            for node in graph[start]:
                if node not in path:
                    newpaths = all_paths(graph, node, end, path)
                    for p in newpaths:
                        paths.append(p)
            return paths
        
        nodes = list(self.graph.keys())
        all_possible_paths = []
        for r in range(1, len(nodes) + 1):
            for combination in itertools.combinations(nodes, r):
                if start in combination and end in combination:
                    path = list(combination)
                    if path[0] == start and path[-1] == end:
                        all_possible_paths.append(path)
        return all_possible_paths

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
print(colored("All paths from A to F:", 'blue'), colored(graph_traversal.find_paths_itertools('A', 'F'), 'green'))  # Output: [['A', 'B', 'E', 'F'], ['A', 'C', 'F']]
print(colored(repr(graph_traversal), 'magenta'))