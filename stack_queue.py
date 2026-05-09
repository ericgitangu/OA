"""
Stack & Queue — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Stack (Basic) and § Queue (Basic)

Key insight from dsa.md:
  - Stack (LIFO): O(1) push/pop — ideal for "most recent" tracking,
    matching brackets, and monotonic problems.
  - Queue (FIFO): O(1) enqueue/dequeue via collections.deque — ideal
    for BFS, sliding windows, and task scheduling.

Patterns covered:
  1. Valid Parentheses        — classic stack matching
  2. Min Stack                — stack augmented with running minimum
  3. Daily Temperatures       — monotonic decreasing stack
  4. Sliding Window Maximum   — monotonic deque (hardest pattern here)
  5. Number of Islands (BFS)  — queue-driven flood fill
"""

from collections import deque
from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Valid Parentheses
# ---------------------------------------------------------------------------
def is_valid(s: str) -> bool:
    """
    LeetCode 20 — Valid Parentheses
    Determine if a string of brackets is correctly matched and nested.

    Approach: Push opening brackets onto a stack. When a closing bracket
    is seen, the top of the stack must be its matching opener.

    T: O(n)  — single pass
    S: O(n)  — stack holds at most n/2 openers

    Real-world analogy: syntax validation in a compiler/linter checking
    that every opened block, tag, or expression is properly closed.

    Args:
        s: string containing only '(', ')', '{', '}', '[', ']'

    Returns:
        True if brackets are valid, False otherwise

    Example:
        >>> is_valid("()[]{}")
        True
        >>> is_valid("(]")
        False
        >>> is_valid("{[]}")
        True
    """
    stack = []
    match = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in match:
            if not stack or stack[-1] != match[ch]:
                return False
            stack.pop()
        else:
            stack.append(ch)
    return not stack  # valid only if nothing left unmatched


# ---------------------------------------------------------------------------
# 2. Min Stack
# ---------------------------------------------------------------------------
class MinStack:
    """
    LeetCode 155 — Min Stack
    Stack that supports push, pop, top, and getMin in O(1).

    Approach: Maintain a parallel 'min_stack' that tracks the current
    minimum at every level. When we push x, we push min(x, current_min)
    onto min_stack. When we pop, we pop both stacks together.

    T: O(1) for all operations
    S: O(n) — two stacks of equal size

    Real-world analogy: a trading system that needs to instantly report
    the lowest price seen since any given point in time.

    Example:
        >>> ms = MinStack()
        >>> ms.push(-2); ms.push(0); ms.push(-3)
        >>> ms.get_min()
        -3
        >>> ms.pop()
        >>> ms.top()
        0
        >>> ms.get_min()
        -2
    """

    def __init__(self):
        self.stack: list[int] = []
        self.min_stack: list[int] = []  # min_stack[i] = min of stack[0..i]

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Track the minimum seen so far at this depth
        current_min = val if not self.min_stack else min(val, self.min_stack[-1])
        self.min_stack.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]


# ---------------------------------------------------------------------------
# 3. Daily Temperatures
# ---------------------------------------------------------------------------
def daily_temperatures(temps: list[int]) -> list[int]:
    """
    LeetCode 739 — Daily Temperatures
    For each day, find how many days until a warmer temperature.
    Return 0 if no warmer day exists.

    Approach: Monotonic decreasing stack of indices. We maintain a stack
    where temperatures are always decreasing from bottom to top. When we
    see a temperature warmer than the stack top, we've found the answer
    for that day.

    T: O(n)  — each index pushed and popped at most once
    S: O(n)  — stack

    Real-world analogy: for each item in a price history, find how many
    days until the price exceeds the current value (next greater element).

    Args:
        temps: list of daily temperatures

    Returns:
        list where result[i] = days until warmer temp (0 if none)

    Example:
        >>> daily_temperatures([73,74,75,71,69,72,76,73])
        [1, 1, 4, 2, 1, 1, 0, 0]
    """
    result = [0] * len(temps)
    stack: list[int] = []  # stores indices, temps are decreasing

    for i, temp in enumerate(temps):
        # Pop all days that are cooler than today — today is their answer
        while stack and temps[stack[-1]] < temp:
            j = stack.pop()
            result[j] = i - j
        stack.append(i)

    return result


