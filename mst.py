"""
Minimum Spanning Tree (MST) — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Kruskal's Algorithm for MST (Intermediate),
           § Prim's Algorithm for MST (Intermediate)

Key insight from dsa.md:
  - MST connects all V vertices with exactly V-1 edges at minimum total weight.
  - Kruskal's: sort edges by weight, greedily add if it doesn't form a cycle.
    Uses Union-Find for O(α(n)) cycle detection. Best for sparse graphs.
    T: O(E log E)
  - Prim's: grow the MST from a seed vertex using a min-heap frontier.
    Best for dense graphs (fewer edges to manage in the heap).
    T: O(E log V)

Patterns covered:
  1. Kruskal's Algorithm          — edge-based, Union-Find
  2. Prim's Algorithm             — vertex-based, min-heap
  3. Min Cost to Connect All Points — LeetCode 1584 (Prim's on implicit graph)
  4. Optimize Water Distribution  — LeetCode 1168 (virtual node + Kruskal's)
"""

import heapq
from collections import defaultdict
from termcolor import colored


# ---------------------------------------------------------------------------
# Union-Find (needed by Kruskal's — see also union_find.py)
# ---------------------------------------------------------------------------
class _UF:
    """Minimal Union-Find with path compression and union by rank."""
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# ---------------------------------------------------------------------------
# 1. Kruskal's Algorithm
# ---------------------------------------------------------------------------
def kruskal(n: int, edges: list[tuple[int, int, int]]) -> tuple[list, int]:
    """
    Kruskal's MST Algorithm.

    Reference: dsa.md § Kruskal's Algorithm for MST (Intermediate)

    Approach:
      1. Sort all edges by weight.
      2. Greedily add the lightest edge that connects two different components
         (Union-Find detects if adding an edge would form a cycle).
      3. Stop when V-1 edges have been added.

    T: O(E log E)  — dominated by sorting; Union-Find ops are near O(1)
    S: O(V + E)    — Union-Find + sorted edge list

    Real-world analogy: a telecoms company laying the minimum total cable
    to connect all cities — always lay the cheapest available cable that
    connects two previously disconnected regions.

    Args:
        n:     number of vertices (0..n-1)
        edges: list of (weight, u, v) tuples

    Returns:
        (mst_edges, total_weight) where mst_edges is list of (u, v, weight)

    Example:
        >>> edges = [(1,0,1),(4,0,2),(2,1,2),(5,1,3),(3,2,3)]
        >>> mst, cost = kruskal(4, edges)
        >>> cost
        6
    """
    uf = _UF(n)
    mst_edges = []
    total_weight = 0

    for weight, u, v in sorted(edges):  # process lightest edges first
        if uf.union(u, v):              # only add if it doesn't form a cycle
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == n - 1:
                break  # MST complete

    return mst_edges, total_weight


# ---------------------------------------------------------------------------
# 2. Prim's Algorithm
# ---------------------------------------------------------------------------
def prim(graph: dict[int, list[tuple[int, int]]], start: int = 0) -> tuple[list, int]:
    """
    Prim's MST Algorithm using a min-heap.

    Reference: dsa.md § Prim's Algorithm for MST (Intermediate)

    Approach: Maintain a min-heap of (weight, vertex, parent) for the
    "frontier" — edges that cross from the MST into unvisited territory.
    Always expand the cheapest frontier edge.

    T: O(E log V)  — each edge pushed/popped from heap at most once
    S: O(V + E)    — heap + visited set

    Real-world analogy: growing a road network from a capital city —
    always build the cheapest road that reaches a new city.

    Args:
        graph: adjacency list {vertex: [(neighbour, weight), ...]}
        start: seed vertex (default 0)

    Returns:
        (mst_edges, total_weight) where mst_edges is list of (u, v, weight)

    Example:
        >>> g = {0:[(1,1),(2,4)], 1:[(0,1),(2,2),(3,5)],
        ...      2:[(0,4),(1,2),(3,3)], 3:[(1,5),(2,3)]}
        >>> mst, cost = prim(g)
        >>> cost
        6
    """
    visited: set[int] = set()
    mst_edges: list[tuple[int, int, int]] = []
    total_weight = 0
    heap = [(0, start, -1)]  # (weight, vertex, parent)

    while heap and len(visited) < len(graph):
        weight, u, parent = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if parent != -1:
            mst_edges.append((parent, u, weight))
            total_weight += weight
        for v, w in graph[u]:
            if v not in visited:
                heapq.heappush(heap, (w, v, u))

    return mst_edges, total_weight


