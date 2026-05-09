"""
Sorting Algorithms — Implementations and LeetCode-type problems.

Reference: dsa.md § Merge Sort (Intermediate), § Quick Sort (Intermediate),
           § Bubble Sort (Basic), § Insertion Sort (Basic), § Selection Sort (Basic)

Key insight from dsa.md:
  - Merge Sort: O(n log n) guaranteed, stable, O(n) extra space.
    Best when stability matters or sorting linked lists.
  - Quick Sort: O(n log n) average, O(n²) worst, in-place, not stable.
    Best for in-memory sorting where average case dominates.
  - Bubble/Insertion/Selection: O(n²) — only useful for tiny or nearly-sorted data.

Patterns covered:
  1. Merge Sort                — divide-and-conquer, stable
  2. Quick Sort                — partition-based, in-place
  3. Sort Colors (Dutch Flag)  — 3-way partition, O(n) one-pass
  4. Merge Intervals           — sort + greedy merge
  5. Largest Number            — custom comparator sort
"""
from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Merge Sort
# ---------------------------------------------------------------------------
def merge_sort(arr: list[int]) -> list[int]:
    """
    Classic Merge Sort — stable, O(n log n) guaranteed.

    Approach: Recursively split the array in half, sort each half, then
    merge the two sorted halves using two pointers.

    T: O(n log n)  — log n levels of recursion, O(n) merge work per level
    S: O(n)        — temporary arrays during merge + O(log n) call stack

    Real-world analogy: merging two sorted filing cabinets into one —
    you always pick the smaller of the two front files.

    Args:
        arr: list of integers

    Returns:
        new sorted list (original unchanged)

    Example:
        >>> merge_sort([5, 2, 4, 6, 1, 3])
        [1, 2, 3, 4, 5, 6]
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= preserves stability
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------------------------
# 2. Quick Sort
# ---------------------------------------------------------------------------
def quick_sort(arr: list[int], lo: int = 0, hi: int = -1) -> None:
    """
    Classic Quick Sort — in-place, average O(n log n).

    Approach: Choose a pivot (last element), partition the array so all
    elements < pivot are left of it and all > pivot are right, then
    recursively sort both sides.

    T: O(n log n) average, O(n²) worst (sorted input with bad pivot)
    S: O(log n) average call stack, O(n) worst

    Real-world analogy: sorting a hand of cards by repeatedly picking one
    card as a reference and splitting the rest into "lower" and "higher".

    Args:
        arr: list of integers — sorted IN PLACE
        lo:  start index (default 0)
        hi:  end index inclusive (default len(arr)-1)

    Example:
        >>> a = [3,6,8,10,1,2,1]
        >>> quick_sort(a)
        >>> a
        [1, 1, 2, 3, 6, 8, 10]
    """
    if hi == -1:
        hi = len(arr) - 1
    if lo < hi:
        p = _partition(arr, lo, hi)
        quick_sort(arr, lo, p - 1)
        quick_sort(arr, p + 1, hi)


def _partition(arr: list[int], lo: int, hi: int) -> int:
    """Lomuto partition: pivot = arr[hi]. Returns final pivot index."""
    pivot = arr[hi]
    i = lo - 1  # boundary of elements < pivot
    for j in range(lo, hi):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
    return i + 1


# ---------------------------------------------------------------------------
# 3. Sort Colors (Dutch National Flag)
# ---------------------------------------------------------------------------
def sort_colors(nums: list[int]) -> None:
    """
    LeetCode 75 — Sort Colors
    Sort an array of 0s, 1s, and 2s in-place in a single pass.

    Approach: Dutch National Flag algorithm with three pointers:
      - lo: boundary of 0s (everything left of lo is 0)
      - hi: boundary of 2s (everything right of hi is 2)
      - mid: current element being examined

    T: O(n)  — single pass
    S: O(1)  — in-place

    Real-world analogy: physically sorting coloured balls into three bins
    in one sweep without counting them first.

    Args:
        nums: list containing only 0, 1, 2 — sorted IN PLACE

    Example:
        >>> a = [2,0,2,1,1,0]
        >>> sort_colors(a)
        >>> a
        [0, 0, 1, 1, 2, 2]
    """
    lo, mid, hi = 0, 0, len(nums) - 1
    while mid <= hi:
        if nums[mid] == 0:
            nums[lo], nums[mid] = nums[mid], nums[lo]
            lo += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[hi] = nums[hi], nums[mid]
            hi -= 1  # don't advance mid; swapped element not yet examined


# ---------------------------------------------------------------------------
# 4. Merge Intervals
# ---------------------------------------------------------------------------
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """
    LeetCode 56 — Merge Intervals
    Merge all overlapping intervals and return the result.

    Approach: Sort by start time. Iterate and extend the last merged
    interval if the current one overlaps, otherwise append it.

    T: O(n log n)  — dominated by sort
    S: O(n)        — output list

    Real-world analogy: merging overlapping calendar events into a single
    blocked time slot for a meeting scheduler.

    Args:
        intervals: list of [start, end] pairs

    Returns:
        list of merged non-overlapping intervals

    Example:
        >>> merge_intervals([[1,3],[2,6],[8,10],[15,18]])
        [[1, 6], [8, 10], [15, 18]]
        >>> merge_intervals([[1,4],[4,5]])
        [[1, 5]]
    """
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:          # overlaps with last merged
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged


# ---------------------------------------------------------------------------
# 5. Largest Number
# ---------------------------------------------------------------------------
def largest_number(nums: list[int]) -> str:
    """
    LeetCode 179 — Largest Number
    Arrange integers to form the largest possible number.

    Approach: Custom sort — compare two numbers a, b by checking whether
    str(a)+str(b) > str(b)+str(a). Use functools.cmp_to_key to plug this
    comparator into Python's sort.

    T: O(n log n * k)  — n numbers, each comparison is O(k) string concat
                         where k = average digit count
    S: O(n)            — string conversion

    Real-world analogy: arranging department codes to form the highest
    possible composite identifier for a report.

    Args:
        nums: list of non-negative integers

    Returns:
        string representing the largest number

    Example:
        >>> largest_number([10, 2])
        '210'
        >>> largest_number([3,30,34,5,9])
        '9534330'
    """
    from functools import cmp_to_key

    def compare(a: str, b: str) -> int:
        # Return negative if a+b > b+a (a should come first)
        if a + b > b + a:
            return -1
        elif a + b < b + a:
            return 1
        return 0

    strs = sorted([str(n) for n in nums], key=cmp_to_key(compare))
    result = "".join(strs)
    return "0" if result[0] == "0" else result  # edge case: all zeros


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Merge Sort
    assert merge_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([2, 1]) == [1, 2]
    print(colored("✓ merge_sort", "green"))

    # Quick Sort
    a = [3, 6, 8, 10, 1, 2, 1]
    quick_sort(a)
    assert a == [1, 1, 2, 3, 6, 8, 10]
    b = [1]
    quick_sort(b)
    assert b == [1]
    print(colored("✓ quick_sort", "green"))

    # Sort Colors
    c = [2, 0, 2, 1, 1, 0]
    sort_colors(c)
    assert c == [0, 0, 1, 1, 2, 2]
    d = [2, 0, 1]
    sort_colors(d)
    assert d == [0, 1, 2]
    print(colored("✓ sort_colors", "green"))

    # Merge Intervals
    assert merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [[1, 6], [8, 10], [15, 18]]
    assert merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]
    assert merge_intervals([[1, 4], [0, 4]]) == [[0, 4]]
    print(colored("✓ merge_intervals", "green"))

    # Largest Number
    assert largest_number([10, 2]) == "210"
    assert largest_number([3, 30, 34, 5, 9]) == "9534330"
    assert largest_number([0, 0]) == "0"
    print(colored("✓ largest_number", "green"))

    print(colored("\nAll tests passed.", "cyan"))
