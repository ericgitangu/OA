# The 4-Hour 4AM Competitive Programming Routine

This routine leverages your past experience (200+ completed problems) to rapidly restore and exceed your previous algorithmic readiness level. By structuring your 4 hours every morning (4:00 AM - 8:00 AM) efficiently, you will merge spaced repetition with aggressive problem-solving.

> [!TIP]
> The primary goal of this schedule is **Pattern Recognition and Mastery**, not just grinding number counts. We will accomplish this by pairing known implementations in your `OA/dsa.md` guide with new LeetCode challenges.

---

## The Schedule Breakdown

### 🎯 Phase 1: Context Loading & Spaced Repetition (04:00 - 04:30)

**Duration:** 30 Minutes
**Goal:** Warm up the brain and reinforce previously established neural pathways.

1. **(10 mins) Pattern Review:** Pick one algorithmic pattern for the day (e.g., Two Pointers, Sliding Window, DP, or Graph traversals). Re-read the corresponding section in your `dsa.md` or glance over the scripts in the `OA` folder (like `bfs.py`).
1. **(20 mins) The "Known" Grind:** Go to LeetCode and pick a problem **you have already solved in the past** (from your 200 solved list) that fits today's pattern.
   - **Constraint:** Attempt to code it out from scratch in under 15 minutes. Focus strictly on clean, bug-free python implementation. If you fail or struggle, do not panic; mark it for tomorrow's review.

### 🔥 Phase 2: Deep Work & Discovery (04:30 - 06:15)

**Duration:** 1 Hour 45 Minutes
**Goal:** Push your boundaries and test your pattern recognition on unseen problems.

1. **Problem Selection:** Pick 2 Mediums or 1 Hard problem from a curated FAANG-ready list (like the NeetCode 150 or Grind 75) based on the day's pattern.
1. **Strict Timeboxing:**
   - For **Mediums**: Set a timer for 35 minutes.
   - For **Hards**: Set a timer for 50 minutes.
1. **Execution Rules:**
   - Spend the first 10-15 minutes *only* thinking and writing comments/pseudocode. What is the brute force? What are the overlapping subproblems? How can you optimize it using a Hash Map or Heap?
   - *Do not execute code until you've verified your logic on edge cases.*
   - If the timer runs out and you do not have an optimal passing solution, **STOP**. Move immediately to Phase 3.

### 🧠 Phase 3: Solution Deconstruction & Hardening (06:15 - 07:15)

**Duration:** 1 Hour
**Goal:** Analyze where you failed, learn the optimal approach, and permanently bridge the knowledge gap.

1. **Analyze:** Open the optimal solution on LeetCode (or NeetCode video). Do **not** look at the code first. Listen/read the intuition.
1. **Dissect:** Once you understand the intuition, close the solution. Code it entirely from scratch.
1. **Complexity Check:** Write down the Time (`O(T)`) and Space (`O(S)`) complexity as comments at the top of your function. Justify them.

> [!WARNING]  
> Never copy-paste solutions. The act of typing out the code, even if you know the logic, builds muscle memory for edge-cases (like matrix boundaries or pointer updates).

### ✍️ Phase 4: Documentation & Systematization (07:15 - 08:00)

**Duration:** 45 Minutes
**Goal:** Cement your learnings into your `OA` repository so you can reference them in future Phase 1 reviews.

1. **Repo Integration:** Create a standalone Python script (e.g., `sliding_window_maximum.py`) in your `OA` directory, similar to your existing structural files.
1. **Document:** Write out extensive comments explaining the "Why" and the "How". Add test cases at the bottom of the script.
1. **Update `dsa.md`:** If you learned a new trick (e.g., a clever bit manipulation or an optimization), add it as a new section or update an existing table in `dsa.md`.

---

## Weekly Progression Strategy

To ensure comprehensive coverage, structure your week by grouping data structures logically:

| Day | Primary Focus | Secondary Focus (Review) | Suggested `OA` Reference scripts |
| :---: | :--- | :--- | :--- |
| **Monday** | Arrays, Hashing, & Strings | None | `longest_palidromic_string.py`, `text_search_algoritms.py` |
| **Tuesday** | Two Pointers & Sliding Window | Arrays & Strings | - |
| **Wednesday** | Stacks, Queues, & Linked Lists | Two Pointers | `linked_lists.py`, `circular_linked_lists.py` |
| **Thursday** | Trees, Tries, & Heaps | Stacks/Queues | `min_max-heap.py` |
| **Friday** | Graphs & Advanced Traversals | Trees/Heaps | `bfs.py`, `dfs.py`, `graph_traversal.py` |
| **Saturday** | Dynamic Programming & Greedy | Graphs | `dynamic_programming_knapsack.py` |
| **Sunday** | *Mock Interview / Contest Simulation* | Global Review | Complete blind 4-question set. |

> [!IMPORTANT]
> The Sunday Mock Interview is critical. Select a randomized set of 4 problems on Leetcode (1 Easy, 2 Mediums, 1 Hard) and give yourself exactly 1.5 hours without any interruptions to simulate an actual Online Assessment.

## Getting Started: Day 1 (Tomorrow)

Since you are returning from a hiatus but have a foundation of 200 problems:

1. **Focus:** Arrays and Hashing.
1. **Phase 1 Problem:** Re-do *Two Sum* and *Valid Anagram* (focus on extreme speed and perfect syntax).
1. **Phase 2 Problem:** Try *Group Anagrams* and *Top K Frequent Elements*.

Execute this plan for two weeks consistently. At the end of the two weeks, you will find your OA speed and pattern recognition will have drastically sharpened.
