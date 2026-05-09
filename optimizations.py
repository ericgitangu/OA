"""
Common Optimization Patterns — Space & Time.

Reference: dsa.md (throughout — complexity columns in both tables)

This script is a catalogue of the most frequently applicable optimizations
in interview problems, each shown as a BEFORE → AFTER pair so the gain is
immediately visible.

Patterns covered:
  1.  Two Pointers          — O(n²) → O(n), eliminates inner loop on sorted data
  2.  Sliding Window        — O(n²) → O(n), fixed/variable window on arrays/strings
  3.  Prefix Sum            — O(n) per query → O(1), precompute cumulative sums
  4.  Hash Map Frequency    — O(n²) → O(n), replace nested search with O(1) lookup
  5.  In-Place Reversal     — O(n) space → O(1), reverse without extra array
  6.  Floyd's Cycle         — O(n) space → O(1), detect cycle with two pointers
  7.  Monotonic Stack       — O(n²) → O(n), next-greater/smaller in one pass
  8.  DP Space Compression  — O(n²) space → O(n), rolling array for 2D DP
  9.  Early Exit / Pruning  — constant factor reduction, skip impossible branches
  10. Bit Manipulation      — replace arithmetic/set ops with O(1) bit tricks
"""
from termcolor import colored

# ===========================================================================
# 1. TWO POINTERS  —  O(n²) → O(n)
# ===========================================================================

def two_sum_sorted_SLOW(nums: list[int], target: int) -> list[int]:
    """Brute force: try every pair. T: O(n²)"""
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


