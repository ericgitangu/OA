"""
Shortest Path Algorithms — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Dijkstra's Algorithm (Advanced),
           § Bellman-Ford (Advanced), § Floyd-Warshall (Advanced)

Key insight from dsa.md:
  - Dijkstra: O((V+E) log V) with a min-heap. Requires non-negative weights.
    Best for single-source shortest path on sparse graphs.
  - Bellman-Ford: O(VE). Handles negative weights; detects negative cycles.
    Use when Dijkstra is not applicable.
  - Floyd-Warshall: O(V³). All-pairs shortest paths. Simple DP on a matrix.
    Only practical for small, dense graphs (V ≤ ~500).

Patterns covered:
  1. Dijkstra's Algorithm         — single-source, non-negative weights
  2. Network Delay Time           — LeetCode 743 (Dijkstra application)
  3. Bellman-Ford                 — single-source with negative weights
  4. Floyd-Warshall               — all-pairs shortest paths
  5. Cheapest Flights Within K Stops — LeetCode 787 (Bellman-Ford variant)
"""

import heapq
from collections import defaultdict

from termcolor import colored

INF = float('inf')


# ---------------------------------------------------------------------------
# 1. Dijkstra's Algorithm
# ---------------------------------------------------------------------------
def dijkstra(graph: dict[int, list[tuple[int, int]]], src: int) -> dict[int, float]:
    """
    Single-source shortest paths using Dijkstra's algorithm.

    Reference: dsa.md § Dijkstra's Algorithm (Advanced)

    Approach: Min-heap (priority queue) of (distance, node). Always expand
    the closest unvisited node. When a node is first popped from the heap,
    its distance is finalised (greedy correctness relies on non-negative weights).

    T: O((V + E) log V)  — each node/edge processed once; heap ops O(log V)
    S: O(V + E)          — graph + dist dict + heap

    Real-world analogy: GPS navigation finding the fastest route — always
    extending the currently shortest known path.

    Args:
        graph: adjacency list {node: [(neighbour, weight), ...]}
        src:   source node

    Returns:
        dict mapping each node to its shortest distance from src
        (INF if unreachable)

    Example:
        >>> g = {0:[(1,4),(2,1)], 1:[(3,1)], 2:[(1,2),(3,5)], 3:[]}
        >>> dijkstra(g, 0)
        {0: 0, 1: 3, 2: 1, 3: 4}
    """
    dist: dict[int, float] = {node: INF for node in graph}
    dist[src] = 0
    heap = [(0, src)]  # (distance, node)

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry — already found a shorter path
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))

    return dist


# ---------------------------------------------------------------------------
# 2. Network Delay Time (Dijkstra application)
# ---------------------------------------------------------------------------
def network_delay_time(times: list[list[int]], n: int, k: int) -> int:
    """
    LeetCode 743 — Network Delay Time
    A signal is sent from node k. Find the time for ALL nodes to receive it.
    Return -1 if some node is unreachable.

    Approach: Dijkstra from k. The answer is the maximum shortest-path
    distance across all nodes (the last node to receive the signal).

    T: O((V + E) log V)
    S: O(V + E)

    Real-world analogy: broadcasting a message across a network and
    measuring how long until every server has received it.

    Args:
        times: list of [u, v, w] directed edges (1-indexed nodes)
        n:     number of nodes
        k:     source node

    Returns:
        time for all nodes to receive signal, or -1 if impossible

    Example:
        >>> network_delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2)
        2
    """
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    # Ensure all nodes 1..n are in the graph (even if no outgoing edges)
    for i in range(1, n + 1):
        if i not in graph:
            graph[i] = []

    dist = dijkstra(graph, k)
    max_dist = max(dist.values())
    return max_dist if max_dist < INF else -1


# ---------------------------------------------------------------------------
# 3. Bellman-Ford
# ---------------------------------------------------------------------------
def bellman_ford(
    vertices: list, edges: list[tuple], src
) -> dict | None:
    """
    Single-source shortest paths using Bellman-Ford.

    Reference: dsa.md § Bellman-Ford (Advanced)

    Approach: Relax ALL edges V-1 times. After V-1 iterations, all shortest
    paths (without negative cycles) are found. A Vth relaxation that still
    improves a distance indicates a negative cycle.

    T: O(V * E)  — V-1 relaxation rounds, each processing E edges
    S: O(V)      — distance array

    Real-world analogy: currency arbitrage detection — negative cycles in
    a forex graph represent profitable arbitrage loops.

    Args:
        vertices: list of all vertex identifiers
        edges:    list of (u, v, weight) directed edges
        src:      source vertex

    Returns:
        dict of shortest distances, or None if a negative cycle exists

    Example:
        >>> verts = [0,1,2,3]
        >>> edges = [(0,1,1),(0,2,4),(1,2,2),(1,3,5),(2,3,1)]
        >>> bellman_ford(verts, edges, 0)
        {0: 0, 1: 1, 2: 3, 3: 4}
    """
    dist = {v: INF for v in vertices}
    dist[src] = 0

    # Relax all edges V-1 times
    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break  # early exit: no changes means we're done

    # Check for negative cycles (Vth relaxation)
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            return None  # negative cycle detected

    return dist


