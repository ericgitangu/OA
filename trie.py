"""
Trie (Prefix Tree) — Real-world patterns and LeetCode-type problems.

Reference: dsa.md § Trie (Prefix Tree) (Advanced)

Key insight from dsa.md:
  - Trie gives O(m) insert/search where m = word length — independent of
    the number of words stored (unlike hash map which is O(m) average but
    with collision risk).
  - Shared prefixes are stored once → space-efficient for large word sets
    with common prefixes (e.g. autocomplete dictionaries).
  - The end_of_word flag is critical: "app" and "apple" share a path but
    only "apple" has end_of_word=True at the 'e' node.

Patterns covered:
  1. Trie (insert / search / startsWith)  — LeetCode 208, core structure
  2. Word Search II                        — Trie + DFS backtracking on grid
  3. Replace Words                         — find shortest root prefix
  4. Design Add and Search Words           — Trie with '.' wildcard
"""
from termcolor import colored


class TrieNode:
    """
    A single node in the Trie.

    Attributes:
        children:    dict mapping char → TrieNode
        end_of_word: True if a complete word ends at this node
    """
    __slots__ = ("children", "end_of_word")

    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.end_of_word: bool = False


# ---------------------------------------------------------------------------
# 1. Implement Trie
# ---------------------------------------------------------------------------
class Trie:
    """
    LeetCode 208 — Implement Trie (Prefix Tree)
    Supports insert, search (exact word), and startsWith (prefix check).

    T: O(m) per operation where m = length of word/prefix
    S: O(n * m) total where n = number of words, m = average length
       (shared prefixes reduce actual space)

    Real-world analogy: the autocomplete engine in a search bar — every
    keystroke traverses one level of the trie to find matching suggestions.

    Example:
        >>> t = Trie()
        >>> t.insert("apple")
        >>> t.search("apple")
        True
        >>> t.search("app")
        False
        >>> t.starts_with("app")
        True
        >>> t.insert("app")
        >>> t.search("app")
        True
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word into the trie. T: O(m)"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end_of_word = True

    def search(self, word: str) -> bool:
        """Return True if word is in the trie (exact match). T: O(m)"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Return True if any word in the trie starts with prefix. T: O(m)"""
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True  # reached end of prefix — at least one word continues


# ---------------------------------------------------------------------------
# 2. Word Search II (Trie + DFS backtracking)
# ---------------------------------------------------------------------------
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """
    LeetCode 212 — Word Search II
    Find all words from the list that exist in the board (connected cells,
    no cell reused in a single word).

    Approach: Build a Trie from all words. DFS from every cell; at each
    step, follow the trie path. When end_of_word is reached, record the
    word. Prune trie nodes after finding a word to avoid duplicates and
    speed up future searches.

    T: O(M * 4 * 3^(L-1))  — M cells, each DFS explores 4 directions
                              then 3 (can't go back), L = max word length
    S: O(N * L)             — trie storage, N = number of words

    Real-world analogy: a word-find puzzle solver that uses a dictionary
    index (trie) to prune dead-end paths early.

    Args:
        board: 2D grid of characters
        words: list of words to find

    Returns:
        list of words found in the board

    Example:
        >>> board = [["o","a","a","n"],["e","t","a","e"],
        ...          ["i","h","k","r"],["i","f","l","v"]]
        >>> sorted(find_words(board, ["oath","pea","eat","rain"]))
        ['eat', 'oath']
    """
    # Build trie from word list
    root = TrieNode()
    for word in words:
        node = root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end_of_word = True  # store word at terminal node

    rows, cols = len(board), len(board[0])
    found: list[str] = []

    def dfs(r: int, c: int, node: TrieNode, path: str) -> None:
        ch = board[r][c]
        if ch not in node.children:
            return
        next_node = node.children[ch]
        path += ch

        if next_node.end_of_word:
            found.append(path)
            next_node.end_of_word = False  # prune: don't add duplicate

        board[r][c] = '#'  # mark visited
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
                dfs(nr, nc, next_node, path)
        board[r][c] = ch  # restore

        # Prune empty trie nodes to speed up future searches
        if not next_node.children:
            del node.children[ch]

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root, "")

    return found


