"""
Dynamic Programming Patterns — Real-world problems and LeetCode-type questions.

Reference: dsa.md § Dynamic Programming (DP) (Advanced),
           § Dynamic Programming: LIS, § Advanced DP Variation: Minimum Edit Distance,
           § Additional DP examples: 0/1 Knapsack, Coin Change, LCS

Key insight from dsa.md:
  - DP applies when a problem has OVERLAPPING SUBPROBLEMS and OPTIMAL SUBSTRUCTURE.
  - Two styles:
      Top-down (memoisation): recursive + cache. Natural to write, easy to reason about.
      Bottom-up (tabulation): iterative + table. Usually faster (no recursion overhead).
  - Space optimisation: many 2D DP tables can be reduced to 1D by processing row by row.

Patterns covered:
  1. Climbing Stairs / Fibonacci      — 1D DP warm-up (LeetCode 70)
  2. Longest Increasing Subsequence   — 1D DP (LeetCode 300)
  3. Coin Change                       — unbounded knapsack (LeetCode 322)
  4. 0/1 Knapsack                      — classic bounded knapsack
  5. Longest Common Subsequence        — 2D DP (LeetCode 1143)
  6. Edit Distance (Levenshtein)        — 2D DP (LeetCode 72)
  7. Word Break                         — 1D DP + hash set (LeetCode 139)
"""
from termcolor import colored


# ---------------------------------------------------------------------------
# 1. Climbing Stairs
# ---------------------------------------------------------------------------
def climb_stairs(n: int) -> int:
    """
    LeetCode 70 — Climbing Stairs
    Count distinct ways to climb n stairs taking 1 or 2 steps at a time.

    Approach: dp[i] = dp[i-1] + dp[i-2] (Fibonacci recurrence).
    Space-optimised to O(1) using two variables.

    T: O(n)   S: O(1)

    Real-world analogy: counting the number of ways to traverse a sequence
    of checkpoints where you can skip at most one at a time.

    Example:
        >>> climb_stairs(3)
        3
        >>> climb_stairs(5)
        8
    """
    if n <= 2:
        return n
    prev, curr = 1, 2
    for _ in range(3, n + 1):
        prev, curr = curr, prev + curr
    return curr


# ---------------------------------------------------------------------------
# 2. Longest Increasing Subsequence (LIS)
# ---------------------------------------------------------------------------
def length_of_lis(nums: list[int]) -> int:
    """
    LeetCode 300 — Longest Increasing Subsequence
    Find the length of the longest strictly increasing subsequence.

    Approach (O(n log n) patience sorting):
      Maintain a 'tails' array where tails[i] = smallest tail element of
      all increasing subsequences of length i+1. Binary search to find
      where to place each new element.

    T: O(n log n)  — n elements, each binary searched in O(log n)
    S: O(n)        — tails array

    Reference: dsa.md § Dynamic Programming: LIS

    Real-world analogy: finding the longest chain of events that can be
    scheduled in strictly increasing order of start time.

    Args:
        nums: list of integers

    Returns:
        length of the longest strictly increasing subsequence

    Example:
        >>> length_of_lis([10,9,2,5,3,7,101,18])
        4
        >>> length_of_lis([0,1,0,3,2,3])
        4
    """
    import bisect
    tails: list[int] = []
    for x in nums:
        pos = bisect.bisect_left(tails, x)
        if pos == len(tails):
            tails.append(x)   # extend the longest subsequence
        else:
            tails[pos] = x    # replace to keep tails as small as possible
    return len(tails)


# ---------------------------------------------------------------------------
# 3. Coin Change
# ---------------------------------------------------------------------------
def coin_change(coins: list[int], amount: int) -> int:
    """
    LeetCode 322 — Coin Change
    Find the minimum number of coins to make up the given amount.
    Return -1 if it's not possible.

    Approach (bottom-up unbounded knapsack):
      dp[i] = min coins to make amount i.
      For each amount i, try every coin c: dp[i] = min(dp[i], dp[i-c] + 1).

    T: O(amount * len(coins))
    S: O(amount)

    Reference: dsa.md § Coin Change (Minimum Coins)

    Real-world analogy: a vending machine finding the fewest coins to
    return as change for a given amount.

    Args:
        coins:  list of coin denominations
        amount: target amount

    Returns:
        minimum number of coins, or -1 if impossible

    Example:
        >>> coin_change([1,2,5], 11)
        3
        >>> coin_change([2], 3)
        -1
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # base case: 0 coins needed for amount 0

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1

    return dp[amount] if dp[amount] != float('inf') else -1


# ---------------------------------------------------------------------------
# 4. 0/1 Knapsack
# ---------------------------------------------------------------------------
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Classic 0/1 Knapsack Problem
    Maximise total value of items that fit within a weight capacity.
    Each item can be taken at most once (0/1 choice).

    Approach (space-optimised bottom-up):
      dp[w] = max value achievable with capacity w.
      Process items one by one; iterate capacity RIGHT-TO-LEFT to prevent
      using the same item twice (key difference from unbounded knapsack).

    T: O(n * W)  — n items, W = capacity
    S: O(W)      — 1D dp array (space-optimised from 2D)

    Reference: dsa.md § 0/1 Knapsack Problem

    Real-world analogy: packing a hiking backpack — each item has a weight
    and value, and you can only carry so much total weight.

    Args:
        weights:  list of item weights
        values:   list of item values (parallel to weights)
        capacity: maximum weight capacity

    Returns:
        maximum total value

    Example:
        >>> knapsack_01([1,3,4,5], [1,4,5,7], 7)
        9
        >>> knapsack_01([2,3,4], [3,4,5], 5)
        7
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        # Traverse right-to-left: ensures item i is used at most once
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]


# ---------------------------------------------------------------------------
# 5. Longest Common Subsequence (LCS)
# ---------------------------------------------------------------------------
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    LeetCode 1143 — Longest Common Subsequence
    Find the length of the longest subsequence common to both strings.
    (A subsequence doesn't need to be contiguous.)

    Approach (bottom-up 2D DP, space-optimised to 1D):
      dp[j] = LCS length of text1[0..i] and text2[0..j].
      Recurrence:
        if text1[i] == text2[j]: dp[j] = prev_dp[j-1] + 1
        else:                    dp[j] = max(dp[j-1], prev_dp[j])

    T: O(m * n)  — m = len(text1), n = len(text2)
    S: O(n)      — two 1D arrays instead of full 2D table

    Reference: dsa.md § Longest Common Subsequence (LCS)

    Real-world analogy: finding the longest shared edit history between
    two versions of a document (basis of diff tools like git diff).

    Args:
        text1, text2: input strings

    Returns:
        length of longest common subsequence

    Example:
        >>> longest_common_subsequence("abcde", "ace")
        3
        >>> longest_common_subsequence("abc", "abc")
        3
        >>> longest_common_subsequence("abc", "def")
        0
    """
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)

    for i in range(m):
        curr = [0] * (n + 1)
        for j in range(n):
            if text1[i] == text2[j]:
                curr[j + 1] = prev[j] + 1
            else:
                curr[j + 1] = max(curr[j], prev[j + 1])
        prev = curr

    return prev[n]