# ---------------------------------------------------------------------------
# 4. Floyd-Warshall
# ---------------------------------------------------------------------------
def floyd_warshall(matrix: list[list[float]]) -> list[list[float]]:
    """
    All-pairs shortest paths using Floyd-Warshall.

    Reference: dsa.md § Floyd-Warshall (Advanced)

    Approach: DP. dist[i][j] = shortest path from i to j considering only
    vertices 0..k as intermediates. For each k, update all (i,j) pairs:
      dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    T: O(V³)  — three nested loops over V vertices
    S: O(V²)  — distance matrix (modified in place)

    Real-world analogy: computing the shortest travel time between every
    pair of cities in a road network — useful for pre-computing a lookup
    table for a routing service.

    Args:
        matrix: V×V adjacency matrix where matrix[i][j] = edge weight
                (INF if no direct edge, 0 on diagonal)

    Returns:
        V×V matrix of all-pairs shortest distances

    Raises:
        ValueError if a negative cycle is detected

    Example:
        >>> INF = float('inf')
        >>> m = [[0,3,INF,5],[2,0,INF,4],[INF,1,0,INF],[INF,INF,2,0]]
        >>> floyd_warshall(m)[0]
        [0, 3, 7, 5]
    """
    n = len(matrix)
    dist = [row[:] for row in matrix]  # deep copy

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] != INF and dist[k][j] != INF:
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    # Negative cycle: any node has a negative path to itself
    for i in range(n):
        if dist[i][i] < 0:
            raise ValueError("Graph contains a negative cycle")

    return dist


# ---------------------------------------------------------------------------
# 5. Cheapest Flights Within K Stops (Bellman-Ford variant)
# ---------------------------------------------------------------------------
def find_cheapest_price(
    n: int, flights: list[list[int]], src: int, dst: int, k: int
) -> int:
    """
    LeetCode 787 — Cheapest Flights Within K Stops
    Find the cheapest price from src to dst with at most k stops.

    Approach: Bellman-Ford limited to k+1 relaxation rounds (k stops =
    k+1 edges). Use a copy of distances each round to prevent using more
    than one new edge per round.

    T: O(k * E)  — k+1 rounds, each processing E edges
    S: O(V)      — distance array

    Real-world analogy: finding the cheapest flight itinerary with a
    maximum number of layovers — a common travel booking constraint.

    Args:
        n:       number of cities (0..n-1)
        flights: list of [from, to, price]
        src:     source city
        dst:     destination city
        k:       maximum number of stops (not counting src)

    Returns:
        minimum cost, or -1 if unreachable within k stops

    Example:
        >>> find_cheapest_price(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1)
        700
    """
    dist = [INF] * n
    dist[src] = 0

    for _ in range(k + 1):  # at most k+1 edges = k stops
        temp = dist[:]       # snapshot: don't use edges added this round
        for u, v, price in flights:
            if dist[u] != INF and dist[u] + price < temp[v]:
                temp[v] = dist[u] + price
        dist = temp

    return dist[dst] if dist[dst] != INF else -1


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Dijkstra
    g = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)], 3: []}
    d = dijkstra(g, 0)
    assert d == {0: 0, 1: 3, 2: 1, 3: 4}
    print(colored("✓ dijkstra", "green"))

    # Network Delay Time
    assert network_delay_time([[2,1,1],[2,3,1],[3,4,1]], 4, 2) == 2
    assert network_delay_time([[1,2,1]], 2, 2) == -1  # node 1 unreachable from 2
    print(colored("✓ network_delay_time", "green"))

    # Bellman-Ford
    verts = [0, 1, 2, 3]
    edges = [(0,1,1),(0,2,4),(1,2,2),(1,3,5),(2,3,1)]
    result = bellman_ford(verts, edges, 0)
    assert result == {0: 0, 1: 1, 2: 3, 3: 4}
    # Negative cycle detection
    neg_edges = [(0,1,1),(1,2,-1),(2,0,-1)]
    assert bellman_ford([0,1,2], neg_edges, 0) is None
    print(colored("✓ bellman_ford", "green"))

    # Floyd-Warshall
    m = [[0, 3, INF, 5],
         [2, 0, INF, 4],
         [INF, 1, 0, INF],
         [INF, INF, 2, 0]]
    fw = floyd_warshall(m)
    assert fw[0] == [0, 3, 7, 5]
    assert fw[1] == [2, 0, 6, 4]
    print(colored("✓ floyd_warshall", "green"))

    # Cheapest Flights Within K Stops
    flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
    assert find_cheapest_price(4, flights, 0, 3, 1) == 700
    assert find_cheapest_price(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1) == 200
    print(colored("✓ find_cheapest_price", "green"))

    print(colored("\nAll tests passed.", "cyan"))