# ---------------------------------------------------------------------------
# 4. Sliding Window Maximum
# ---------------------------------------------------------------------------
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    LeetCode 239 — Sliding Window Maximum
    Return the maximum value in each sliding window of size k.

    Approach: Monotonic decreasing deque of indices. The front always
    holds the index of the current window's maximum. We:
      - Remove indices that have fallen outside the window (front).
      - Remove indices from the back whose values are <= current value
        (they can never be the max while current element is in the window).

    T: O(n)  — each element added and removed from deque at most once
    S: O(k)  — deque holds at most k indices

    Real-world analogy: real-time monitoring dashboard showing the peak
    metric value over a rolling time window.

    Args:
        nums: list of integers
        k:    window size

    Returns:
        list of maximums for each window position

    Example:
        >>> max_sliding_window([1,3,-1,-3,5,3,6,7], 3)
        [3, 3, 5, 5, 6, 7]
    """
    dq: deque[int] = deque()  # stores indices; values are decreasing
    result = []

    for i, val in enumerate(nums):
        # Remove indices outside the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # Maintain decreasing order: remove smaller values from the back
        while dq and nums[dq[-1]] < val:
            dq.pop()

        dq.append(i)

        # Window is fully formed starting at index k-1
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


# ---------------------------------------------------------------------------
# 5. Number of Islands (BFS)
# ---------------------------------------------------------------------------
def num_islands(grid: list[list[str]]) -> int:
    """
    LeetCode 200 — Number of Islands
    Count distinct islands (connected groups of '1's) in a 2D grid.

    Approach: BFS flood fill. For each unvisited '1', start a BFS that
    marks all connected land cells as visited ('0'). Each BFS call = 1 island.

    T: O(m * n)  — every cell visited at most once
    S: O(min(m, n))  — BFS queue size bounded by the shorter dimension

    Real-world analogy: counting connected components in a network topology
    map, or labeling distinct regions in a satellite image.

    Args:
        grid: 2D list of '1' (land) and '0' (water) — modified in place

    Returns:
        number of islands

    Example:
        >>> num_islands([
        ...   ["1","1","0","0","0"],
        ...   ["1","1","0","0","0"],
        ...   ["0","0","1","0","0"],
        ...   ["0","0","0","1","1"]
        ... ])
        3
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def bfs(r: int, c: int) -> None:
        queue = deque([(r, c)])
        grid[r][c] = '0'  # mark visited immediately on enqueue
        while queue:
            row, col = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
                    grid[nr][nc] = '0'
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                bfs(r, c)
                count += 1

    return count


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Valid Parentheses
    assert is_valid("()[]{}") is True
    assert is_valid("(]") is False
    assert is_valid("{[]}") is True
    assert is_valid("([)]") is False
    print(colored("✓ is_valid", "green"))

    # Min Stack
    ms = MinStack()
    ms.push(-2); ms.push(0); ms.push(-3)
    assert ms.get_min() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.get_min() == -2
    print(colored("✓ MinStack", "green"))

    # Daily Temperatures
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 40, 50, 60]) == [1, 1, 1, 0]
    print(colored("✓ daily_temperatures", "green"))

    # Sliding Window Maximum
    assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert max_sliding_window([1], 1) == [1]
    print(colored("✓ max_sliding_window", "green"))

    # Number of Islands
    grid1 = [["1","1","0","0","0"],
             ["1","1","0","0","0"],
             ["0","0","1","0","0"],
             ["0","0","0","1","1"]]
    assert num_islands(grid1) == 3
    grid2 = [["1","1","1"],["0","1","0"],["1","1","1"]]
    assert num_islands(grid2) == 1
    print(colored("✓ num_islands", "green"))

    print(colored("\nAll tests passed.", "cyan"))
