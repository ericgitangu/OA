"""
Topological Sort — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Topological Sort (Intermediate)

Key insight from dsa.md:
  - Topological sort only works on Directed Acyclic Graphs (DAGs).
  - Two approaches:
      1. Kahn's Algorithm (BFS): process nodes with in-degree 0 first.
         Naturally detects cycles (not all nodes get processed).
      2. DFS post-order: push to stack after visiting all descendants.
  - Both are O(V + E).

Patterns covered:
  1. Kahn's Algorithm (BFS)       — core implementation
  2. Course Schedule              — LeetCode 207 (cycle detection)
  3. Course Schedule II           — LeetCode 210 (return order)
  4. Alien Dictionary             — LeetCode 269 (build graph from constraints)
"""

from collections import deque

from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Kahn's Algorithm — Core Topological Sort
# ---------------------------------------------------------------------------
def topological_sort_kahn(graph: dict[int, list[int]]) -> list[int]:
    """
    Topological sort using Kahn's BFS algorithm.

    Approach:
      1. Compute in-degree for every node.
      2. Enqueue all nodes with in-degree 0 (no prerequisites).
      3. Process queue: for each node, reduce neighbours' in-degrees;
         enqueue any that reach 0.
      4. If result length < number of nodes → cycle detected.

    T: O(V + E)
    S: O(V + E)

    Real-world analogy: a build system (like Make) that determines the
    order to compile files based on their import dependencies.

    Args:
        graph: adjacency list {node: [neighbours]}

    Returns:
        nodes in topological order

    Raises:
        ValueError if graph contains a cycle

    Example:
        >>> topological_sort_kahn({0:[1,2], 1:[3], 2:[3], 3:[]})
        [0, 1, 2, 3]  # or [0, 2, 1, 3] — both valid
    """
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque(u for u in graph if in_degree[u] == 0)
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(order) != len(graph):
        raise ValueError("Graph contains a cycle — topological sort impossible")
    return order


# ---------------------------------------------------------------------------
# 2. Course Schedule (Can Finish?)
# ---------------------------------------------------------------------------
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    LeetCode 207 — Course Schedule
    Determine if it's possible to finish all courses given prerequisites.
    Equivalent to: does the prerequisite graph contain a cycle?

    Approach: Kahn's algorithm. If we can process all courses (topological
    order has length == num_courses), no cycle exists.

    T: O(V + E)  — V = num_courses, E = len(prerequisites)
    S: O(V + E)

    Real-world analogy: checking whether a university curriculum has
    circular dependencies (e.g. "you need A to take B, and B to take A").

    Args:
        num_courses:   total number of courses (0..num_courses-1)
        prerequisites: list of [course, prereq] pairs

    Returns:
        True if all courses can be completed

    Example:
        >>> can_finish(2, [[1,0]])
        True
        >>> can_finish(2, [[1,0],[0,1]])
        False
    """
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    finished = 0

    while queue:
        node = queue.popleft()
        finished += 1
        for neighbour in graph[node]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    return finished == num_courses


# ---------------------------------------------------------------------------
# 3. Course Schedule II (Return Order)
# ---------------------------------------------------------------------------
def find_order(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    """
    LeetCode 210 — Course Schedule II
    Return a valid order to take all courses, or [] if impossible.

    Approach: Same as can_finish but collect the processing order.

    T: O(V + E)
    S: O(V + E)

    Real-world analogy: generating a valid task execution plan for a
    CI/CD pipeline where some jobs must run before others.

    Args:
        num_courses:   total number of courses
        prerequisites: list of [course, prereq] pairs

    Returns:
        valid course order, or [] if a cycle exists

    Example:
        >>> find_order(4, [[1,0],[2,0],[3,1],[3,2]])
        [0, 1, 2, 3]  # or [0, 2, 1, 3]
        >>> find_order(2, [[1,0],[0,1]])
        []
    """
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1

    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbour in graph[node]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    return order if len(order) == num_courses else []


# ---------------------------------------------------------------------------
# 4. Alien Dictionary
# ---------------------------------------------------------------------------
def alien_order(words: list[str]) -> str:
    """
    LeetCode 269 — Alien Dictionary
    Given a sorted list of words in an alien language, determine the
    character ordering of that language.

    Approach:
      1. Every character is a node; initialise all with in-degree 0.
      2. Compare adjacent words to extract ordering constraints:
         the first differing character gives an edge (earlier → later).
         If word A is a prefix of word B but longer, the input is invalid.
      3. Run Kahn's topological sort on the character graph.

    T: O(C)  — C = total characters across all words
    S: O(1)  — at most 26 characters (fixed alphabet)

    Real-world analogy: reverse-engineering the sort order of a foreign
    language dictionary from a sample of sorted entries.

    Args:
        words: list of words sorted in alien lexicographic order

    Returns:
        string of characters in alien order, or "" if invalid

    Example:
        >>> alien_order(["wrt","wrf","er","ett","rftt"])
        'wertf'
        >>> alien_order(["z","x"])
        'zx'
        >>> alien_order(["z","x","z"])
        ''
    """
    # Initialise all characters with empty adjacency lists
    adj: dict[str, set[str]] = {ch: set() for word in words for ch in word}
    in_degree: dict[str, int] = {ch: 0 for ch in adj}

    # Extract ordering constraints from adjacent word pairs
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        min_len = min(len(w1), len(w2))
        # Invalid: longer word is a prefix of shorter word
        if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
            return ""
        for j in range(min_len):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break  # only the first differing char gives an ordering

    # Kahn's topological sort on character graph
    queue = deque(ch for ch in in_degree if in_degree[ch] == 0)
    result = []

    while queue:
        ch = queue.popleft()
        result.append(ch)
        for neighbour in adj[ch]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    return "".join(result) if len(result) == len(in_degree) else ""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Kahn's core
    g = {0: [1, 2], 1: [3], 2: [3], 3: []}
    order = topological_sort_kahn(g)
    # Validate: for every edge u→v, u appears before v
    pos = {node: i for i, node in enumerate(order)}
    assert all(pos[u] < pos[v] for u in g for v in g[u])
    print(colored("✓ topological_sort_kahn", "green"))

    # Cycle detection
    try:
        topological_sort_kahn({0: [1], 1: [0]})
        assert False, "Should have raised"
    except ValueError:
        pass
    print(colored("✓ topological_sort_kahn cycle detection", "green"))

    # Can Finish
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(2, [[1, 0], [0, 1]]) is False
    assert can_finish(5, [[1,4],[2,4],[3,1],[3,2]]) is True
    print(colored("✓ can_finish", "green"))

    # Find Order
    order = find_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]])
    assert order[0] == 0 and order[-1] == 3
    assert find_order(2, [[1, 0], [0, 1]]) == []
    print(colored("✓ find_order", "green"))

    # Alien Dictionary
    assert alien_order(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert alien_order(["z", "x"]) == "zx"
    assert alien_order(["z", "x", "z"]) == ""
    assert alien_order(["abc", "ab"]) == ""  # invalid prefix case
    print(colored("✓ alien_order", "green"))

    print(colored("\nAll tests passed.", "cyan"))