# ---------------------------------------------------------------------------
# 3. Replace Words
# ---------------------------------------------------------------------------
def replace_words(dictionary: list[str], sentence: str) -> str:
    """
    LeetCode 648 — Replace Words
    Replace each word in the sentence with its shortest root from the
    dictionary. If no root exists, keep the original word.

    Approach: Insert all roots into a trie. For each word in the sentence,
    traverse the trie character by character; stop at the first
    end_of_word encountered — that's the shortest root.

    T: O(D + S)  — D = total chars in dictionary, S = total chars in sentence
    S: O(D)      — trie storage

    Real-world analogy: a text normaliser that reduces inflected words to
    their stem (e.g. "running" → "run") using a prefix dictionary.

    Args:
        dictionary: list of root words
        sentence:   space-separated string of words

    Returns:
        sentence with words replaced by their shortest root

    Example:
        >>> replace_words(["cat","bat","rat"], "the cattle was rattled by the battery")
        'the cat was rat by the bat'
    """
    trie = Trie()
    for root in dictionary:
        trie.insert(root)

    def shortest_root(word: str) -> str:
        node = trie.root
        for i, ch in enumerate(word):
            if ch not in node.children:
                break
            node = node.children[ch]
            if node.end_of_word:
                return word[:i + 1]  # found shortest root
        return word  # no root found

    return " ".join(shortest_root(w) for w in sentence.split())


# ---------------------------------------------------------------------------
# 4. Design Add and Search Words (with '.' wildcard)
# ---------------------------------------------------------------------------
class WordDictionary:
    """
    LeetCode 211 — Design Add and Search Words Data Structure
    Supports adding words and searching with '.' as a wildcard for any char.

    Approach: Standard trie insert. For search, when '.' is encountered,
    recursively try all children at that position.

    T: O(m) insert, O(26^d * m) search worst case where d = number of dots
    S: O(n * m) trie storage

    Real-world analogy: a regex-lite search in a contact list where '.'
    matches any single character (e.g. "j.hn" matches "john" or "jahn").

    Example:
        >>> wd = WordDictionary()
        >>> wd.add_word("bad"); wd.add_word("dad"); wd.add_word("mad")
        >>> wd.search("pad")
        False
        >>> wd.search("bad")
        True
        >>> wd.search(".ad")
        True
        >>> wd.search("b..")
        True
    """

    def __init__(self):
        self.root = TrieNode()

    def add_word(self, word: str) -> None:
        """Insert word. T: O(m)"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.end_of_word = True

    def search(self, word: str) -> bool:
        """Search with '.' wildcard. T: O(26^d * m) worst case"""
        return self._search(word, 0, self.root)

    def _search(self, word: str, idx: int, node: TrieNode) -> bool:
        if idx == len(word):
            return node.end_of_word
        ch = word[idx]
        if ch == '.':
            # Try every possible child
            return any(self._search(word, idx + 1, child)
                       for child in node.children.values())
        if ch not in node.children:
            return False
        return self._search(word, idx + 1, node.children[ch])


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Trie basic operations
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.starts_with("app") is True
    t.insert("app")
    assert t.search("app") is True
    assert t.starts_with("xyz") is False
    print(colored("✓ Trie insert/search/starts_with", "green"))

    # Word Search II
    board = [["o","a","a","n"],
             ["e","t","a","e"],
             ["i","h","k","r"],
             ["i","f","l","v"]]
    result = find_words(board, ["oath","pea","eat","rain"])
    assert sorted(result) == ["eat", "oath"]
    print(colored("✓ find_words (Word Search II)", "green"))

    # Replace Words
    assert replace_words(["cat","bat","rat"],
                         "the cattle was rattled by the battery") == \
           "the cat was rat by the bat"
    assert replace_words(["a","b","c"],
                         "aadsfasf absbs bbab cadsfafs") == "a a b c"
    print(colored("✓ replace_words", "green"))

    # WordDictionary with wildcard
    wd = WordDictionary()
    for w in ["bad", "dad", "mad"]:
        wd.add_word(w)
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True
    assert wd.search("b..") is True
    assert wd.search("....") is False
    print(colored("✓ WordDictionary", "green"))

    print(colored("\nAll tests passed.", "cyan"))