# ---------------------------------------------------------------------------
# 3. Min Cost to Connect All Points
# ---------------------------------------------------------------------------
def min_cost_connect_points(points: list[list[int]]) -> int:
    """
    LeetCode 1584 — Min Cost to Connect All Points
    Connect all points with minimum total Manhattan distance.
    Manhattan distance between (x1,y1) and (x2,y2) = |x1-x2| + |y1-y2|.

    Approach: Prim's on an implicit complete graph (no need to build the
    full edge list — generate neighbours on the fly from the heap).

    T: O(V² log V)  — V² edges in a complete graph, each heap op O(log V)
    S: O(V²)        — heap can hold all edges

    Real-world analogy: laying the minimum total fibre-optic cable to
    connect a set of buildings on a city grid.

    Args:
        points: list of [x, y] coordinates

    Returns:
        minimum total cost (sum of Manhattan distances in MST)

    Example:
        >>> min_cost_connect_points([[0,0],[2,2],[3,10],[5,2],[7,0]])
        20
        >>> min_cost_connect_points([[3,12],[-2,5],[-4,1]])
        18
    """
    n = len(points)
    if n == 1:
        return 0

    visited = set()
    total = 0
    # Start from point 0; heap stores (cost, point_index)
    heap = [(0, 0)]

    while len(visited) < n:
        cost, i = heapq.heappop(heap)
        if i in visited:
            continue
        visited.add(i)
        total += cost
        xi, yi = points[i]
        for j in range(n):
            if j not in visited:
                dist = abs(xi - points[j][0]) + abs(yi - points[j][1])
                heapq.heappush(heap, (dist, j))

    return total


# ---------------------------------------------------------------------------
# 4. Optimize Water Distribution in a Village
# ---------------------------------------------------------------------------
def min_cost_to_supply_water(
    n: int, wells: list[int], pipes: list[list[int]]
) -> int:
    """
    LeetCode 1168 — Optimize Water Distribution in a Village
    Each house can either dig a well (cost wells[i]) or connect to another
    house via a pipe (cost pipes[i]). Find the minimum cost to supply water
    to all houses.

    Approach: Add a virtual node 0. For each house i, add an edge from 0
    to i with cost wells[i-1] (digging a well = connecting to the virtual
    water source). Then find the MST of this augmented graph using Kruskal's.

    T: O((V + E) log(V + E))
    S: O(V + E)

    Real-world analogy: deciding for each house whether to drill its own
    well or connect to a neighbour's water supply — modelled as an MST
    problem by treating "drill a well" as connecting to a central source.

    Args:
        n:     number of houses (1..n)
        wells: wells[i] = cost to dig a well at house i+1
        pipes: list of [house1, house2, cost] pipe connections

    Returns:
        minimum total cost

    Example:
        >>> min_cost_to_supply_water(3, [1,2,2], [[1,2,1],[2,3,1]])
        3
        >>> min_cost_to_supply_water(2, [1,1], [[1,2,2]])
        2
    """
    # Build edge list: virtual node 0 represents the water source
    edges = []
    for i, cost in enumerate(wells):
        edges.append((cost, 0, i + 1))  # well = edge from virtual node to house
    for h1, h2, cost in pipes:
        edges.append((cost, h1, h2))

    # Kruskal's on n+1 nodes (0 = virtual source, 1..n = houses)
    uf = _UF(n + 1)
    total = 0
    for cost, u, v in sorted(edges):
        if uf.union(u, v):
            total += cost

    return total


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Kruskal's
    edges = [(1, 0, 1), (4, 0, 2), (2, 1, 2), (5, 1, 3), (3, 2, 3)]
    mst, cost = kruskal(4, edges)
    assert cost == 6
    assert len(mst) == 3
    print(colored("✓ kruskal", "green"))

    # Prim's
    g = {
        0: [(1, 1), (2, 4)],
        1: [(0, 1), (2, 2), (3, 5)],
        2: [(0, 4), (1, 2), (3, 3)],
        3: [(1, 5), (2, 3)],
    }
    mst, cost = prim(g)
    assert cost == 6
    assert len(mst) == 3
    print(colored("✓ prim", "green"))

    # Min Cost Connect Points
    assert min_cost_connect_points([[0,0],[2,2],[3,10],[5,2],[7,0]]) == 20
    assert min_cost_connect_points([[3,12],[-2,5],[-4,1]]) == 18
    assert min_cost_connect_points([[0,0]]) == 0
    print(colored("✓ min_cost_connect_points", "green"))

    # Optimize Water Distribution
    assert min_cost_to_supply_water(3, [1, 2, 2], [[1, 2, 1], [2, 3, 1]]) == 3
    assert min_cost_to_supply_water(2, [1, 1], [[1, 2, 2]]) == 2
    print(colored("✓ min_cost_to_supply_water", "green"))

    print(colored("\nAll tests passed.", "cyan"))
