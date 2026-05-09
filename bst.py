"""
Binary Search Tree (BST) — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Binary Search Tree (BST) (Intermediate)

Key insight from dsa.md:
  - BST property: left subtree values < node < right subtree values.
  - O(log n) average for insert/search/delete when balanced;
    degrades to O(n) on sorted input (skewed tree).
  - Inorder traversal of a BST yields elements in sorted order — this
    is the most commonly tested property in interviews.

Patterns covered:
  1. BST Insert / Search / Inorder  — core operations
  2. Validate BST                   — range-based DFS
  3. Lowest Common Ancestor (BST)   — exploit BST ordering
  4. Kth Smallest in BST            — inorder traversal with counter
  5. Convert Sorted Array to BST    — build balanced BST recursively
"""
from termcolor import colored


class TreeNode:
    """Standard binary tree node used across all problems."""
    def __init__(self, val: int = 0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


# ---------------------------------------------------------------------------
# 1. BST Core Operations
# ---------------------------------------------------------------------------
class BST:
    """
    Binary Search Tree with insert, search, delete, and inorder traversal.

    Reference: dsa.md § Binary Search Tree (BST) (Intermediate)

    T: O(log n) average / O(n) worst for insert, search, delete
    S: O(n) for the tree, O(h) call stack where h = height

    Real-world analogy: a sorted contact list where you can quickly find,
    add, or remove a contact by name without re-sorting the whole list.
    """

    def __init__(self):
        self.root: TreeNode | None = None

    def insert(self, val: int) -> None:
        """Insert val maintaining BST property. T: O(h)"""
        self.root = self._insert(self.root, val)

    def _insert(self, node: TreeNode | None, val: int) -> TreeNode:
        if node is None:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        elif val > node.val:
            node.right = self._insert(node.right, val)
        # equal: ignore duplicates
        return node

    def search(self, val: int) -> bool:
        """Return True if val exists in the BST. T: O(h)"""
        node = self.root
        while node:
            if val == node.val:
                return True
            node = node.left if val < node.val else node.right
        return False

    def delete(self, val: int) -> None:
        """Remove val from BST. T: O(h)"""
        self.root = self._delete(self.root, val)

    def _delete(self, node: TreeNode | None, val: int) -> TreeNode | None:
        if node is None:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Node to delete found
            if node.left is None:
                return node.right   # replace with right child
            if node.right is None:
                return node.left    # replace with left child
            # Two children: replace with inorder successor (min of right subtree)
            successor = node.right
            while successor.left:
                successor = successor.left
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)
        return node

    def inorder(self) -> list[int]:
        """Return values in sorted order via inorder traversal. T: O(n)"""
        result: list[int] = []
        def dfs(node: TreeNode | None) -> None:
            if node:
                dfs(node.left)
                result.append(node.val)
                dfs(node.right)
        dfs(self.root)
        return result


# ---------------------------------------------------------------------------
# 2. Validate BST
# ---------------------------------------------------------------------------
def is_valid_bst(root: TreeNode | None) -> bool:
    """
    LeetCode 98 — Validate Binary Search Tree
    Determine if a binary tree is a valid BST.

    Approach: DFS with a valid range [min_val, max_val] for each node.
    A node is valid only if min_val < node.val < max_val. Recurse left
    with updated max, right with updated min.

    T: O(n)  — visit every node once
    S: O(h)  — recursion stack

    Real-world analogy: auditing a hierarchical approval chain where each
    level must fall within bounds set by its parent.

    Args:
        root: root of binary tree

    Returns:
        True if valid BST

    Example:
        >>> root = TreeNode(2, TreeNode(1), TreeNode(3))
        >>> is_valid_bst(root)
        True
        >>> bad = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
        >>> is_valid_bst(bad)
        False
    """
    def validate(node: TreeNode | None, lo: float, hi: float) -> bool:
        if node is None:
            return True
        if not (lo < node.val < hi):
            return False
        return (validate(node.left, lo, node.val) and
                validate(node.right, node.val, hi))

    return validate(root, float('-inf'), float('inf'))


# ---------------------------------------------------------------------------
# 3. Lowest Common Ancestor of a BST
# ---------------------------------------------------------------------------
def lca_bst(root: TreeNode, p: int, q: int) -> int:
    """
    LeetCode 235 — Lowest Common Ancestor of a BST
    Find the LCA of nodes with values p and q.

    Approach: Exploit BST ordering. If both p and q are less than root,
    LCA is in the left subtree. If both are greater, it's in the right.
    Otherwise, root is the LCA (the split point).

    T: O(h)  — traverse from root to LCA
    S: O(1)  — iterative, no extra space

    Real-world analogy: finding the nearest common manager of two employees
    in a company org chart that is sorted by employee ID.

    Args:
        root: root of BST
        p, q: values of the two nodes

    Returns:
        value of the LCA node

    Example:
        >>> root = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4)),
        ...                    TreeNode(8, TreeNode(7), TreeNode(9)))
        >>> lca_bst(root, 2, 8)
        6
        >>> lca_bst(root, 2, 4)
        2
    """
    node = root
    while node:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node.val  # split point = LCA
    return -1  # unreachable if p, q guaranteed in tree


