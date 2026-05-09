"""
Arrays & Hashing — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Array (Basic) and § Hash Table / Hash Map (Intermediate)

Key insight from dsa.md:
  - Arrays give O(1) random access but O(n) insert/delete in the middle.
  - Hash maps give O(1) average insert/lookup/delete — the go-to for
    "have we seen this before?" and frequency-counting problems.

Patterns covered:
  1. Two Sum              — hash map for complement lookup
  2. Group Anagrams       — hash map keyed by sorted word (canonical form)
  3. Top-K Frequent       — frequency map + bucket sort (O(n))
  4. Product Except Self  — prefix/suffix products without division
  5. Longest Consecutive  — hash set for O(n) sequence detection
"""

from collections import defaultdict
from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Two Sum
# ---------------------------------------------------------------------------
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    LeetCode 1 — Two Sum
    Find indices of two numbers that add up to target.

    Approach: For each number x, check if (target - x) is already in the
    hash map. If yes, we found our pair. If no, store x with its index.

    T: O(n)  — single pass through the array
    S: O(n)  — hash map stores up to n elements

    Real-world analogy: matching a purchase amount against a list of
    previously seen transactions to find a pair that sums to a budget.

    Args:
        nums:   list of integers
        target: desired sum

    Returns:
        [i, j] where nums[i] + nums[j] == target

    Example:
        >>> two_sum([2, 7, 11, 15], 9)
        [0, 1]
        >>> two_sum([3, 2, 4], 6)
        [1, 2]
    """
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []  # no solution (problem guarantees one exists)


# ---------------------------------------------------------------------------
# 2. Group Anagrams
# ---------------------------------------------------------------------------
def group_anagrams(words: list[str]) -> list[list[str]]:
    """
    LeetCode 49 — Group Anagrams
    Group strings that are anagrams of each other.

    Approach: Two words are anagrams iff their sorted characters are equal.
    Use sorted(word) as a canonical key in a hash map.

    T: O(n * k log k)  — n words, each sorted in O(k log k) where k = len(word)
    S: O(n * k)        — storing all words in the map

    Real-world analogy: grouping product SKUs that share the same letters
    (e.g. inventory deduplication).

    Args:
        words: list of lowercase strings

    Returns:
        list of groups, each group containing anagram strings

    Example:
        >>> sorted(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
        [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))  # canonical anagram key
        groups[key].append(word)
    return list(groups.values())


# ---------------------------------------------------------------------------
# 3. Top-K Frequent Elements
# ---------------------------------------------------------------------------
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    LeetCode 347 — Top K Frequent Elements
    Return the k most frequently occurring elements.

    Approach: Bucket sort by frequency. Since max frequency <= n, create
    n+1 buckets indexed by frequency. This avoids an O(n log n) heap sort.

    T: O(n)  — frequency count + bucket fill + single reverse scan
    S: O(n)  — frequency map + buckets

    Real-world analogy: finding the top-k trending hashtags from a stream
    of posts without a full sort.

    Args:
        nums: list of integers
        k:    number of top elements to return

    Returns:
        list of k most frequent elements (any order)

    Example:
        >>> top_k_frequent([1,1,1,2,2,3], 2)
        [1, 2]
        >>> top_k_frequent([1], 1)
        [1]
    """
    freq: dict[int, int] = defaultdict(int)
    for n in nums:
        freq[n] += 1

    # buckets[i] holds all numbers that appear exactly i times
    buckets: list[list[int]] = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    result = []
    for i in range(len(buckets) - 1, 0, -1):  # scan high freq → low
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result


# ---------------------------------------------------------------------------
# 4. Product of Array Except Self
# ---------------------------------------------------------------------------
def product_except_self(nums: list[int]) -> list[int]:
    """
    LeetCode 238 — Product of Array Except Self
    Return array where output[i] = product of all nums except nums[i].
    Division is NOT allowed.

    Approach: Two passes.
      Pass 1 (left→right): output[i] = product of all elements to the LEFT of i.
      Pass 2 (right→left): multiply output[i] by product of all elements to the RIGHT.

    T: O(n)  — two linear passes
    S: O(1)  — output array doesn't count as extra space per problem rules

    Real-world analogy: computing the "impact score" of removing each sensor
    from a pipeline where the combined reading is a product of all sensors.

    Args:
        nums: list of integers (length >= 2)

    Returns:
        list where result[i] = product of all nums except nums[i]

    Example:
        >>> product_except_self([1, 2, 3, 4])
        [24, 12, 8, 6]
        >>> product_except_self([-1, 1, 0, -3, 3])
        [0, 0, 9, 0, 0]
    """
    n = len(nums)
    output = [1] * n

    # Left pass: output[i] holds product of nums[0..i-1]
    prefix = 1
    for i in range(n):
        output[i] = prefix
        prefix *= nums[i]

    # Right pass: multiply by product of nums[i+1..n-1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        output[i] *= suffix
        suffix *= nums[i]

    return output


# ---------------------------------------------------------------------------
# 5. Longest Consecutive Sequence
# ---------------------------------------------------------------------------
def longest_consecutive(nums: list[int]) -> int:
    """
    LeetCode 128 — Longest Consecutive Sequence
    Find the length of the longest sequence of consecutive integers.
    Must run in O(n).

    Approach: Put all numbers in a hash set. For each number n, only start
    counting a sequence if (n-1) is NOT in the set — this ensures we only
    start at the beginning of a sequence, giving O(n) total work.

    T: O(n)  — each number is visited at most twice
    S: O(n)  — hash set

    Real-world analogy: finding the longest unbroken streak of daily logins
    in a user activity log.

    Args:
        nums: list of integers (may be unsorted, may have duplicates)

    Returns:
        length of the longest consecutive sequence

    Example:
        >>> longest_consecutive([100, 4, 200, 1, 3, 2])
        4
        >>> longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])
        9
    """
    num_set = set(nums)
    best = 0

    for n in num_set:
        if n - 1 not in num_set:  # n is the start of a sequence
            length = 1
            while n + length in num_set:
                length += 1
            best = max(best, length)

    return best


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(colored("=" * 60, "red"))
    print(colored("  Arrays & Hashing", "magenta"))
    print(colored("=" * 60, "red"))
    # Two Sum
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]
    assert two_sum([3, 2, 4], 6) == [1, 2]
    assert two_sum([3, 3], 6) == [0, 1]
    print(colored("✓ two_sum", "green"))

    # Group Anagrams
    result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    result_sorted = sorted([sorted(g) for g in result])
    assert result_sorted == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    print(colored("✓ group_anagrams", "green"))

    # Top-K Frequent
    assert set(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == {1, 2}
    assert top_k_frequent([1], 1) == [1]
    print(colored("✓ top_k_frequent", "green"))

    # Product Except Self
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    print(colored("✓ product_except_self", "green"))

    # Longest Consecutive
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    print(colored("✓ longest_consecutive", "green"))

    print(colored("\nAll tests passed.", "cyan"))