def two_sum_sorted_FAST(nums: list[int], target: int) -> list[int]:
    """
    Two Pointers on a SORTED array. T: O(n)  S: O(1)

    Key insight: if the sum is too large, move the right pointer left;
    if too small, move the left pointer right. Each pointer moves at most
    n times → O(n) total.

    LeetCode 167 — Two Sum II (Input Array Is Sorted)

    Example:
        >>> two_sum_sorted_FAST([2,7,11,15], 9)
        [0, 1]
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return [lo, hi]
        elif s < target:
            lo += 1
        else:
            hi -= 1
    return []


def container_with_most_water(height: list[int]) -> int:
    """
    LeetCode 11 — Container With Most Water. T: O(n)  S: O(1)

    Two pointers from both ends. Always move the shorter side inward —
    moving the taller side can only decrease width without increasing height.

    Example:
        >>> container_with_most_water([1,8,6,2,5,4,8,3,7])
        49
    """
    lo, hi = 0, len(height) - 1
    best = 0
    while lo < hi:
        best = max(best, min(height[lo], height[hi]) * (hi - lo))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return best


# ===========================================================================
# 2. SLIDING WINDOW  —  O(n²) → O(n)
# ===========================================================================

def max_subarray_sum_SLOW(nums: list[int], k: int) -> int:
    """Brute force: recompute sum for every window. T: O(n*k)"""
    return max(sum(nums[i:i+k]) for i in range(len(nums) - k + 1))


def max_subarray_sum_FAST(nums: list[int], k: int) -> int:
    """
    Fixed Sliding Window. T: O(n)  S: O(1)

    Key insight: instead of recomputing the sum from scratch, subtract the
    element leaving the window and add the element entering it.

    Example:
        >>> max_subarray_sum_FAST([2,1,5,1,3,2], 3)
        9
    """
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]   # slide: add new, remove old
        best = max(best, window)
    return best


def longest_substring_no_repeat(s: str) -> int:
    """
    LeetCode 3 — Longest Substring Without Repeating Characters.
    Variable Sliding Window. T: O(n)  S: O(min(n, alphabet))

    Key insight: expand right freely; when a duplicate is found, shrink
    from the left until the duplicate is gone. Each character enters and
    leaves the window at most once → O(n).

    Example:
        >>> longest_substring_no_repeat("abcabcbb")
        3
        >>> longest_substring_no_repeat("pwwkew")
        3
    """
    last_seen: dict[str, int] = {}
    lo = best = 0
    for hi, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= lo:
            lo = last_seen[ch] + 1   # shrink window past the duplicate
        last_seen[ch] = hi
        best = max(best, hi - lo + 1)
    return best


# ===========================================================================
# 3. PREFIX SUM  —  O(n) per query → O(1) after O(n) build
# ===========================================================================

def range_sum_SLOW(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """Recompute each range sum from scratch. T: O(n) per query"""
    return [sum(nums[l:r+1]) for l, r in queries]


def range_sum_FAST(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    """
    Prefix Sum. Build: O(n)  Query: O(1)  S: O(n)

    Key insight: prefix[i] = sum of nums[0..i-1].
    Range sum [l, r] = prefix[r+1] - prefix[l].

    LeetCode 303 — Range Sum Query - Immutable

    Example:
        >>> range_sum_FAST([1,2,3,4,5], [(1,3),(0,4)])
        [9, 15]
    """
    prefix = [0] * (len(nums) + 1)
    for i, x in enumerate(nums):
        prefix[i + 1] = prefix[i] + x
    return [prefix[r + 1] - prefix[l] for l, r in queries]


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    """
    LeetCode 560 — Subarray Sum Equals K. T: O(n)  S: O(n)

    Key insight: if prefix[j] - prefix[i] == k, then subarray [i..j-1]
    sums to k. Store prefix sums in a hash map; for each new prefix sum p,
    check if (p - k) was seen before.

    Example:
        >>> subarray_sum_equals_k([1,1,1], 2)
        2
        >>> subarray_sum_equals_k([1,2,3], 3)
        2
    """
    from collections import defaultdict
    count_map: dict[int, int] = defaultdict(int)
    count_map[0] = 1   # empty prefix
    prefix = count = 0
    for x in nums:
        prefix += x
        count += count_map[prefix - k]
        count_map[prefix] += 1
    return count


# ===========================================================================
# 4. HASH MAP FREQUENCY  —  O(n²) → O(n)
# ===========================================================================

def contains_duplicate_SLOW(nums: list[int]) -> bool:
    """Sort then scan. T: O(n log n)"""
    s = sorted(nums)
    return any(s[i] == s[i-1] for i in range(1, len(s)))


def contains_duplicate_FAST(nums: list[int]) -> bool:
    """
    Hash Set. T: O(n)  S: O(n)

    Key insight: a set lookup is O(1); build the set in one pass.

    LeetCode 217 — Contains Duplicate

    Example:
        >>> contains_duplicate_FAST([1,2,3,1])
        True
        >>> contains_duplicate_FAST([1,2,3,4])
        False
    """
    seen: set[int] = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


def two_sum_hash(nums: list[int], target: int) -> list[int]:
    """
    LeetCode 1 — Two Sum (unsorted). T: O(n)  S: O(n)

    Key insight: store each value's index in a hash map. For each new
    element x, check if (target - x) is already in the map in O(1).

    Example:
        >>> two_sum_hash([2,7,11,15], 9)
        [0, 1]
    """
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
    return []


# ===========================================================================
# 5. IN-PLACE OPERATIONS  —  O(n) space → O(1)
# ===========================================================================

def reverse_array_SLOW(nums: list[int]) -> list[int]:
    """Creates a new reversed list. S: O(n)"""
    return nums[::-1]


def reverse_array_FAST(nums: list[int]) -> None:
    """
    In-Place Reversal with two pointers. T: O(n)  S: O(1)

    Key insight: swap elements from both ends moving inward.
    Modifies the list in place — no extra memory.

    Example:
        >>> a = [1,2,3,4,5]
        >>> reverse_array_FAST(a)
        >>> a
        [5, 4, 3, 2, 1]
    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1; hi -= 1