# ---------------------------------------------------------------------------
# 4. Kth Smallest Element in a BST
# ---------------------------------------------------------------------------
def kth_smallest(root: TreeNode | None, k: int) -> int:
    """
    LeetCode 230 — Kth Smallest Element in a BST
    Find the kth smallest value (1-indexed).

    Approach: Iterative inorder traversal using an explicit stack.
    Inorder visits nodes in ascending order; stop at the kth node.

    T: O(h + k)  — traverse to leftmost node (h steps) then k steps
    S: O(h)      — stack depth

    Real-world analogy: finding the kth cheapest product in a price-sorted
    catalogue without loading the entire catalogue into memory.

    Args:
        root: root of BST
        k:    1-indexed rank

    Returns:
        kth smallest value

    Example:
        >>> root = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
        >>> kth_smallest(root, 1)
        1
        >>> kth_smallest(root, 3)
        3
    """
    stack: list[TreeNode] = []
    node = root
    count = 0
    while stack or node:
        while node:                 # go as far left as possible
            stack.append(node)
            node = node.left
        node = stack.pop()
        count += 1
        if count == k:
            return node.val
        node = node.right
    return -1  # k > number of nodes


# ---------------------------------------------------------------------------
# 5. Convert Sorted Array to Height-Balanced BST
# ---------------------------------------------------------------------------
def sorted_array_to_bst(nums: list[int]) -> TreeNode | None:
    """
    LeetCode 108 — Convert Sorted Array to Binary Search Tree
    Build a height-balanced BST from a sorted array.

    Approach: The middle element of the array becomes the root (minimises
    height). Recursively do the same for left and right halves.

    T: O(n)  — each element becomes a node exactly once
    S: O(log n)  — recursion stack depth for balanced tree

    Real-world analogy: building a balanced binary index from a sorted
    list of database keys to minimise lookup depth.

    Args:
        nums: sorted list of distinct integers

    Returns:
        root of height-balanced BST

    Example:
        >>> root = sorted_array_to_bst([-10,-3,0,5,9])
        >>> BST inorder should equal original array
    """
    if not nums:
        return None
    mid = len(nums) // 2
    node = TreeNode(nums[mid])
    node.left = sorted_array_to_bst(nums[:mid])
    node.right = sorted_array_to_bst(nums[mid + 1:])
    return node


def _inorder(root: TreeNode | None) -> list[int]:
    """Helper: inorder traversal of any binary tree."""
    if root is None:
        return []
    return _inorder(root.left) + [root.val] + _inorder(root.right)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # BST core operations
    tree = BST()
    for v in [5, 3, 7, 1, 4, 6, 8]:
        tree.insert(v)
    assert tree.inorder() == [1, 3, 4, 5, 6, 7, 8]
    assert tree.search(4) is True
    assert tree.search(9) is False
    tree.delete(3)
    assert tree.inorder() == [1, 4, 5, 6, 7, 8]
    tree.delete(5)  # delete root
    assert 5 not in tree.inorder()
    print(colored("✓ BST core operations", "green"))

    # Validate BST
    valid_root = TreeNode(2, TreeNode(1), TreeNode(3))
    assert is_valid_bst(valid_root) is True
    invalid_root = TreeNode(5, TreeNode(1), TreeNode(4, TreeNode(3), TreeNode(6)))
    assert is_valid_bst(invalid_root) is False
    print(colored("✓ is_valid_bst", "green"))

    # LCA of BST
    lca_root = TreeNode(6,
        TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3), TreeNode(5))),
        TreeNode(8, TreeNode(7), TreeNode(9)))
    assert lca_bst(lca_root, 2, 8) == 6
    assert lca_bst(lca_root, 2, 4) == 2
    assert lca_bst(lca_root, 0, 5) == 2
    print(colored("✓ lca_bst", "green"))

    # Kth Smallest
    kth_root = TreeNode(3, TreeNode(1, None, TreeNode(2)), TreeNode(4))
    assert kth_smallest(kth_root, 1) == 1
    assert kth_smallest(kth_root, 3) == 3
    print(colored("✓ kth_smallest", "green"))

    # Sorted Array to BST
    bst_root = sorted_array_to_bst([-10, -3, 0, 5, 9])
    assert _inorder(bst_root) == [-10, -3, 0, 5, 9]
    # Height-balanced: left and right subtree sizes differ by at most 1
    assert bst_root.val == 0  # middle element is root
    print(colored("✓ sorted_array_to_bst", "green"))

    print(colored("\nAll tests passed.", "cyan"))
