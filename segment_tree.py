"""
Segment Tree & Fenwick Tree (BIT) — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Segment Tree (Advanced), § Fenwick Tree (BIT) (Advanced)

Key insight from dsa.md:
  - Segment Tree: O(log n) range queries AND point/range updates.
    Stored as an array where node i has children at 2i and 2i+1.
    Needs 4n space. More flexible than Fenwick (supports min/max/sum).
  - Fenwick Tree (BIT): O(log n) prefix sum queries and point updates.
    Simpler code, less space, but only supports prefix-sum-style queries.

Patterns covered:
  1. SegmentTree class          — range sum query + point update
  2. Range Sum Query — Mutable  — LeetCode 307 (classic segment tree use)
  3. FenwickTree class          — prefix sum + point update
  4. Count of Smaller Numbers   — LeetCode 315 (BIT + coordinate compression)
"""
from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Segment Tree
# ---------------------------------------------------------------------------
class SegmentTree:
    """
    Array-based segment tree for range sum queries and point updates.

    Reference: dsa.md § Segment Tree (Advanced)

    The tree is stored in a flat array where:
      - Node 1 is the root (covers the full array)
      - Node i's left child is at 2*i, right child at 2*i+1
      - Leaf nodes store individual array values
      - Internal nodes store the sum of their range

    T: O(n) build, O(log n) query and update
    S: O(4n) — 4x to safely cover all tree levels

    Real-world analogy: a financial reporting system that can instantly
    answer "total sales between day L and day R" and update individual
    day figures, without recomputing the entire period each time.
    """

    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        if self.n:
            self._build(nums, 0, self.n - 1, 1)

    def _build(self, nums: list[int], lo: int, hi: int, node: int) -> None:
        """Recursively build the tree bottom-up."""
        if lo == hi:
            self.tree[node] = nums[lo]
            return
        mid = (lo + hi) // 2
        self._build(nums, lo, mid, 2 * node)
        self._build(nums, mid + 1, hi, 2 * node + 1)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx: int, val: int) -> None:
        """
        Set nums[idx] = val and update all ancestor nodes. T: O(log n)

        Args:
            idx: 0-indexed position to update
            val: new value
        """
        self._update(0, self.n - 1, 1, idx, val)

    def _update(self, lo: int, hi: int, node: int, idx: int, val: int) -> None:
        if lo == hi:
            self.tree[node] = val
            return
        mid = (lo + hi) // 2
        if idx <= mid:
            self._update(lo, mid, 2 * node, idx, val)
        else:
            self._update(mid + 1, hi, 2 * node + 1, idx, val)
        self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, l: int, r: int) -> int:
        """
        Return sum of nums[l..r] inclusive. T: O(log n)

        Args:
            l: left bound (0-indexed, inclusive)
            r: right bound (0-indexed, inclusive)
        """
        return self._query(0, self.n - 1, 1, l, r)

    def _query(self, lo: int, hi: int, node: int, l: int, r: int) -> int:
        if r < lo or hi < l:
            return 0  # completely outside query range
        if l <= lo and hi <= r:
            return self.tree[node]  # completely inside query range
        mid = (lo + hi) // 2
        return (self._query(lo, mid, 2 * node, l, r) +
                self._query(mid + 1, hi, 2 * node + 1, l, r))


# ---------------------------------------------------------------------------
# 2. Range Sum Query — Mutable (LeetCode 307)
# ---------------------------------------------------------------------------
class NumArray:
    """
    LeetCode 307 — Range Sum Query - Mutable
    Support both point updates and range sum queries efficiently.

    Approach: Wrap SegmentTree. Each update/query is O(log n).

    T: O(n) init, O(log n) update and sumRange
    S: O(n)

    Real-world analogy: a live leaderboard where individual scores change
    frequently and you need instant range-sum queries (e.g. "total score
    of players ranked 3rd through 7th").

    Example:
        >>> na = NumArray([1, 3, 5])
        >>> na.sum_range(0, 2)
        9
        >>> na.update(1, 2)
        >>> na.sum_range(0, 2)
        8
    """

    def __init__(self, nums: list[int]):
        self.st = SegmentTree(nums)

    def update(self, index: int, val: int) -> None:
        """Set nums[index] = val. T: O(log n)"""
        self.st.update(index, val)

    def sum_range(self, left: int, right: int) -> int:
        """Return sum of nums[left..right]. T: O(log n)"""
        return self.st.query(left, right)