# ---------------------------------------------------------------------------
# 6. Edit Distance (Levenshtein Distance)
# ---------------------------------------------------------------------------
def min_distance(word1: str, word2: str) -> int:
    """
    LeetCode 72 — Edit Distance
    Find the minimum number of operations (insert, delete, replace) to
    transform word1 into word2.

    Approach (bottom-up 2D DP, space-optimised to 1D):
      dp[j] = edit distance between word1[0..i] and word2[0..j].
      Recurrence:
        if word1[i-1] == word2[j-1]: dp[j] = prev[j-1]  (no op needed)
        else: dp[j] = 1 + min(prev[j],    # delete from word1
                               dp[j-1],   # insert into word1
                               prev[j-1]) # replace

    T: O(m * n)
    S: O(n)

    Reference: dsa.md § Advanced DP Variation: Minimum Edit Distance

    Real-world analogy: spell-checker computing how "close" a misspelled
    word is to dictionary entries (used in autocorrect suggestions).

    Args:
        word1, word2: input strings

    Returns:
        minimum edit distance

    Example:
        >>> min_distance("horse", "ros")
        3
        >>> min_distance("intention", "execution")
        5
        >>> min_distance("", "abc")
        3
    """
    m, n = len(word1), len(word2)
    # Base case: transforming empty string to word2[0..j] costs j insertions
    prev = list(range(n + 1))

    for i in range(1, m + 1):
        curr = [i] + [0] * n  # transforming word1[0..i] to "" costs i deletions
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                curr[j] = prev[j - 1]  # characters match — no operation
            else:
                curr[j] = 1 + min(prev[j],      # delete word1[i-1]
                                   curr[j - 1],  # insert word2[j-1]
                                   prev[j - 1])  # replace word1[i-1] with word2[j-1]
        prev = curr

    return prev[n]


# ---------------------------------------------------------------------------
# 7. Word Break
# ---------------------------------------------------------------------------
def word_break(s: str, word_dict: list[str]) -> bool:
    """
    LeetCode 139 — Word Break
    Determine if s can be segmented into words from word_dict.

    Approach (bottom-up 1D DP):
      dp[i] = True if s[0..i-1] can be segmented.
      For each position i, check all j < i: if dp[j] is True and
      s[j..i-1] is in the dictionary, then dp[i] = True.

    T: O(n² * m)  — n = len(s), m = avg word length for hash lookup
    S: O(n + W)   — dp array + word set

    Real-world analogy: a tokeniser checking whether a raw string of
    characters can be split into valid tokens from a known vocabulary.

    Args:
        s:         input string
        word_dict: list of valid words

    Returns:
        True if s can be fully segmented

    Example:
        >>> word_break("leetcode", ["leet","code"])
        True
        >>> word_break("applepenapple", ["apple","pen"])
        True
        >>> word_break("catsandog", ["cats","dog","sand","and","cat"])
        False
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # empty prefix is always valid

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break  # no need to check further j values

    return dp[n]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Climbing Stairs
    assert climb_stairs(1) == 1
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
    print(colored("✓ climb_stairs", "green"))

    # LIS
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7, 7]) == 1
    print(colored("✓ length_of_lis", "green"))

    # Coin Change
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
    print(colored("✓ coin_change", "green"))

    # 0/1 Knapsack
    assert knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7) == 9
    assert knapsack_01([2, 3, 4], [3, 4, 5], 5) == 7
    assert knapsack_01([], [], 10) == 0
    print(colored("✓ knapsack_01", "green"))

    # LCS
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0
    print(colored("✓ longest_common_subsequence", "green"))

    # Edit Distance
    assert min_distance("horse", "ros") == 3
    assert min_distance("intention", "execution") == 5
    assert min_distance("", "abc") == 3
    assert min_distance("abc", "") == 3
    print(colored("✓ min_distance", "green"))

    # Word Break
    assert word_break("leetcode", ["leet", "code"]) is True
    assert word_break("applepenapple", ["apple", "pen"]) is True
    assert word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False
    print(colored("✓ word_break", "green"))

    print(colored("\nAll tests passed.", "cyan"))
