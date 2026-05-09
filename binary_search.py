"""
Binary Search — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Binary Search (Basic)

Key insight from dsa.md:
  - Binary search requires a SORTED (or monotonic) search space.
  - Each iteration eliminates half the remaining candidates → O(log n).
  - The hard part is not the algorithm itself but recognising WHAT to
    binary-search on: an index, a value, or an answer range.

Patterns covered:
  1. Classic Binary Search          — find exact value in sorted array
  2. Search Insert Position         — leftmost insertion point (lower bound)
  3. Find Minimum in Rotated Array  — binary search on a rotated sorted array
  4. Search in Rotated Sorted Array — find target in rotated array
  5. Koko Eating Bananas            — binary search on the ANSWER (speed)
"""
from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Classic Binary Search
# ---------------------------------------------------------------------------
def binary_search(nums: list[int], target: int) -> int:
    """
    LeetCode 704 — Binary Search
    Find the index of target in a sorted array, or -1 if not present.

    Approach: Maintain [lo, hi] window. Compare mid to target and halve
    the window each iteration.

    T: O(log n)  — window halves each step
    S: O(1)      — three pointers only

    Real-world analogy: looking up a word in a physical dictionary by
    opening to the middle and deciding which half to continue in.

    Args:
        nums:   sorted list of distinct integers
        target: value to find

    Returns:
        index of target, or -1

    Example:
        >>> binary_search([-1,0,3,5,9,12], 9)
        4
        >>> binary_search([-1,0,3,5,9,12], 2)
        -1
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # avoids overflow vs (lo+hi)//2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# 2. Search Insert Position (Lower Bound)
# ---------------------------------------------------------------------------
def search_insert(nums: list[int], target: int) -> int:
    """
    LeetCode 35 — Search Insert Position
    Return the index where target is found, or where it would be inserted
    to keep the array sorted.

    Approach: Standard lower-bound binary search. After the loop, lo is
    the first index where nums[lo] >= target.

    T: O(log n)
    S: O(1)

    Real-world analogy: finding the correct slot to insert a new record
    into a sorted database index without a full scan.

    Args:
        nums:   sorted list of distinct integers
        target: value to find or insert

    Returns:
        index of target or insertion point

    Example:
        >>> search_insert([1,3,5,6], 5)
        2
        >>> search_insert([1,3,5,6], 2)
        1
        >>> search_insert([1,3,5,6], 7)
        4
    """
    lo, hi = 0, len(nums)  # hi = len(nums) so we can insert at the end
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid  # mid could be the answer; don't exclude it
    return lo


# ---------------------------------------------------------------------------
# 3. Find Minimum in Rotated Sorted Array
# ---------------------------------------------------------------------------
def find_min_rotated(nums: list[int]) -> int:
    """
    LeetCode 153 — Find Minimum in Rotated Sorted Array
    Array was sorted then rotated at some pivot. Find the minimum.

    Approach: The minimum is at the rotation point. If nums[mid] > nums[hi],
    the minimum is in the right half; otherwise it's in the left half
    (including mid itself).

    T: O(log n)
    S: O(1)

    Real-world analogy: finding the "reset point" in a circular log buffer
    where entries wrap around.

    Args:
        nums: rotated sorted array with distinct values

    Returns:
        minimum value

    Example:
        >>> find_min_rotated([3,4,5,1,2])
        1
        >>> find_min_rotated([4,5,6,7,0,1,2])
        0
        >>> find_min_rotated([11,13,15,17])
        11
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1  # min is in the right half
        else:
            hi = mid      # mid could be the min; keep it
    return nums[lo]


# ---------------------------------------------------------------------------
# 4. Search in Rotated Sorted Array
# ---------------------------------------------------------------------------
def search_rotated(nums: list[int], target: int) -> int:
    """
    LeetCode 33 — Search in Rotated Sorted Array
    Find target in a rotated sorted array (distinct values).

    Approach: At every mid, one of the two halves is guaranteed to be
    sorted. Determine which half is sorted, then check if target falls
    within it to decide which half to continue searching.

    T: O(log n)
    S: O(1)

    Real-world analogy: searching a circular shift register where data
    wraps around but is otherwise ordered.

    Args:
        nums:   rotated sorted array with distinct values
        target: value to find

    Returns:
        index of target, or -1

    Example:
        >>> search_rotated([4,5,6,7,0,1,2], 0)
        4
        >>> search_rotated([4,5,6,7,0,1,2], 3)
        -1
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        if nums[mid] == target:
            return mid

        # Left half is sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


# ---------------------------------------------------------------------------
# 5. Koko Eating Bananas (Binary Search on Answer)
# ---------------------------------------------------------------------------
def min_eating_speed(piles: list[int], h: int) -> int:
    """
    LeetCode 875 — Koko Eating Bananas
    Find the minimum eating speed k (bananas/hour) such that all piles
    can be eaten within h hours.

    Approach: Binary search on the ANSWER (speed k) in range [1, max(piles)].
    For a given speed k, hours needed = sum(ceil(pile/k) for pile in piles).
    Find the smallest k where total hours <= h.

    T: O(n log m)  — n = len(piles), m = max(piles); log m binary search
                     steps, each O(n) to compute hours
    S: O(1)

    Real-world analogy: finding the minimum server throughput needed to
    process all queued jobs within a deadline.

    Args:
        piles: list of pile sizes
        h:     total hours available (h >= len(piles))

    Returns:
        minimum integer eating speed

    Example:
        >>> min_eating_speed([3,6,7,11], 8)
        4
        >>> min_eating_speed([30,11,23,4,20], 5)
        30
    """
    import math

    def hours_needed(speed: int) -> int:
        return sum(math.ceil(pile / speed) for pile in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if hours_needed(mid) <= h:
            hi = mid      # mid works; try slower
        else:
            lo = mid + 1  # too slow; need faster
    return lo


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Classic Binary Search
    assert binary_search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert binary_search([-1, 0, 3, 5, 9, 12], 2) == -1
    assert binary_search([5], 5) == 0
    print(colored("✓ binary_search", "green"))

    # Search Insert Position
    assert search_insert([1, 3, 5, 6], 5) == 2
    assert search_insert([1, 3, 5, 6], 2) == 1
    assert search_insert([1, 3, 5, 6], 7) == 4
    assert search_insert([1, 3, 5, 6], 0) == 0
    print(colored("✓ search_insert", "green"))

    # Find Minimum in Rotated Array
    assert find_min_rotated([3, 4, 5, 1, 2]) == 1
    assert find_min_rotated([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min_rotated([11, 13, 15, 17]) == 11
    print(colored("✓ find_min_rotated", "green"))

    # Search in Rotated Sorted Array
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert search_rotated([1], 0) == -1
    print(colored("✓ search_rotated", "green"))

    # Koko Eating Bananas
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_eating_speed([30, 11, 23, 4, 20], 6) == 23
    print(colored("✓ min_eating_speed", "green"))

    print(colored("\nAll tests passed.", "cyan"))