# ---------------------------------------------------------------------------
# 3. Fenwick Tree (Binary Indexed Tree)
# ---------------------------------------------------------------------------
class FenwickTree:
    """
    Binary Indexed Tree (BIT) for prefix sum queries and point updates.

    Reference: dsa.md § Fenwick Tree (BIT) (Advanced)

    Uses the lowest set bit trick (i & -i) to navigate the tree:
      - update: add delta to index i and all ancestors
      - prefix_sum: sum from index 1 to i

    T: O(n) build, O(log n) update and prefix_sum
    S: O(n)

    Real-world analogy: a vote-counting system that can instantly report
    the cumulative vote count up to any candidate number, and update
    individual counts as new votes arrive.

    Note: 1-indexed internally. External callers use 0-indexed via helpers.
    """

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)  # 1-indexed

    def update(self, i: int, delta: int) -> None:
        """Add delta to position i (1-indexed). T: O(log n)"""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # move to next responsible node

    def prefix_sum(self, i: int) -> int:
        """Return sum of positions 1..i (1-indexed). T: O(log n)"""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)  # move to parent
        return total

    def range_sum(self, l: int, r: int) -> int:
        """Return sum of positions l..r (1-indexed). T: O(log n)"""
        return self.prefix_sum(r) - self.prefix_sum(l - 1)


# ---------------------------------------------------------------------------
# 4. Count of Smaller Numbers After Self (BIT + coordinate compression)
# ---------------------------------------------------------------------------
def count_smaller(nums: list[int]) -> list[int]:
    """
    LeetCode 315 — Count of Smaller Numbers After Self
    For each element, count how many elements to its right are smaller.

    Approach:
      1. Coordinate compress nums to range [1, len(unique_vals)].
      2. Traverse right-to-left. For each element x (compressed to rank r):
         - Query BIT for prefix_sum(r-1) = count of smaller elements seen so far.
         - Update BIT at position r (record that we've seen x).

    T: O(n log n)  — n BIT operations each O(log n)
    S: O(n)

    Real-world analogy: for each stock price in a time series, count how
    many future prices are lower (useful for drawdown analysis).

    Args:
        nums: list of integers

    Returns:
        list where result[i] = count of nums[j] < nums[i] for all j > i

    Example:
        >>> count_smaller([5, 2, 6, 1])
        [2, 1, 1, 0]
    """
    # Coordinate compression: map values to ranks 1..m
    sorted_unique = sorted(set(nums))
    rank = {v: i + 1 for i, v in enumerate(sorted_unique)}  # 1-indexed

    bit = FenwickTree(len(sorted_unique))
    result = []

    for x in reversed(nums):
        r = rank[x]
        # Count elements already seen (to the right) that are smaller than x
        result.append(bit.prefix_sum(r - 1))
        bit.update(r, 1)  # record that we've seen x

    return result[::-1]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # SegmentTree
    st = SegmentTree([1, 3, 5, 7, 9, 11])
    assert st.query(1, 3) == 15   # 3+5+7
    assert st.query(0, 5) == 36   # sum of all
    st.update(1, 10)              # change index 1 from 3 to 10
    assert st.query(1, 3) == 22   # 10+5+7
    print(colored("✓ SegmentTree", "green"))

    # NumArray (LeetCode 307)
    na = NumArray([1, 3, 5])
    assert na.sum_range(0, 2) == 9
    na.update(1, 2)
    assert na.sum_range(0, 2) == 8
    assert na.sum_range(0, 0) == 1
    print(colored("✓ NumArray (Range Sum Query Mutable)", "green"))

    # FenwickTree
    ft = FenwickTree(6)
    for i, v in enumerate([1, 3, 5, 7, 9, 11], start=1):
        ft.update(i, v)
    assert ft.prefix_sum(3) == 9   # 1+3+5
    assert ft.range_sum(2, 4) == 15  # 3+5+7
    ft.update(2, 7)  # add 7 to position 2 (now 3+7=10)
    assert ft.prefix_sum(3) == 16  # 1+10+5
    print(colored("✓ FenwickTree", "green"))

    # Count Smaller Numbers After Self
    assert count_smaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert count_smaller([2, 0, 1]) == [2, 0, 0]
    assert count_smaller([-1]) == [0]
    print(colored("✓ count_smaller", "green"))

    print(colored("\nAll tests passed.", "cyan"))