def rotate_array_inplace(nums: list[int], k: int) -> None:
    """
    LeetCode 189 — Rotate Array. T: O(n)  S: O(1)

    Key insight: rotating right by k = reverse all, reverse first k,
    reverse last n-k. Three in-place reversals, no extra array.

    Example:
        >>> a = [1,2,3,4,5,6,7]
        >>> rotate_array_inplace(a, 3)
        >>> a
        [5, 6, 7, 1, 2, 3, 4]
    """
    n = len(nums)
    k %= n

    def rev(lo: int, hi: int) -> None:
        while lo < hi:
            nums[lo], nums[hi] = nums[hi], nums[lo]
            lo += 1; hi -= 1

    rev(0, n - 1)   # reverse entire array
    rev(0, k - 1)   # reverse first k elements
    rev(k, n - 1)   # reverse remaining elements


# ===========================================================================
# 6. FLOYD'S CYCLE DETECTION  —  O(n) space → O(1)
# ===========================================================================

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle_SLOW(head: ListNode | None) -> bool:
    """Store visited nodes in a set. S: O(n)"""
    seen = set()
    node = head
    while node:
        if id(node) in seen:
            return True
        seen.add(id(node))
        node = node.next
    return False


def has_cycle_FAST(head: ListNode | None) -> bool:
    """
    Floyd's Tortoise and Hare. T: O(n)  S: O(1)

    Key insight: slow moves 1 step, fast moves 2. If a cycle exists,
    fast will lap slow and they'll meet. If no cycle, fast reaches None.

    LeetCode 141 — Linked List Cycle

    Example:
        >>> n1,n2,n3 = ListNode(1),ListNode(2),ListNode(3)
        >>> n1.next=n2; n2.next=n3; n3.next=n2  # cycle
        >>> has_cycle_FAST(n1)
        True
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def find_duplicate_FAST(nums: list[int]) -> int:
    """
    LeetCode 287 — Find the Duplicate Number. T: O(n)  S: O(1)

    Key insight: treat the array as a linked list where nums[i] is the
    next pointer from node i. A duplicate creates a cycle. Floyd's
    algorithm finds the cycle entry = the duplicate.

    Example:
        >>> find_duplicate_FAST([1,3,4,2,2])
        2
        >>> find_duplicate_FAST([3,1,3,4,2])
        3
    """
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    # Phase 2: find cycle entry
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow


# ===========================================================================
# 7. MONOTONIC STACK  —  O(n²) → O(n)
# ===========================================================================

def next_greater_SLOW(nums: list[int]) -> list[int]:
    """Brute force: for each element scan right. T: O(n²)"""
    result = [-1] * len(nums)
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[i]:
                result[i] = nums[j]
                break
    return result


def next_greater_FAST(nums: list[int]) -> list[int]:
    """
    Monotonic Decreasing Stack. T: O(n)  S: O(n)

    Key insight: maintain a stack of indices whose "next greater" hasn't
    been found yet. When we see a larger element, it's the answer for
    everything on the stack that is smaller.

    LeetCode 496 — Next Greater Element I

    Example:
        >>> next_greater_FAST([2,1,2,4,3])
        [4, 2, 4, -1, -1]
    """
    result = [-1] * len(nums)
    stack: list[int] = []   # indices of elements awaiting their next greater
    for i, val in enumerate(nums):
        while stack and nums[stack[-1]] < val:
            result[stack.pop()] = val
        stack.append(i)
    return result


# ===========================================================================
# 8. DP SPACE COMPRESSION  —  O(n²) space → O(n)
# ===========================================================================

def lcs_2d(s1: str, s2: str) -> int:
    """Standard 2D DP table. S: O(m*n)"""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]


def lcs_1d(s1: str, s2: str) -> int:
    """
    LCS with rolling 1D array. S: O(n)  (same T: O(m*n))

    Key insight: row i only depends on row i-1. Keep two 1D arrays
    (prev, curr) and swap them each iteration. Further reducible to
    one array with a 'diagonal' variable.

    Example:
        >>> lcs_1d("abcde", "ace")
        3
    """
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                curr[j] = prev[j-1] + 1
            else:
                curr[j] = max(prev[j], curr[j-1])
        prev = curr
    return prev[n]


def knapsack_1d(weights: list[int], values: list[int], cap: int) -> int:
    """
    0/1 Knapsack with 1D DP. S: O(W)  (same T: O(n*W))

    Key insight: iterate capacity RIGHT-TO-LEFT so each item is only
    considered once (prevents using the same item multiple times).

    Example:
        >>> knapsack_1d([1,3,4,5],[1,4,5,7],7)
        9
    """
    dp = [0] * (cap + 1)
    for w, v in zip(weights, values):
        for c in range(cap, w - 1, -1):   # ← right-to-left is the key
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[cap]


# ===========================================================================
# 9. EARLY EXIT / PRUNING
# ===========================================================================

def has_pair_with_sum_SLOW(nums: list[int], target: int) -> bool:
    """Checks all pairs even after finding the answer. T: O(n²)"""
    return any(nums[i] + nums[j] == target
               for i in range(len(nums))
               for j in range(i+1, len(nums)))


def is_palindrome_pruned(s: str) -> bool:
    """
    Palindrome check with early exit. T: O(n)  S: O(1)

    Key insight: compare from both ends; return False the moment a
    mismatch is found instead of building the reversed string.

    Example:
        >>> is_palindrome_pruned("racecar")
        True
        >>> is_palindrome_pruned("hello")
        False
    """
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:
            return False   # early exit — no need to check the rest
        lo += 1; hi -= 1
    return True


def search_matrix(matrix: list[list[int]], target: int) -> bool:
    """
    LeetCode 240 — Search a 2D Matrix II. T: O(m+n)  S: O(1)

    Key insight: start at top-right corner. If current > target, move
    left (eliminate column). If current < target, move down (eliminate
    row). Each step eliminates a full row or column → O(m+n) not O(m*n).

    Example:
        >>> m = [[1,4,7],[2,5,8],[3,6,9]]
        >>> search_matrix(m, 5)
        True
        >>> search_matrix(m, 10)
        False
    """
    if not matrix:
        return False
    r, c = 0, len(matrix[0]) - 1
    while r < len(matrix) and c >= 0:
        if matrix[r][c] == target:
            return True
        elif matrix[r][c] > target:
            c -= 1   # too large — eliminate this column
        else:
            r += 1   # too small — eliminate this row
    return False


# ===========================================================================
# 10. BIT MANIPULATION  —  O(1) tricks
# ===========================================================================

def single_number(nums: list[int]) -> int:
    """
    LeetCode 136 — Single Number. T: O(n)  S: O(1)

    Key insight: XOR of a number with itself is 0; XOR with 0 is the
    number itself. XOR all elements — pairs cancel, leaving the singleton.
    No hash map needed.

    Example:
        >>> single_number([4,1,2,1,2])
        4
    """
    result = 0
    for x in nums:
        result ^= x
    return result


def is_power_of_two(n: int) -> bool:
    """
    LeetCode 231 — Power of Two. T: O(1)  S: O(1)

    Key insight: a power of two has exactly one set bit.
    n & (n-1) clears the lowest set bit. If the result is 0, only one
    bit was set → n is a power of two.

    Example:
        >>> is_power_of_two(16)
        True
        >>> is_power_of_two(18)
        False
    """
    return n > 0 and (n & (n - 1)) == 0


def count_bits(n: int) -> list[int]:
    """
    LeetCode 338 — Counting Bits. T: O(n)  S: O(n)

    Key insight: dp[i] = dp[i >> 1] + (i & 1).
    The number of 1-bits in i equals the bits in i//2 plus the last bit.
    Avoids calling bin() or popcount for each number individually.

    Example:
        >>> count_bits(5)
        [0, 1, 1, 2, 1, 2]
    """
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp


def missing_number(nums: list[int]) -> int:
    """
    LeetCode 268 — Missing Number. T: O(n)  S: O(1)

    Key insight: XOR all indices 0..n with all values. Every present
    number cancels its index; the missing number's index has no partner.

    Example:
        >>> missing_number([3,0,1])
        2
        >>> missing_number([9,6,4,2,3,5,7,0,1])
        8
    """
    result = len(nums)
    for i, x in enumerate(nums):
        result ^= i ^ x
    return result


# ===========================================================================
# Tests
# ===========================================================================
if __name__ == "__main__":
    # 1. Two Pointers
    assert two_sum_sorted_FAST([2, 7, 11, 15], 9) == [0, 1]
    assert container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    print(colored("✓ two pointers", "green"))

    # 2. Sliding Window
    assert max_subarray_sum_FAST([2, 1, 5, 1, 3, 2], 3) == 9
    assert longest_substring_no_repeat("abcabcbb") == 3
    assert longest_substring_no_repeat("pwwkew") == 3
    print(colored("✓ sliding window", "green"))

    # 3. Prefix Sum
    assert range_sum_FAST([1, 2, 3, 4, 5], [(1, 3), (0, 4)]) == [9, 15]
    assert subarray_sum_equals_k([1, 1, 1], 2) == 2
    assert subarray_sum_equals_k([1, 2, 3], 3) == 2
    print(colored("✓ prefix sum", "green"))

    # 4. Hash Map
    assert contains_duplicate_FAST([1, 2, 3, 1]) is True
    assert contains_duplicate_FAST([1, 2, 3, 4]) is False
    assert two_sum_hash([2, 7, 11, 15], 9) == [0, 1]
    print(colored("✓ hash map frequency", "green"))

    # 5. In-Place
    a = [1, 2, 3, 4, 5]
    reverse_array_FAST(a)
    assert a == [5, 4, 3, 2, 1]
    b = [1, 2, 3, 4, 5, 6, 7]
    rotate_array_inplace(b, 3)
    assert b == [5, 6, 7, 1, 2, 3, 4]
    print(colored("✓ in-place operations", "green"))

    # 6. Floyd's Cycle
    n1, n2, n3 = ListNode(1), ListNode(2), ListNode(3)
    n1.next = n2; n2.next = n3; n3.next = n2
    assert has_cycle_FAST(n1) is True
    n4 = ListNode(1); n4.next = ListNode(2)
    assert has_cycle_FAST(n4) is False
    assert find_duplicate_FAST([1, 3, 4, 2, 2]) == 2
    assert find_duplicate_FAST([3, 1, 3, 4, 2]) == 3
    print(colored("✓ Floyd's cycle detection", "green"))

    # 7. Monotonic Stack
    assert next_greater_FAST([2, 1, 2, 4, 3]) == [4, 2, 4, -1, -1]
    assert next_greater_FAST([1, 3, 2, 4]) == [3, 4, 4, -1]
    print(colored("✓ monotonic stack", "green"))

    # 8. DP Space Compression
    assert lcs_1d("abcde", "ace") == 3
    assert lcs_2d("abcde", "ace") == lcs_1d("abcde", "ace")
    assert knapsack_1d([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    print(colored("✓ DP space compression", "green"))

    # 9. Early Exit / Pruning
    assert is_palindrome_pruned("racecar") is True
    assert is_palindrome_pruned("hello") is False
    m = [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    assert search_matrix(m, 5) is True
    assert search_matrix(m, 10) is False
    print(colored("✓ early exit / pruning", "green"))

    # 10. Bit Manipulation
    assert single_number([4, 1, 2, 1, 2]) == 4
    assert is_power_of_two(16) is True
    assert is_power_of_two(18) is False
    assert count_bits(5) == [0, 1, 1, 2, 1, 2]
    assert missing_number([3, 0, 1]) == 2
    assert missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
    print(colored("✓ bit manipulation", "green"))

    print(colored("\nAll tests passed.", "cyan"))
