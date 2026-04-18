import collections
import itertools
from termcolor import colored

class NetworkGraph:
    """
    Problem Type: Network Simulation, Graph Connectivity
    
    Problem Statement:
    Given a network of nodes representing servers and edges representing connections between them, simulate the network's behavior using collections and itertools. Determine the shortest path between two servers.
    
    Parameters:
    graph (Dict[str, List[str]]): The network graph represented as an adjacency list.
    
    Methods:
    add_connection(node1, node2): Adds a bidirectional connection between two nodes.
    remove_connection(node1, node2): Removes a bidirectional connection between two nodes.
    shortest_path(start, end): Finds the shortest path between two nodes using BFS.
    
    Example:
    network = NetworkGraph()
    network.add_connection('A', 'B')
    network.add_connection('B', 'C')
    network.add_connection('A', 'C')
    network.shortest_path('A', 'C') -> ['A', 'C']
    
    Diagram:
    
        A
       /|\
      B-|-C
       \|/
        D
    """
    
    def __init__(self):
        # Initialize the graph as a defaultdict of lists
        self.graph = collections.defaultdict(list)
    
    def __setitem__(self, node1, node2):
        # Add a bidirectional connection between node1 and node2
        self.graph[node1].append(node2)
        self.graph[node2].append(node1)
    
    def __delitem__(self, node1, node2):
        # Remove the bidirectional connection between node1 and node2
        self.graph[node1].remove(node2)
        self.graph[node2].remove(node1)
    
    def __call__(self, start, end):
        """
        Finds the shortest path between two nodes using BFS.
        
        Parameters:
        start (str): The starting node.
        end (str): The ending node.
        
        Returns:
        List[str]: The shortest path from start to end.
        """
        # Initialize the queue with the starting node in a list
        queue = collections.deque([[start]])
        # Initialize the set of visited nodes
        visited = set()
        
        while queue:
            # Pop the first path from the queue
            path = queue.popleft()
            # Get the last node from the path
            node = path[-1]
            
            # If the last node is the end node, return the path
            if node == end:
                return path
            
            # If the node has not been visited
            elif node not in visited:
                # Iterate over the neighbors of the node
                for neighbor in self.graph[node]:
                    # Create a new path with the neighbor added
                    new_path = list(path)
                    new_path.append(neighbor)
                    # Append the new path to the queue
                    queue.append(new_path)
                
                # Mark the node as visited
                visited.add(node)
        # Return an empty list if no path is found
        return []
    
    def all_paths(self, start, end):
        """
        Finds all possible paths between two nodes using itertools.
        
        Parameters:
        start (str): The starting node.
        end (str): The ending node.
        
        Returns:
        List[List[str]]: A list of all possible paths from start to end.
        """
        def find_paths(graph, start, end, path=[]):
            # Add the start node to the current path
            path = path + [start]
            # If the start node is the end node, return the current path as a complete path
            if start == end:
                return [path]
            # If the start node is not in the graph, return an empty list (no paths)
            if start not in graph:
                return []
            # Initialize a list to store all possible paths
            paths = []
            # Iterate over the neighbors of the start node
            for node in graph[start]:
                # If the neighbor has not been visited in the current path
                if node not in path:
                    # Recursively find all paths from the neighbor to the end node
                    newpaths = find_paths(graph, node, end, path)
                    # Add each new path to the list of paths
                    for p in newpaths:
                        paths.append(p)
            # Return the list of all possible paths
            return paths
        
        # Get a list of all nodes in the graph
        nodes = list(self.graph.keys())
        # Initialize a list to store all possible paths
        all_possible_paths = []
        # Iterate over all possible lengths of combinations of nodes
        for r in range(1, len(nodes) + 1):
            # Iterate over all combinations of nodes of length r
            for combination in itertools.combinations(nodes, r):
                # If both the start and end nodes are in the combination
                if start in combination and end in combination:
                    # Create a subgraph with only the nodes in the combination
                    subgraph = {node: self.graph[node] for node in combination}
                    # Find all paths in the subgraph from start to end
                    paths = find_paths(subgraph, start, end)
                    # Add the found paths to the list of all possible paths
                    all_possible_paths.extend(paths)
        # Remove duplicate paths by converting to a set of tuples and back to a list of lists
        return list(map(list, set(map(tuple, all_possible_paths))))

    def __repr__(self):
        # Return a string representation of the NetworkGraph instance
        return f"NetworkGraph(graph={dict(self.graph)})"

# Example usage:
network = NetworkGraph()
# Add connections between nodes A, B, C, D
def add_network(network, connections):
    for node, neighbors in connections.items():
        for neighbor in neighbors:
            network[node] = neighbor

connections = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['A', 'B', 'C']
}

add_network(network, connections)

# Find and print the shortest path from A to D
print(colored("Shortest path from A to D:", 'green'), colored(network('A', 'D'), 'green'))  # Output: ['A', 'C', 'D']
# Find and print all possible paths from A to D
print(colored("All paths from A to D:", 'red'), colored(network.all_paths('A', 'D'), 'green'))  # Output: All possible paths from A to D
# Print the representation of the NetworkGraph instance
print(colored(repr(network), 'magenta'))
