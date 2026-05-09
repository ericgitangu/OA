"""
Union-Find (Disjoint Set Union) — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Disjoint Set (Union-Find) (Advanced)

Key insight from dsa.md:
  - Union-Find tracks which elements belong to the same connected component.
  - Two optimisations make it nearly O(1) amortised per operation:
      1. Path Compression: during find(), point every node directly to root.
      2. Union by Rank: attach the shorter tree under the taller one.
  - The combined complexity is O(α(n)) — inverse Ackermann, effectively constant.

Patterns covered:
  1. UnionFind class              — core data structure with both optimisations
  2. Number of Connected Components — LeetCode 323
  3. Redundant Connection           — LeetCode 684 (cycle detection)
  4. Accounts Merge                 — LeetCode 721 (grouping by shared element)
"""
from termcolor import colored


class UnionFind:
    """
    Disjoint Set Union with path compression and union by rank.

    Reference: dsa.md § Disjoint Set (Union-Find) (Advanced)

    T: O(α(n)) amortised per find/union — effectively O(1)
    S: O(n)

    Real-world analogy: tracking which users belong to the same social
    network cluster as friend connections are added one by one.

    Attributes:
        parent: parent[i] = representative of i's set (itself if root)
        rank:   upper bound on tree height, used to keep trees shallow
        count:  number of disjoint sets currently
    """

    def __init__(self, n: int):
        """Initialise n singleton sets {0}, {1}, ..., {n-1}."""
        self.parent = list(range(n))  # each node is its own root
        self.rank = [0] * n           # all trees start at height 0
        self.count = n                # n separate components

    def find(self, x: int) -> int:
        """Return the root representative of x's set. Path-compresses on the way."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merge the sets containing x and y.

        Returns:
            True if x and y were in different sets (a merge happened),
            False if they were already connected.
        """
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # already in the same set
        # Union by rank: attach smaller tree under larger
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.count -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        """Return True if x and y are in the same set."""
        return self.find(x) == self.find(y)


# ---------------------------------------------------------------------------
# 2. Number of Connected Components in an Undirected Graph
# ---------------------------------------------------------------------------
def count_components(n: int, edges: list[list[int]]) -> int:
    """
    LeetCode 323 — Number of Connected Components in an Undirected Graph
    Given n nodes (0..n-1) and a list of undirected edges, count the
    number of connected components.

    Approach: Start with n components. Each successful union reduces the
    count by 1. Final count = number of components.

    T: O(n + E * α(n))  — initialise n nodes, process E edges
    S: O(n)

    Real-world analogy: counting isolated sub-networks in a data centre
    after some cables are connected.

    Args:
        n:     number of nodes
        edges: list of [u, v] undirected edges

    Returns:
        number of connected components

    Example:
        >>> count_components(5, [[0,1],[1,2],[3,4]])
        2
        >>> count_components(5, [[0,1],[1,2],[2,3],[3,4]])
        1
    """
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count


# ---------------------------------------------------------------------------
# 3. Redundant Connection (Cycle Detection)
# ---------------------------------------------------------------------------
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """
    LeetCode 684 — Redundant Connection
    A tree of n nodes has n-1 edges. One extra edge was added, creating a
    cycle. Find and return that edge.

    Approach: Process edges in order. The first edge whose two endpoints
    are already connected (same component) is the redundant one — adding
    it would create a cycle.

    T: O(E * α(n))
    S: O(n)

    Real-world analogy: auditing a network topology to find the one
    redundant cable that creates a loop in what should be a spanning tree.

    Args:
        edges: list of [u, v] edges (1-indexed nodes)

    Returns:
        the redundant edge [u, v]

    Example:
        >>> find_redundant_connection([[1,2],[1,3],[2,3]])
        [2, 3]
        >>> find_redundant_connection([[1,2],[2,3],[3,4],[1,4],[1,5]])
        [1, 4]
    """
    n = len(edges)
    uf = UnionFind(n + 1)  # nodes are 1-indexed
    for u, v in edges:
        if not uf.union(u, v):  # already connected → this edge is redundant
            return [u, v]
    return []  # guaranteed to find one


# ---------------------------------------------------------------------------
# 4. Accounts Merge
# ---------------------------------------------------------------------------
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    """
    LeetCode 721 — Accounts Merge
    Each account is [name, email1, email2, ...]. Merge accounts that share
    at least one email. Return merged accounts with sorted emails.

    Approach:
      1. Assign each unique email an integer ID.
      2. Union all emails within the same account.
      3. Group emails by their root representative.
      4. Attach the account name and sort emails.

    T: O(N * K * α(N))  — N accounts, K emails per account
    S: O(N * K)

    Real-world analogy: deduplicating customer records across multiple
    databases where the same person may appear under different accounts
    but shares at least one email address.

    Args:
        accounts: list of [name, email, email, ...]

    Returns:
        merged list of [name, sorted_email, ...] accounts

    Example:
        >>> accounts_merge([
        ...   ["John","johnsmith@mail.com","john_newyork@mail.com"],
        ...   ["John","johnsmith@mail.com","john00@mail.com"],
        ...   ["Mary","mary@mail.com"],
        ...   ["John","johnnybravo@mail.com"]
        ... ])
        [['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'],
         ['Mary', 'mary@mail.com'],
         ['John', 'johnnybravo@mail.com']]
    """
    from collections import defaultdict

    email_to_id: dict[str, int] = {}
    email_to_name: dict[str, str] = {}

    # Assign IDs and record owner name
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_id:
                email_to_id[email] = len(email_to_id)
            email_to_name[email] = name

    uf = UnionFind(len(email_to_id))

    # Union all emails within the same account
    for account in accounts:
        first_id = email_to_id[account[1]]
        for email in account[2:]:
            uf.union(first_id, email_to_id[email])

    # Group emails by root representative
    root_to_emails: dict[int, list[str]] = defaultdict(list)
    for email, eid in email_to_id.items():
        root_to_emails[uf.find(eid)].append(email)

    return [
        [email_to_name[emails[0]]] + sorted(emails)
        for emails in root_to_emails.values()
    ]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # UnionFind core
    uf = UnionFind(5)
    assert uf.count == 5
    uf.union(0, 1); uf.union(1, 2)
    assert uf.connected(0, 2) is True
    assert uf.connected(0, 3) is False
    assert uf.count == 3
    uf.union(3, 4)
    assert uf.count == 2
    print(colored("✓ UnionFind core", "green"))

    # Count Components
    assert count_components(5, [[0, 1], [1, 2], [3, 4]]) == 2
    assert count_components(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1
    assert count_components(4, []) == 4
    print(colored("✓ count_components", "green"))

    # Redundant Connection
    assert find_redundant_connection([[1, 2], [1, 3], [2, 3]]) == [2, 3]
    assert find_redundant_connection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4]
    print(colored("✓ find_redundant_connection", "green"))

    # Accounts Merge
    accs = [
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ]
    merged = accounts_merge(accs)
    # Find John's merged account (the one with 3 emails)
    big_john = next(a for a in merged if len(a) == 4)
    assert big_john[0] == "John"
    assert big_john[1:] == sorted(["johnsmith@mail.com",
                                    "john_newyork@mail.com",
                                    "john00@mail.com"])
    assert any(a == ["Mary", "mary@mail.com"] for a in merged)
    print(colored("✓ accounts_merge", "green"))

    print(colored("\nAll tests passed.", "cyan"))
