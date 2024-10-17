import itertools

def find_paths(graph, start, end, path=[]):
    """
    Problem Type: Graph Traversal, Path Finding
    
    Problem Statement:
    Given a graph represented as an adjacency list, a starting node, and an ending node, find all possible paths from the start node to the end node.
    
    Parameters:
    graph (Dict[Any, List[Any]]): The graph represented as an adjacency list.
    start (Any): The starting node for the path finding.
    end (Any): The ending node for the path finding.
    path (List[Any], optional): The current path being traversed. Defaults to an empty list.
    
    Returns:
    List[List[Any]]: A list of all possible paths from the start node to the end node.
    
    Example:
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }
    find_paths(graph, 'A', 'F') -> [['A', 'B', 'E', 'F'], ['A', 'C', 'F']]
    
    Diagram:
    
        A
       / \
      B   C
     / \   \
    D   E   F
         \
          F
    """
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_paths(graph, node, end, path)
            for p in newpaths:
                paths.append(p)
    return paths

# Example usage:
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
print("\nAll Paths from A to F:")
print(find_paths(graph, 'A', 'F'))  # Output: All paths from A to F
