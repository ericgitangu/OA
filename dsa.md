# Comprehensive Data Structures and Algorithms Overview

## Data Structures Table

| Data Structure                | Description                                                                                                   | Complexity (Common Operations)                                                                 | Best Used For                                          | Not Ideal For                                            | Derived From / Notes                                                      |
|-------------------------------|-----------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|--------------------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------------|
| **Array** (Basic)             | A contiguous block of memory holding elements accessible by index.                                            | Access: O(1), Append: O(1) amortized, Insert/Remove (front/mid): O(n), Search (unsorted): O(n) | Random access, static collections, small lookups        | Frequent insertions/deletions in the middle               | Primitive, forms basis of many structures                  |
| **Linked List** (Basic)       | A linear collection of nodes where each node points to the next (singly) or both next and previous (doubly).  | Insert/Remove at head or tail: O(1), Search: O(n), Random Access: O(n)                          | Insertions/removals at ends, implementing stacks/queues | Fast random access required scenarios                     | Built from nodes and pointers/references                   |
| **Stack** (Basic)             | LIFO structure typically backed by an array or linked list.                                                   | Push/Pop: O(1), Peek: O(1)                                                                     | Function call tracking, undo operations, parsing        | Situations needing random access or non-LIFO traversal     | Often implemented using arrays or linked lists            |
| **Queue** (Basic)             | FIFO structure typically backed by an array or linked list.                                                   | Enqueue/Dequeue: O(1), Peek: O(1)                                                              | Breadth-first search, scheduling tasks                  | Random access or stack-like (LIFO) behaviors              | Often implemented using arrays or linked lists            |
| **Hash Table / Hash Map** (Intermediate) | Stores key-value pairs with O(1) average lookup/insertion via hashing.                                | Insert/Lookup/Remove: O(1) average, O(n) worst case                                            | Fast lookups by key, caching, dictionaries              | Maintaining sorted order, range queries                   | Built on top of arrays + hashing                          |
| **Binary Search Tree (BST)** (Intermediate) | A tree where each node’s left child < node < right child, often balanced to achieve good complexity. | Insert/Lookup/Remove: O(log n) average if balanced, O(n) worst                                 | Ordered data, range queries, maintaining sorted structure | Worst-case skewed trees without balancing                 | Derived from basic tree nodes, often balanced (AVL, Red-Black) |
| **Heap / Priority Queue** (Intermediate) | A binary tree (often represented as an array) that maintains a heap property for quick min/max access. | Get min/max: O(1), Insert: O(log n), Remove top: O(log n)                                      | Priority scheduling, shortest-path algorithms (Dijkstra) | Situations needing full sorting of all elements upfront   | Typically a binary tree represented as an array           |
| **Graph (Adjacency List)** (Intermediate) | Stores nodes and their edges as lists of adjacent vertices.                                             | Add vertex: O(1), Add edge: O(1), Lookup adjacency: O(deg(v))                                   | Sparse graphs, graph algorithms (DFS, BFS, shortest paths) | Dense graphs (use adjacency matrix)                      | Derived from arrays/lists, flexible representation         |
| **Trie (Prefix Tree)** (Advanced) | A tree-based structure for storing strings by character prefixes.                                        | Insert/Lookup (m-length string): O(m), Space: potentially large                                 | Autocomplete, prefix queries, fast lookup of words       | Large memory usage if few words share prefixes            | Specialized tree keyed by characters                      |
| **Balanced BST (AVL/Red-Black)** (Advanced) | Self-balancing BST maintaining O(log n) operations.                                                  | Insert/Lookup/Remove: O(log n)                                                                 | Maintaining sorted data with guaranteed O(log n) ops     | Very simple implementations or constant-time lookups       | Complexity from rotations and balancing strategies         |
| **B-Tree / B+ Tree** (Advanced) | A tree optimized for disk-based or block-based storage, used in databases and filesystems.                 | Insert/Lookup/Remove: O(log n)                                                                 | Database indexing, file systems                         | Small in-memory data sets                                 | Generalization of BST, multi-way branching                |
| **Segment Tree** (Advanced)   | A tree structure for efficient range queries and updates (e.g. sum, min, max over a range).                  | Query/Update: O(log n)                                                                         | Range queries (sum, min, max) with updates              | Scenarios without range queries or updates                | Built atop array-based tree representation                |
| **Fenwick Tree (BIT)** (Advanced) | A structure for cumulative frequencies or prefix sums.                                                  | Update/Prefix query: O(log n)                                                                  | Prefix sum queries, frequency counting                   | Complex operations beyond prefix sums                     | Derived from array, uses clever indexing                  |
| **Disjoint Set (Union-Find)** (Advanced) | Keeps track of elements partitioned into disjoint sets for fast union/find.                           | Union/Find: O(α(n)) (Inverse Ackermann function, very slow-growing)                            | Kruskal’s MST, clustering problems                       | Not for linear order queries, only connected components    | Linked structure with path compression and union by rank   |

---

## Algorithms Table

| Algorithm                     | Genre          | Data Structures Commonly Used    | Complexity (Typical)        | Best Used For                                 | Not Ideal For                                         | Notes                                     |
|-------------------------------|----------------|----------------------------------|-----------------------------|------------------------------------------------|--------------------------------------------------------|-------------------------------------------|
| **Bubble Sort** (Basic)       | Sorting        | Array                            | O(n²)                       | Very small datasets, educational purposes      | Large datasets, performance-critical tasks              | Simple but inefficient                     |
| **Insertion Sort** (Basic)    | Sorting        | Array                            | O(n²), O(n) best case       | Small or partially sorted data                 | Large random datasets                                 | Stable, easy to implement                  |
| **Selection Sort** (Basic)    | Sorting        | Array                            | O(n²)                       | Situations where minimal swaps are needed       | Large datasets                                       | Always O(n²), not stable                   |
| **Merge Sort** (Intermediate) | Sorting        | Array (often split arrays)       | O(n log n)                 | General-purpose sorting                        | Memory-limited or strictly in-place requirements       | Stable, divide-and-conquer                 |
| **Quick Sort** (Intermediate) | Sorting        | Array                            | Average O(n log n), worst O(n²) | General-purpose, often very fast in practice | Worst-case scenarios without good pivot choice         | Not stable, often in-place                 |
| **Binary Search** (Basic)     | Searching      | Sorted Array                     | O(log n)                    | Fast lookups in sorted arrays                  | Unsorted data                                        | Requires sorted data                        |
| **Breadth-First Search (BFS)** (Intermediate) | Graph Traversal | Queue, Graph (Adjacency List) | O(V + E)                   | Shortest paths in unweighted graphs, level-order traversal | Weighted graphs without unit weights       | Explores neighbors first                    |
| **Depth-First Search (DFS)** (Intermediate)    | Graph Traversal | Stack (implicit recursion), Graph (Adjacency List) | O(V + E) | Traversing or searching graph/trees, topological sort | Finding shortest paths in weighted graphs  | Explores depth before breadth              |
| **Dijkstra’s Algorithm** (Advanced) | Shortest Path | Priority Queue (Min-Heap), Graph | O((V+E) log V)             | Single-source shortest paths on weighted graphs | Negative edge weights                              | Efficient with a min-heap                   |
| **Bellman-Ford** (Advanced)   | Shortest Path  | Array/Adjacency List             | O(VE)                       | Graphs with negative edges (no negative cycles) | Very large or dense graphs due to O(VE) complexity   | More flexible than Dijkstra, handles negatives |
| **Floyd-Warshall** (Advanced) | Shortest Path  | Matrix                           | O(V³)                       | All-pairs shortest paths, small dense graphs    | Very large graphs                                   | Easy to implement, high complexity          |
| **Topological Sort** (Intermediate) | Graph Ordering | Graph (Adjacency List), Queue (Kahn’s), Stack (DFS) | O(V + E) | Ordering tasks with dependencies (DAGs)          | Graphs with cycles (not applicable)                 | Requires a DAG                               |
| **Knuth-Morris-Pratt (KMP)** (Intermediate) | String Searching | Array (prefix function)        | O(n + m) (n: text length, m: pattern length)   | Finding a substring pattern efficiently             | Very short patterns or trivial matches      | Precomputes failure function for pattern    |
| **Rabin-Karp** (Intermediate) | String Searching | Rolling Hash (Array)            | Average O(n + m), worst O(nm) | Multiple pattern searches, average fast          | Worst case can degrade to O(nm)                     | Uses hashing to speed pattern matching       |
| **Dynamic Programming (DP)** (Advanced, Family of Techniques) | Optimization/Counting | Arrays/Tables, sometimes Trees/Graphs | Depends on subproblem count and transition cost | Optimal solutions to complex problems via subproblems | Problems without overlapping subproblems or optimal substructure | Approach rather than a single algorithm   |
| **Greedy Algorithms** (Family) | Optimization   | Often arrays, priority queues, sorting | Problem-specific (varies)   | Selecting local optimum at each step (e.g. Huffman coding, interval scheduling) | Problems requiring a global optimum that isn't achieved by local choices | Not one algorithm, but a strategy           |

---

## Data Structure Code Snippets

### Array (Basic)

*Description:* Arrays are fundamental data structures that store elements in contiguous memory locations. In Python, lists serve as dynamic arrays that automatically resize when needed. Key features:
- Backed by contiguous memory blocks for O(1) random access by index
- Dynamic resizing (typically doubles capacity when full) gives amortized O(1) append
- Cache-friendly due to memory locality
- Excellent for random access and iteration
- Supports both primitive types and objects
- Drawbacks include O(n) insertions/deletions in middle due to shifting elements

Common use cases:
- Fast random access to elements
- Iteration over sequential data
- Building blocks for other data structures (stacks, queues, heaps)
- Situations where memory locality matters for performance
- Small to medium collections with mostly reads and appends

```python
    # Create an array and demonstrate O(1) random access
    arr = [1, 2, 3, 4, 5]
    print(arr[3])      # O(1) random access -> prints 4
    
    # Demonstrate O(1) amortized append at end
    arr.append(6)      # Fast append at end
    print(arr)         # [1, 2, 3, 4, 5, 6]
    
    # Demonstrate O(n) insertion in middle requiring shifts
    arr.insert(2, 10)  # Insert at index 2, shifts elements right
    print(arr)         # [1, 2, 10, 3, 4, 5, 6]
    
    # Demonstrate O(n) deletion requiring shifts
    del arr[3]         # Delete at index 3, shifts elements left
    print(arr)         # [1, 2, 10, 4, 5, 6]
    
    # Demonstrate iteration and memory locality
    total = 0
    for x in arr:      # Fast iteration due to memory locality
        total += x
    print(f"Sum: {total}")
    
    # Demonstrate dynamic resizing
    for i in range(10):
        arr.append(i)  # Array will resize automatically when needed
    print(f"Length after growth: {len(arr)}")
```
### Linked List (Basic)

Description: Implementation of a singly linked list demonstrating fundamental linked data structure concepts. Key features:

Data Structures Used:
- Node Class:
  - Contains value field for data storage
  - Contains next pointer for linking to subsequent node
  - Enables O(1) pointer manipulation for insertions/deletions
  - Forms building block for the linked structure

- LinkedList Class:
  - Maintains head pointer to first node
  - Tracks size for O(1) length queries
  - Provides interface for list operations
  - Manages node connections and traversal

Key advantages over arrays:
- O(1) insertions/deletions at known positions
- Dynamic size without resizing/reallocation
- Memory efficiency with no empty spaces
- Easy implementation of stacks/queues

Common applications:
- Implementation of stacks and queues
- Memory allocation systems
- Undo systems in software
- Music playlists
- Browser history

```python
    class Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    class SinglyLinkedList:
        """
        A singly linked list implementation with basic operations.
        Each node contains a value and a pointer to the next node.
        
        Key features:
        - O(1) insertions at head/tail
        - O(n) search and deletion
        - Dynamic size
        - No random access
        """
        def __init__(self):
            self.head = None
            self.size = 0

        def insert_at_head(self, val):
            """Insert a new node at the head in O(1) time"""
            new_node = Node(val)
            new_node.next = self.head
            self.head = new_node
            self.size += 1

        def insert_at_tail(self, val):
            """Insert a new node at the tail in O(n) time"""
            new_node = Node(val)
            if not self.head:
                self.head = new_node
            else:
                current = self.head
                while current.next:
                    current = current.next
                current.next = new_node
            self.size += 1

        def delete(self, val):
            """Delete first occurrence of val in O(n) time"""
            if not self.head:
                return False
                
            if self.head.val == val:
                self.head = self.head.next
                self.size -= 1
                return True
                
            current = self.head
            while current.next:
                if current.next.val == val:
                    current.next = current.next.next
                    self.size -= 1
                    return True
                current = current.next
            return False

        def search(self, val):
            """Search for val in O(n) time"""
            current = self.head
            while current:
                if current.val == val:
                    return True
                current = current.next
            return False

        def get_size(self):
            """Return size of list in O(1) time"""
            return self.size

    # Example usage
    ll = SinglyLinkedList()
    ll.insert_at_head(10)  # List: 10
    ll.insert_at_head(20)  # List: 20->10
    ll.insert_at_tail(30)  # List: 20->10->30
    print(ll.search(10))   # True
    print(ll.search(40))   # False
    print(ll.get_size())   # 3
    ll.delete(10)          # List: 20->30
    print(ll.get_size())   # 2
```

### Stack (Basic)

Description: A Stack is a fundamental data structure that follows Last-In-First-Out (LIFO) ordering. Key features:
- Uses a Python list internally which provides O(1) amortized append/pop operations
- Only allows access to the top element (most recently added)
- Perfect for tracking function calls, undo operations, and parsing expressions
- Common operations:
  - push() - Add element to top
  - pop() - Remove and return top element
  - peek() - View top element without removing
- Memory efficient since elements are stored contiguously
- Can be implemented using arrays or linked lists
- Often used in:
  - Function call stacks
  - Expression evaluation
  - Backtracking algorithms
  - Browser history
  - Undo/Redo operations

The implementation below uses a Python list which automatically handles resizing.

```python
    class Stack:
        """
        A Stack data structure that implements LIFO (Last-In-First-Out) ordering.
        
        Attributes:
            items (list): Internal list to store stack elements
            
        Methods:
            push(item): Add item to top of stack in O(1) time
            pop(): Remove and return top item in O(1) time 
            peek(): Return top item without removing it in O(1) time
            is_empty(): Check if stack is empty in O(1) time
            size(): Return number of items in stack in O(1) time
        """
        def __init__(self):
            self.items = []

        def push(self, item):
            """Add item to top of stack"""
            self.items.append(item)  # O(1)

        def pop(self):
            """Remove and return top item"""
            if self.is_empty():
                raise IndexError("Pop from empty stack")
            return self.items.pop()  # O(1)

        def peek(self):
            """Return top item without removing it"""
            if self.is_empty():
                raise IndexError("Peek at empty stack") 
            return self.items[-1]  # O(1)
            
        def is_empty(self):
            """Check if stack is empty"""
            return len(self.items) == 0  # O(1)
            
        def size(self):
            """Return number of items in stack"""
            return len(self.items)  # O(1)

    # Example usage
    stack = Stack()
    stack.push("function_call_1")  # Simulating function call stack
    stack.push("function_call_2") 
    print(stack.peek())  # "function_call_2"
    print(stack.pop())   # "function_call_2"
    print(stack.pop())   # "function_call_1"
    print(stack.is_empty())  # True
```

### Queue (Basic)

Description: A Queue is a fundamental data structure that follows First-In-First-Out (FIFO) ordering. While it can be implemented using a regular list, Python's collections.deque (double-ended queue) provides a more efficient implementation because:

- Uses a doubly-linked list internally for O(1) operations at both ends
- Optimized for fast appends and pops from either end
- Better than list for queue operations since list.pop(0) is O(n)
- Thread-safe and memory efficient
- Maintains insertion order
- Ideal for breadth-first search, task scheduling, and producer-consumer patterns
- Common operations:
  - append() - Add to right end (enqueue)
  - popleft() - Remove from left end (dequeue) 
  - appendleft() - Add to left end
  - pop() - Remove from right end

The implementation below uses collections.deque which provides all these benefits automatically.

```python
    from collections import deque

    class Queue:
        """
        A Queue data structure that implements FIFO (First-In-First-Out) ordering.
        
        Attributes:
            items (collections.deque): Internal deque to store queue elements
            
        Methods:
            enqueue(item): Add item to end of queue in O(1) time
            dequeue(): Remove and return item from front of queue in O(1) time
            peek(): Return front item without removing it in O(1) time
            is_empty(): Check if queue is empty in O(1) time
            size(): Return number of items in queue in O(1) time
            
        Example:
            >>> q = Queue()
            >>> q.enqueue(1)
            >>> q.enqueue(2) 
            >>> q.dequeue()
            1
            >>> q.peek()
            2
        """
        def __init__(self):
            self.items = deque()
            
        def enqueue(self, item):
            """Add item to end of queue"""
            self.items.append(item)  # O(1)
            
        def dequeue(self):
            """Remove and return item from front of queue"""
            return self.items.popleft() if self.items else None  # O(1)
            
        def peek(self):
            """Return front item without removing it"""
            return self.items[0] if self.items else None  # O(1)
            
        def is_empty(self):
            """Check if queue is empty"""
            return len(self.items) == 0
            
        def size(self):
            """Return number of items in queue"""
            return len(self.items)

    # Example usage showing FIFO behavior
    queue = Queue()
    queue.enqueue(1)  # Add to end
    queue.enqueue(2)  # Add to end
    queue.enqueue(3)  # Add to end
    
    print(queue.dequeue())  # Remove from front -> 1 
    print(queue.peek())     # Look at front -> 2
    print(queue.size())     # Number of items -> 2
```

### Hash Table / Hash Map (Intermediate)

Description: A Hash Table (or Hash Map) is a data structure that implements an associative array abstract data type, a structure that can map keys to values. It uses a hash function to compute an index into an array of buckets/slots, from which the desired value can be found. The main features are:

- Uses key-value pairs for storage
- Hash function converts keys into array indices
- O(1) average time complexity for insertions, deletions and lookups
- Handles collisions through methods like chaining or open addressing
- Python's built-in dict uses open addressing with pseudo-random probing
- Dynamically resizes to maintain performance (load factor)
- Space complexity is O(n) where n is number of key-value pairs
- Not ordered - iteration order is not guaranteed

Python's dictionary is a highly optimized hash table implementation that provides fast, constant-time operations for most use cases while handling collision resolution and dynamic resizing automatically.

```python
    # Create a hash map and demonstrate key operations
    hash_map = {}
    
    # Insertions - O(1) average
    hash_map['name'] = 'Alice'
    hash_map['age'] = 25
    hash_map['city'] = 'New York'
    
    # Lookups - O(1) average
    print(hash_map.get('name'))      # 'Alice'
    print(hash_map.get('invalid'))   # None - key doesn't exist
    
    # Update existing key - O(1)
    hash_map['age'] = 26
    
    # Delete operation - O(1)
    del hash_map['city']
    
    # Check key existence - O(1)
    print('name' in hash_map)        # True
    print('city' in hash_map)        # False
    
    # Get all keys and values
    print(hash_map.keys())           # dict_keys(['name', 'age'])
    print(hash_map.values())         # dict_values(['Alice', 26])
```

### Binary Search Tree (BST) (Intermediate)

Description: A Binary Search Tree (BST) is a hierarchical data structure where each node has at most two children (left and right). The key property is that for any node, all values in its left subtree are less than the node's value, and all values in its right subtree are greater. This ordering enables O(log n) search, insert and delete operations on average when the tree is relatively balanced. However, this implementation shows an unbalanced BST which can degrade to O(n) performance if values are inserted in sorted order (creating a linear chain). The tree uses a node-based structure where each node contains:
- A value
- A left child pointer 
- A right child pointer
This simple structure makes it easy to implement but lacks the self-balancing properties of more advanced trees like AVL or Red-Black trees. The BST is useful for maintaining a sorted collection of data with reasonably fast operations when the data is randomly distributed.

```python
    class BSTNode:
        """
        Binary Search Tree node implementation with basic operations.
        Maintains BST property: left subtree values < node value < right subtree values
        
        Operations:
        - insert: Add new value maintaining BST property 
        - search: Find if value exists in tree
        - delete: Remove value maintaining BST property
        - min/max: Find min/max value in tree
        - inorder: Get values in sorted order
        """
        def __init__(self, val):
            self.val = val
            self.left = None 
            self.right = None
            
        def insert(self, val):
            """Insert value into BST maintaining BST property"""
            if val < self.val:
                if self.left is None:
                    self.left = BSTNode(val)
                else:
                    self.left.insert(val)
            else:
                if self.right is None:
                    self.right = BSTNode(val)
                else:
                    self.right.insert(val)
                    
        def search(self, val):
            """Search for value in BST"""
            if val == self.val:
                return True
            elif val < self.val:
                if self.left is None:
                    return False
                return self.left.search(val)
            else:
                if self.right is None:
                    return False
                return self.right.search(val)
                
        def min_value(self):
            """Get minimum value in BST"""
            current = self
            while current.left:
                current = current.left
            return current.val
            
        def max_value(self):
            """Get maximum value in BST"""
            current = self
            while current.right:
                current = current.right
            return current.val
            
        def inorder(self):
            """Get values in sorted order"""
            result = []
            if self.left:
                result.extend(self.left.inorder())
            result.append(self.val)
            if self.right:
                result.extend(self.right.inorder())
            return result

    # Example usage
    root = BSTNode(5)
    for val in [2, 7, 1, 3, 6, 8]:
        root.insert(val)
        
    print(root.search(3))  # True
    print(root.search(4))  # False
    print(root.min_value())  # 1
    print(root.max_value())  # 8
    print(root.inorder())  # [1, 2, 3, 5, 6, 7, 8]
```

### Heap / Priority Queue (Intermediate)

Description: Implementation of a min-heap (priority queue) using Python's heapq module. Key features:

Data Structures Used:
- List/Array:
  - Stores heap elements in level-order
  - Maintains heap property where parent <= children
  - Enables O(1) access to min element at index 0
  - Allows O(log n) insertions and deletions
  - Provides implicit binary tree structure

- Binary Tree Structure (implicit):
  - For node at index i:
    - Left child at 2i + 1
    - Right child at 2i + 2
    - Parent at (i-1)//2
  - Enables efficient upheap/downheap operations
  - Maintains balanced tree shape

The heap data structure is ideal for:
- Priority queues
- Task scheduling
- Graph algorithms like Dijkstra's
- Event-driven simulations
- Median finding

Key operations and complexities:
- Push: O(log n) - Add element and bubble up
- Pop: O(log n) - Remove min and bubble down  
- Peek: O(1) - Access min element
- Heapify: O(n) - Build heap from array

```python
    import heapq

    # Initialize an empty min-heap
    heap = []

    # Push elements - O(log n) per operation
    heapq.heappush(heap, 5)  
    heapq.heappush(heap, 2)
    heapq.heappush(heap, 7)
    heapq.heappush(heap, 1)
    heapq.heappush(heap, 3)

    # Peek at min element without removing - O(1)
    print(heap[0])  # -> 1

    # Pop min elements - O(log n) per operation
    print(heapq.heappop(heap))  # -> 1
    print(heapq.heappop(heap))  # -> 2
    print(heapq.heappop(heap))  # -> 3

    # Create heap from list in O(n) time
    nums = [4, 1, 7, 3, 8, 5]
    heapq.heapify(nums)  # Converts list to valid heap in-place
    print(nums[0])  # -> 1 (min element)

    # Replace top element - O(log n), more efficient than pop + push
    print(heapq.heapreplace(nums, 6))  # -> 1 (returns old top element)
    print(nums[0])  # -> 3 (new min after replacement)
```

### Graph (Adjacency List) (Intermediate)

Description: Implementation of a graph data structure using an adjacency list representation. Key features:

Data Structures Used:
- Dictionary/Hash Map:
  - Maps vertices to their adjacency lists
  - Provides O(1) vertex lookup
  - Enables efficient edge insertion
  - Dynamically grows as vertices are added

- Adjacency Lists (Arrays):
  - Store neighbors for each vertex
  - Enable O(1) edge insertion
  - Space efficient for sparse graphs
  - Fast iteration over neighbors

Key advantages over adjacency matrix:
- Space efficient O(V + E) vs O(V^2)
- Faster to add vertices
- Better for sparse graphs
- More efficient neighbor iteration

Common applications:
- Social networks
- Road/transportation networks  
- Computer networks
- Web page links
- Dependency graphs

```python
    class Graph:
        """
        Graph implementation using adjacency list representation.
        Supports both directed and undirected graphs.
        
        Operations:
        - add_vertex: Add a new vertex to graph
        - add_edge: Add edge between vertices
        - get_neighbors: Get adjacent vertices
        - has_edge: Check if edge exists
        
        Time Complexity:
        - Adding vertex/edge: O(1) amortized
        - Getting neighbors: O(1)
        - Checking edge: O(degree(v))
        """
        def __init__(self, directed=False):
            self.graph = {}  # Adjacency list
            self.directed = directed
            
        def add_vertex(self, v):
            """Add vertex if it doesn't exist"""
            if v not in self.graph:
                self.graph[v] = []
                
        def add_edge(self, u, v):
            """Add edge from u to v"""
            # Add vertices if they don't exist
            self.add_vertex(u)
            self.add_vertex(v)
            
            # Add edge
            self.graph[u].append(v)
            # If undirected, add reverse edge
            if not self.directed:
                self.graph[v].append(u)
                
        def get_neighbors(self, v):
            """Get list of vertices adjacent to v"""
            return self.graph.get(v, [])
            
        def has_edge(self, u, v):
            """Check if edge exists from u to v"""
            return v in self.graph.get(u, [])

    # Example usage
    g = Graph(directed=True)  # Create directed graph
    
    # Add edges
    g.add_edge(0, 1)
    g.add_edge(0, 2) 
    g.add_edge(1, 2)
    
    # Check graph structure
    print(g.graph)  # {0: [1, 2], 1: [2], 2: []}
    print(g.get_neighbors(0))  # [1, 2]
    print(g.has_edge(0, 2))  # True
    print(g.has_edge(2, 0))  # False (directed)
```

### Trie (Prefix Tree) (Advanced)

Description: A Trie (also called prefix tree) is an efficient tree-like data structure for storing and retrieving strings. Key features:

Data Structures Used:
- TrieNode Class:
  - Dictionary/Hash Map for children: Enables O(1) access to child nodes
  - Boolean flag for word endings: Marks complete words
  - Integer counter for prefix frequency: Tracks usage statistics
  - Forms tree structure through node linking

- Trie Class:
  - Root node as entry point
  - Methods for insertion and search
  - Maintains tree invariants

Key advantages over other string storage:
- O(m) lookup time where m is string length
- Space-efficient for common prefixes
- Prefix-based operations like autocomplete
- No hash collisions unlike hash tables

Common applications:
- Autocomplete/type-ahead features
- Spell checkers
- IP routing tables
- Dictionary implementations
- Phone directories

```python
    class TrieNode:
        """
        A node in the Trie data structure.
        
        Attributes:
            children: Dict mapping characters to child TrieNodes
            end_of_word: Boolean flag marking if node represents end of valid word
            count: Number of words containing the prefix represented by this node
            
        The TrieNode forms the building block of a Trie, storing:
        - Links to child nodes in a map for O(1) access
        - Flag to mark complete words
        - Count to track frequency of prefixes
        """
        def __init__(self):
            """Initialize a trie node with empty children map and word flag"""
            self.children = {}  # Map from char to TrieNode
            self.end_of_word = False  # Flag to mark end of valid word
            self.count = 0  # Track frequency of words with this prefix

    class Trie:
        def __init__(self):
            """Initialize an empty trie with just a root node"""
            self.root = TrieNode()

        def insert(self, word):
            """
            Insert a word into the trie
            Time: O(m) where m is word length
            Space: O(m) for new nodes
            """
            current = self.root
            # Traverse/create path for each character
            for ch in word:
                if ch not in current.children:
                    current.children[ch] = TrieNode()
                current = current.children[ch]
                current.count += 1  # Increment prefix count
            current.end_of_word = True

        def search(self, word):
            """
            Search for exact word in trie
            Time: O(m) where m is word length
            """
            current = self.root
            for ch in word:
                if ch not in current.children:
                    return False
                current = current.children[ch]
            return current.end_of_word

        def starts_with(self, prefix):
            """
            Check if any word starts with given prefix
            Time: O(p) where p is prefix length
            """
            current = self.root
            for ch in prefix:
                if ch not in current.children:
                    return False
                current = current.children[ch]
            return True

        def count_prefix(self, prefix):
            """
            Count words that start with given prefix
            Time: O(p) where p is prefix length
            """
            current = self.root
            for ch in prefix:
                if ch not in current.children:
                    return 0
                current = current.children[ch]
            return current.count

    # Example usage
    trie = Trie()
    words = ["apple", "app", "apricot", "bear", "bet"]
    for word in words:
        trie.insert(word)
        
    print(trie.search("apple"))     # True
    print(trie.search("app"))       # True
    print(trie.search("appl"))      # False
    print(trie.starts_with("app"))  # True
    print(trie.count_prefix("app")) # 2 - "apple" and "app"
```

### Balanced BST (AVL/Red-Black) (Advanced)

Description: AVL trees are self-balancing binary search trees where the heights of the left and right subtrees of any node differ by at most one. Key features:
- Uses height-balanced property to ensure O(log n) operations
- Each node stores a balance factor = height(left) - height(right)
- When balance factor becomes > 1 or < -1, rotations restore balance
- Maintains sorted order for efficient searching
- More strictly balanced than Red-Black trees, so better search but more expensive updates
- Common in memory-based applications needing fast lookups

The example below shows basic node structure and insertion without rotations. Full implementation requires:
- Balance factor tracking
- Left and right rotations
- Left-Right and Right-Left double rotations
- Height updates after modifications

```python
class AVLNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1

# Full AVL operations including rotations are complex; 
# This snippet only shows structure setup for demonstration.

```python
    def avl_insert(root, val):
        # Insert like BST
        if root is None:
            return AVLNode(val)
        if val < root.val:
            root.left = avl_insert(root.left, val)
        else:
            root.right = avl_insert(root.right, val)
        # Normally update height and balance factor, then rotate if needed
        return root

    root_avl = None
    for v in [10, 20, 30]:
        root_avl = avl_insert(root_avl, v)

    # Here's a complete AVL implementation with rotations:

    def get_height(node):
        """Get height of node, handling None case"""
        if not node:
            return 0
        return node.height

    def get_balance(node):
        """Get balance factor of node (left height - right height)"""
        if not node:
            return 0
        return get_height(node.left) - get_height(node.right)

    def update_height(node):
        """Update height of node based on children"""
        if node:
            node.height = max(get_height(node.left), get_height(node.right)) + 1

    def right_rotate(y):
        """Perform right rotation
           y                    x
          / \                 /   \
         x   T3   -->       T1    y
        / \                      /  \
       T1  T2                  T2   T3
        """
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        # Update heights bottom-up
        update_height(y)
        update_height(x)

        return x

    def left_rotate(x):
        """Perform left rotation
           x                    y
          / \                 /   \
         T1  y     -->      x     T3
            / \            / \
           T2  T3        T1  T2
        """
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        # Update heights bottom-up
        update_height(x)
        update_height(y)

        return y

    def avl_insert_with_balance(root, val):
        """Insert value into AVL tree while maintaining balance
        Returns new root after any necessary rotations"""

        # Standard BST insert
        if not root:
            return AVLNode(val)

        # Recursively insert into appropriate subtree
        if val < root.val:
            root.left = avl_insert_with_balance(root.left, val)
        elif val > root.val:
            root.right = avl_insert_with_balance(root.right, val)
        else:
            return root  # Duplicate values not allowed

        # Update height of current node
        update_height(root)

        # Get balance factor to check if rebalancing needed
        balance = get_balance(root)

        # Left Left Case: Single right rotation
        if balance > 1 and val < root.left.val:
            return right_rotate(root)

        # Right Right Case: Single left rotation
        if balance < -1 and val > root.right.val:
            return left_rotate(root)

        # Left Right Case: Left rotation then right rotation
        if balance > 1 and val > root.left.val:
            root.left = left_rotate(root.left)
            return right_rotate(root)

        # Right Left Case: Right rotation then left rotation
        if balance < -1 and val < root.right.val:
            root.right = right_rotate(root.right)
            return left_rotate(root)

        return root

    # Example usage showing tree balancing:
    root = None
    values = [10, 20, 30, 40, 50, 25]  # Would cause right-heavy imbalance without AVL
    print("Inserting values:", values)
    for val in values:
        root = avl_insert_with_balance(root, val)
        print(f"Inserted {val}, root is now {root.val}")
```

### B-Tree / B+ Tree (Advanced)

Description: B-Trees are self-balancing search trees designed for efficient disk access and database operations. Unlike binary trees, a B-Tree node can have multiple keys and children. Key features:
- Each node can have M-1 keys and M children (where M is the order/degree)
- All leaves are at the same level (perfect balance)
- Nodes are typically sized to match disk blocks for I/O efficiency
- Great for databases and file systems due to reduced disk seeks
- Maintains sorted data for range queries
- Guarantees O(log n) operations even with large datasets

The implementation below shows a simplified node structure, though actual B-Tree operations like insertion and deletion require careful handling of node splits and merges to maintain the B-Tree properties.

```python
    class BTreeNode:
        def __init__(self, t):
            """Initialize B-Tree node with minimum degree t"""
            self.t = t  # Minimum degree
            self.keys = []  # List of keys
            self.children = []  # List of child nodes
            self.leaf = True  # Is this a leaf node
            self.n = 0  # Current number of keys

    class BTree:
        def __init__(self, t):
            """Initialize empty B-Tree with minimum degree t"""
            self.root = BTreeNode(t)
            self.t = t

        def search(self, k):
            """Search for key k in the B-Tree"""
            return self._search_recursive(self.root, k)
            
        def _search_recursive(self, x, k):
            """Helper method to recursively search for key k"""
            i = 0
            # Find the first key greater than or equal to k
            while i < x.n and k > x.keys[i]:
                i += 1
                
            # If we found the key
            if i < x.n and k == x.keys[i]:
                return (x, i)
                
            # If we're at a leaf, key not found
            if x.leaf:
                return None
                
            # Recurse to appropriate child
            return self._search_recursive(x.children[i], k)

        def insert(self, k):
            """Insert key k into the B-Tree"""
            root = self.root
            
            # Handle root splitting
            if root.n == (2 * self.t) - 1:
                new_root = BTreeNode(self.t)
                new_root.leaf = False
                new_root.children.append(self.root)
                self._split_child(new_root, 0)
                self.root = new_root
                
            self._insert_non_full(self.root, k)

    # Example usage
    btree = BTree(t=3)  # Create B-Tree with minimum degree 3
    # Insert some keys
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    for k in keys:
        btree.insert(k)
        
    # Search for keys
    print(btree.search(6) is not None)  # True
    print(btree.search(15) is not None)  # False
```

### Segment Tree (Advanced)

Description: Constructing a segment tree for range sum queries.

```python
    class SegmentTree:
        """
        A segment tree data structure that supports:
        - Range queries in O(log n) time
        - Point updates in O(log n) time
        - Space complexity O(4n)
        
        Implementation details:
        - Uses array representation of binary tree
        - Each node stores sum of its range
        - Parent node at index i has children at 2i and 2i+1
        - Leaf nodes contain actual array values
        """
        def __init__(self, arr):
            self.n = len(arr)
            # Tree array needs 4n space to handle all cases
            self.tree = [0] * (4 * self.n)
            if self.n > 0:
                self._build_tree(arr, 0, self.n-1, 1)
        
        def _build_tree(self, arr, start, end, node):
            """Recursively build segment tree from input array"""
            # Base case - leaf node
            if start == end:
                self.tree[node] = arr[start]
                return self.tree[node]
            
            # Recursively build left and right subtrees
            mid = (start + end) // 2
            left_sum = self._build_tree(arr, start, mid, 2*node)
            right_sum = self._build_tree(arr, mid+1, end, 2*node+1)
            
            # Internal node stores sum of children
            self.tree[node] = left_sum + right_sum
            return self.tree[node]
            
        def range_sum(self, left, right):
            """Get sum of elements from index left to right inclusive"""
            if left < 0 or right >= self.n:
                raise ValueError("Range out of bounds")
            return self._range_sum_util(0, self.n-1, left, right, 1)
            
        def _range_sum_util(self, start, end, left, right, node):
            """Helper method for range sum query"""
            # No overlap
            if right < start or left > end:
                return 0
                
            # Complete overlap
            if left <= start and right >= end:
                return self.tree[node]
                
            # Partial overlap - recurse on children
            mid = (start + end) // 2
            return (self._range_sum_util(start, mid, left, right, 2*node) + 
                   self._range_sum_util(mid+1, end, left, right, 2*node+1))

    # Example usage
    arr = [1, 2, 3, 4, 5]
    seg_tree = SegmentTree(arr)
    print(seg_tree.range_sum(1, 3))  # Sum of arr[1..3] = 2+3+4 = 9
    print(seg_tree.range_sum(0, 4))  # Sum of entire array = 15

```

### Fenwick Tree (BIT) (Advanced)

Description: A Fenwick Tree (Binary Indexed Tree) is a space-efficient data structure that provides efficient methods for calculating prefix sums in a dynamic array. 

Data Structures Used:
- Array/List as Primary Structure:
  - Stores partial sums in a flat array format
  - Uses 1-based indexing for simpler arithmetic
  - Requires only O(n) space vs O(4n) for segment trees
  - Enables O(log n) updates and queries through binary arithmetic
  - More cache-friendly than pointer-based trees

- Binary Number Properties:
  - Leverages binary representation of indices
  - Uses least significant bit (LSB) for tree traversal
  - Each index i covers range of size LSB(i)
  - Parent/child relationships implicit in binary form
  - No explicit pointers needed between nodes

Key advantages over other structures:
- More memory efficient than segment trees
- Simpler implementation than other range query structures  
- Cache-friendly array-based storage
- Fast O(log n) updates and queries
- No pointer overhead or complex tree maintenance

Common applications:
- Range sum queries in dynamic arrays
- Cumulative frequency tables
- Count of inversions in an array
- Rectangle sum queries in 2D arrays
- Dynamic ranking systems

The structure achieves its efficiency by using a clever binary representation technique where each index i is responsible for storing the sum of elements determined by its rightmost set bit. Updates and queries traverse the implicit tree structure using bitwise operations (i & -i) to efficiently move between levels. This binary arithmetic approach eliminates the need for explicit parent-child pointers while maintaining O(log n) performance.

```python
    class FenwickTree:
        """
        A Fenwick Tree (Binary Indexed Tree) data structure that supports:
        - Point updates in O(log n) time
        - Range sum queries in O(log n) time
        - Space efficient O(n) storage
        
        Key operations:
        - update(i, delta): Add delta to element at index i
        - prefix_sum(i): Get sum of elements from 1 to i
        - range_sum(l, r): Get sum of elements from l to r
        - get(i): Get value at index i
        - set(i, val): Set value at index i
        
        Implementation details:
        - Uses 1-based indexing internally
        - Leverages binary arithmetic (i & -i) for tree traversal
        - Each node implicitly stores partial sums based on binary representation
        - More space efficient than segment tree (n vs 4n nodes)
        """
        def __init__(self, n):
            """Initialize Fenwick tree with size n"""
            self.size = n
            self.fw = [0] * (n + 1)  # 1-based indexing
            
        def update(self, i, delta):
            """Add delta to element at index i
            Time complexity: O(log n)
            """
            if i <= 0 or i > self.size:
                raise ValueError("Index out of bounds")
            while i <= self.size:
                self.fw[i] += delta
                i += i & (-i)  # Add least significant bit
                
        def prefix_sum(self, i):
            """Get sum of elements from index 1 to i inclusive
            Time complexity: O(log n)
            """
            if i <= 0:
                return 0
            if i > self.size:
                i = self.size
            total = 0
            while i > 0:
                total += self.fw[i]
                i -= i & (-i)  # Remove least significant bit
            return total
            
        def range_sum(self, left, right):
            """Get sum of elements from index left to right inclusive"""
            if left > right:
                raise ValueError("Left bound larger than right bound")
            return self.prefix_sum(right) - self.prefix_sum(left - 1)
            
        def get(self, i):
            """Get value at index i"""
            return self.range_sum(i, i)
            
        def set(self, i, val):
            """Set value at index i"""
            delta = val - self.get(i)
            self.update(i, delta)

    # Example usage showing key operations
    arr = [1, 2, 3, 4, 5]
    ft = FenwickTree(len(arr))
    
    # Build tree from array
    for i, val in enumerate(arr, 1):  # 1-based indexing
        ft.update(i, val)
        
    print(ft.prefix_sum(3))  # Sum of first 3 elements: 6
    print(ft.range_sum(2, 4))  # Sum of elements 2-4: 9
    ft.set(2, 10)  # Change value at index 2 to 10
    print(ft.range_sum(2, 4))  # New sum of elements 2-4: 17
```

### Disjoint Set (Union-Find) (Advanced)

Description: Union-Find (also known as Disjoint Set) is a data structure that efficiently tracks disjoint (non-overlapping) sets of elements. It uses several key data structures working together:

Data Structures Used:
- Array/List for Parent Pointers:
  - Maps each element to its parent element
  - Forms tree structure implicitly through indices
  - Enables O(1) access to parent nodes
  - Path compression updates these pointers to root

- Array/List for Ranks:
  - Tracks approximate height/depth of each tree
  - Used to keep trees balanced during unions
  - Prevents degenerate linear chains
  - Critical for O(log n) height bound

- Array/List for Set Sizes:
  - Maintains count of elements in each set
  - Enables O(1) size queries
  - Useful for keeping sets balanced
  - Updated during union operations

The data structure maintains a forest of trees where each tree represents a set, with two key optimizations:

1. Path Compression:
   - During find operations, updates parent pointers to point directly to root
   - Flattens tree structure over time
   - Reduces future traversal costs
   - Critical for amortized near-constant time

2. Union by Rank:
   - Attaches shorter tree under root of taller tree
   - Prevents trees from becoming too deep
   - Maintains logarithmic height bound
   - Works with path compression for efficiency

This combination makes it extremely efficient for:
- Finding connected components in graphs
- Detecting cycles in graphs
- Tracking equivalence classes
- Implementing Kruskal's MST algorithm

The structure achieves nearly O(1) amortized time complexity for both union and find operations through the synergy of these optimizations and data structures.

```python
    class UnionFind:
        """
        A data structure for efficiently managing disjoint sets of elements.
        
        Key features:
        - Uses path compression and union by rank optimizations
        - Near O(1) amortized time for operations
        - Tracks set sizes and total number of disjoint sets
        - Perfect for connectivity problems and finding connected components
        
        Operations:
        - find(x): Find set representative for element x 
        - union(x,y): Merge sets containing x and y
        - connected(x,y): Check if x and y are in same set
        - get_size(x): Get size of set containing x
        
        Time Complexity:
        - All operations are O(α(n)) amortized, where α is inverse Ackermann
        - For practical purposes, O(1) since α(n) ≤ 4 for all reasonable n
        
        Space Complexity: O(n) to store parent pointers and ranks
        """
        def __init__(self, n):
            """Initialize disjoint set with n elements"""
            self.parent = list(range(n))  # Each element starts as its own parent
            self.rank = [0] * n  # Track tree heights for union by rank
            self.size = [1] * n  # Track size of each set
            self.count = n  # Number of disjoint sets

        def find(self, x):
            """Find set representative with path compression"""
            if self.parent[x] != x:
                # Recursively set parent to root and compress path
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x, y):
            """Union two sets by rank"""
            rx, ry = self.find(x), self.find(y)
            if rx == ry:
                return False  # Already in same set
                
            # Union by rank - attach smaller rank tree under root of higher rank tree
            if self.rank[rx] < self.rank[ry]:
                rx, ry = ry, rx
            self.parent[ry] = rx
            self.size[rx] += self.size[ry]
            
            # If same rank, increment rank of root
            if self.rank[rx] == self.rank[ry]:
                self.rank[rx] += 1
                
            self.count -= 1  # Decrease number of disjoint sets
            return True

        def connected(self, x, y):
            """Check if two elements are in the same set"""
            return self.find(x) == self.find(y)
            
        def get_size(self, x):
            """Get size of set containing element x"""
            return self.size[self.find(x)]

    # Example usage showing key operations
    uf = UnionFind(5)
    print(uf.connected(0, 1))  # False - different sets initially
    uf.union(0, 1)  # Union first two elements
    uf.union(2, 3)  # Union next two elements
    print(uf.connected(0, 1))  # True - now connected
    print(uf.get_size(0))  # 2 - size of set containing 0
    print(uf.count)  # 3 - three disjoint sets remain
```

## Algorithm Code Snippets
### Bubble Sort (Basic)

Description: Bubble sort is a simple comparison-based sorting algorithm that demonstrates fundamental sorting concepts. Key features:

Data Structures Used:
- Array/List as Primary Structure:
  - Stores elements to be sorted in contiguous memory
  - Enables O(1) access to adjacent elements for comparisons
  - Modified in-place without auxiliary storage
  - Maintains stable ordering of equal elements
  - Size remains fixed during sorting

- Boolean Flag for Optimization:
  - Tracks if any swaps occurred in a pass
  - Enables early termination if array is sorted
  - Improves best case to O(n) for nearly sorted arrays
  - Simple but effective optimization technique

Key advantages:
- Simple implementation with minimal extra space O(1)
- Stable sorting preserves relative order
- Works well for small or nearly sorted arrays
- Can detect sorted arrays early
- Good for teaching sorting concepts

Limitations:
- O(n²) time complexity makes it inefficient for large arrays
- Requires many array accesses and swaps
- Not suitable for large datasets
- Other algorithms like quicksort are usually better

The algorithm gets its name from the way smaller elements "bubble up" to their correct positions with each pass through the array. While not efficient for large datasets, it remains useful for:
- Educational purposes demonstrating sorting concepts
- Small arrays where simplicity is preferred
- Nearly sorted arrays that need minor corrections
- When stable sorting is required with minimal space

```python
    def bubble_sort(arr):
        """
        Sorts array in-place using bubble sort algorithm by:
        1. Making multiple passes through array
        2. Comparing adjacent elements and swapping if out of order
        3. Optimizing by stopping if no swaps needed (array is sorted)
        Time: O(n²), Space: O(1)
        """
        n = len(arr)
        for i in range(n):
            # Flag to detect if any swaps happened in this pass
            swapped = False
            
            # Last i elements are already in place
            for j in range(n - i - 1):
                # Compare adjacent elements
                if arr[j] > arr[j + 1]:
                    # Swap them if they are in wrong order
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    
            # If no swapping occurred, array is already sorted
            if not swapped:
                break

    # Example showing algorithm's behavior
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", data)
    bubble_sort(data)
    print("Sorted array:", data)  # [11, 12, 22, 25, 34, 64, 90]

    # Test with different input patterns
    nearly_sorted = [1, 2, 4, 3, 5]  # Nearly sorted - best case
    bubble_sort(nearly_sorted)
    print("Nearly sorted case:", nearly_sorted)  # [1, 2, 3, 4, 5]

    reverse_sorted = [5, 4, 3, 2, 1]  # Worst case
    bubble_sort(reverse_sorted)
    print("Reverse sorted case:", reverse_sorted)  # [1, 2, 3, 4, 5]
```

### Insertion Sort (Basic)

Description: Insertion sort is a simple sorting algorithm that builds a sorted portion of the array one element at a time. Key features:

Data Structures Used:
- Array/List:
  - Primary data structure that is sorted in-place
  - Maintains sorted portion at beginning
  - Unsorted portion follows sorted portion
  - Enables O(1) access for comparisons and swaps
  - No extra space needed beyond input array

- Temporary Variable:
  - Stores current element being inserted
  - Enables shifting of elements without losing value
  - Acts as swap space during insertions

The algorithm is ideal for:
- Small arrays/lists
- Nearly sorted data
- Online sorting (processing elements as they arrive)
- Linked list sorting due to local swaps

Key advantages:
- O(1) extra space - sorts in place
- O(n) best case for nearly sorted arrays
- Stable sort - maintains relative order of equal elements
- Simple implementation
- Adaptive - runs faster on partially sorted arrays

```python
    def insertion_sort(arr):
        """
        Builds sorted portion of array one element at a time by:
        1. Taking next unsorted element
        2. Shifting larger sorted elements right
        3. Inserting element in correct position
        Time: O(n²), Space: O(1)
        """
        # Iterate through array starting from second element
        for i in range(1, len(arr)):
            # Store current element to insert
            key = arr[i]
            # Start comparing with previous sorted elements
            j = i - 1
            
            # Shift elements right while they're larger than key
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            
            # Insert key in correct position
            arr[j + 1] = key

    # Example showing algorithm's behavior
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", data)
    insertion_sort(data)
    print("Sorted array:", data)  # [11, 12, 22, 25, 34, 64, 90]

    # Test with different input patterns
    nearly_sorted = [1, 2, 4, 3, 5]  # Nearly sorted
    insertion_sort(nearly_sorted)
    print("Nearly sorted case:", nearly_sorted)  # [1, 2, 3, 4, 5]

    reverse_sorted = [5, 4, 3, 2, 1]  # Worst case
    insertion_sort(reverse_sorted)
    print("Reverse sorted case:", reverse_sorted)  # [1, 2, 3, 4, 5]
```

### Selection Sort (Basic)

Description: Selection sort is an in-place comparison sorting algorithm that relies on several key data structures and properties:

Data Structures Used:
- Input Array:
  - Serves as both input and output storage
  - Divided conceptually into sorted and unsorted regions
  - Modified in-place through swapping
  - Enables O(1) access to elements
  - No extra space needed beyond input array
  - Size remains constant throughout sorting

- Two Logical Regions:
  - Sorted Region (Left Side):
    - Grows from left to right
    - Contains elements in final sorted order
    - Elements never move once placed
    - Size increases by 1 each iteration
  
  - Unsorted Region (Right Side):
    - Shrinks from right to left
    - Contains remaining elements to sort
    - Scanned fully to find each minimum
    - Size decreases by 1 each iteration

Key Properties:
- In-Place: Uses O(1) extra space by modifying input array directly
- Unstable: Can change relative order of equal elements through swapping
- Quadratic Time: O(n²) in all cases due to nested loops
- Simple Implementation: Uses basic array operations only
- Not Adaptive: Running time independent of input order
- Minimal Memory Writes: O(n) swaps vs O(n²) comparisons

```python
    def selection_sort(arr):
        """
        In-place comparison sorting algorithm that:
        1. Divides array into sorted and unsorted regions
        2. Repeatedly finds minimum from unsorted region
        3. Swaps it with first unsorted element
        Time: O(n²), Space: O(1)
        """
        n = len(arr)
        # Iterate through array, growing sorted region
        for i in range(n):
            # Find minimum element in unsorted region
            min_idx = i
            for j in range(i+1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            # Swap minimum with first unsorted element
            # Only swap if needed to minimize operations
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]

    # Example showing algorithm's behavior
    data = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", data)
    selection_sort(data)
    print("Sorted array:", data)  # [11, 12, 22, 25, 34, 64, 90]
    print(data) # [1,2,3]
```

### Merge Sort (Intermediate)

Description: Merge sort is a divide-and-conquer sorting algorithm that relies on several key data structures and properties:

Data Structures Used:
- Input Array:
  - Stores original unsorted data
  - Divided into subarrays during recursion
  - Modified in-place during merging
  - Enables O(1) access to elements

- Temporary Arrays (Left/Right):
  - Created during merge step
  - Store sorted subarrays temporarily
  - Enable stable merging of elements
  - Total O(n) extra space required
  - Freed after each merge completes

- Recursion Stack:
  - Implicitly tracks subproblems
  - Stores local variables and return addresses
  - Maximum depth O(log n)
  - Enables divide-and-conquer strategy

Key Properties:
- Stability: Preserves relative order of equal elements by using <= in merge
- Parallelizable: Subarrays can be sorted independently
- Cache-friendly: Sequential access patterns during merge
- External sort friendly: Can efficiently merge sorted files

Time/Space Analysis:
- Time: O(n log n) guaranteed
  - log n levels of recursion
  - O(n) work per level during merges
- Space: O(n) auxiliary space
  - O(n) for temporary arrays
  - O(log n) for recursion stack

Ideal Use Cases:
- Sorting linked lists (no random access needed)
- External sorting of large files
- When stable sorting is required
- When predictable performance matters more than space

```python
    def merge(arr, left, right):
        """
        Merges two sorted arrays into a single sorted array.
        Uses two pointers to track positions in subarrays being merged.
        """
        i = j = k = 0
        
        # Compare elements from both arrays and merge in sorted order
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:  # Use <= for stability
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j] 
                j += 1
            k += 1
            
        # Copy remaining elements from left array, if any
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            
        # Copy remaining elements from right array, if any    
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    def merge_sort(arr):
        """
        Divide-and-conquer sorting algorithm that:
        1. Divides array into two halves
        2. Recursively sorts the halves 
        3. Merges sorted halves using auxiliary arrays
        Time: O(n log n), Space: O(n)
        """
        if len(arr) <= 1:  # Base case
            return
            
        # Divide array into two halves    
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        # Recursively sort the halves
        merge_sort(left)
        merge_sort(right)

        # Merge sorted halves
        merge(arr, left, right)

    # Example usage showing divide-and-conquer and stability
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5]
    merge_sort(data)
    print(data)  # [1, 1, 2, 3, 4, 5, 5, 6, 9]
```

### Quick Sort (Intermediate)

Description: Quick sort is a highly efficient, in-place sorting algorithm that uses a divide-and-conquer strategy. 

Data Structures Used:
- Input Array:
  - Used directly for in-place sorting without auxiliary storage
  - Enables O(1) swaps between elements
  - Provides good cache locality during partitioning
  - Allows random access for efficient pivoting

- Call Stack:
  - Implicitly used for recursive calls
  - Stores function parameters and local variables
  - Enables divide-and-conquer by tracking subproblems
  - Depth is O(log n) on average, O(n) worst case

- Two Pointers:
  - Left and right indices scan array during partition
  - Enable efficient element comparison and swapping
  - Help maintain partition invariants
  - Allow in-place partitioning without extra space

Key advantages of these structures:
- In-place sorting saves memory
- Good cache performance from array locality
- Minimal auxiliary space needed
- Efficient element swapping

The algorithm works by selecting a 'pivot' element and partitioning the array around it, such that smaller elements go to the left and larger elements go to the right. The partition operation uses the two pointers to scan the array from both ends, swapping elements when necessary.

Time complexity:
- Average case: O(n log n) - balanced partitions
- Worst case: O(n²) - poorly balanced partitions (e.g. sorted array)

Space complexity:
- Average case: O(log n) - recursive call stack depth
- Worst case: O(n) - unbalanced recursion

Quick sort is widely used in practice due to its excellent cache performance from in-place sorting and generally good average case performance. The choice of pivot strategy can significantly impact performance.

```python
    def partition(arr, low, high):
        """
        Partitions array around a pivot using two-pointer technique.
        Returns final pivot position.
        """
        # Choose rightmost element as pivot
        pivot = arr[high]
        i = low - 1  # Index of smaller element
        
        # Move elements smaller than pivot to left side
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                
        # Place pivot in correct position
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quick_sort_helper(arr, low, high):
        """
        Recursive helper that sorts array in-place using partitioning.
        """
        if low < high:
            # Get pivot position after partitioning
            pivot_idx = partition(arr, low, high)
            
            # Recursively sort elements before and after pivot
            quick_sort_helper(arr, low, pivot_idx - 1)
            quick_sort_helper(arr, pivot_idx + 1, high)

    def quick_sort(arr):
        """
        Main quicksort function that sorts array in-place.
        """
        quick_sort_helper(arr, 0, len(arr) - 1)
        return arr

    # Example usage showing different cases
    data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    quick_sort(data)
    print(data)  # [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
```

### Binary Search (Basic)

Description: Binary search is an efficient search algorithm that works on sorted arrays by repeatedly dividing the search interval in half. 

Data Structures Used:
- Sorted Array:
  - Primary data structure that enables O(1) random access
  - Must be sorted to allow eliminating half the search space
  - Enables comparison-based decisions at each step
  - Supports efficient memory access patterns
  - Common implementations use arrays/lists

- Three Pointers:
  - Low: Tracks start of current search range
  - Mid: Divides range for comparison with target
  - High: Tracks end of current search range
  - Together enable O(1) space complexity
  - Allow efficient range manipulation

The algorithm compares the middle element with the target: if equal, we've found it; if target is greater, we search the right half; if smaller, we search the left half. This divide-and-conquer approach gives binary search a time complexity of O(log n), making it much faster than linear search O(n) for large datasets.

Key advantages:
- O(log n) time complexity through halving
- O(1) space as only pointers needed
- Cache-friendly array access pattern
- Highly efficient for large sorted datasets

Common applications:
- Dictionary/phone book lookups
- Database indexing and queries
- Finding insertion points
- Root finding algorithms
- Package version resolution

The key requirement is that the input array must be sorted, as the algorithm relies on the ordering to eliminate half the remaining elements in each step. This makes binary search ideal for frequently searched but rarely modified data.

```python
    def binary_search(arr, target):
        """
        Performs binary search to find target in a sorted array.
        Args:
            arr: Sorted array to search in
            target: Value to find
        Returns:
            Index of target if found, -1 if not found
        """
        # Initialize pointers to track search range
        low = 0
        high = len(arr) - 1
        
        # Keep searching while valid range exists
        while low <= high:
            # Find middle element
            mid = low + (high - low) // 2  # Prevents integer overflow
            
            # Check if middle element is target
            if arr[mid] == target:
                return mid
                
            # If target is greater, ignore left half
            elif arr[mid] < target:
                low = mid + 1
                
            # If target is smaller, ignore right half
            else:
                high = mid - 1
                
        # Target not found
        return -1

    # Example usage showing different cases
    sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(binary_search(sorted_arr, 1))   # 0 (first element)
    print(binary_search(sorted_arr, 5))   # 4 (middle element) 
    print(binary_search(sorted_arr, 10))  # 9 (last element)
    print(binary_search(sorted_arr, 11))  # -1 (not found)
```

### Breadth-First Search (BFS) (Intermediate)

Description: BFS (Breadth-First Search) is a fundamental graph traversal algorithm that uses two key data structures:

Data Structures Used:
- Queue (collections.deque):
  - Stores nodes to be processed in FIFO order
  - O(1) enqueue/dequeue operations
  - Naturally creates level-by-level traversal
  - Maintains frontier between explored and unexplored nodes
  - Typically implemented with collections.deque for efficiency
  - Size is O(V) in worst case for complete graphs

- Visited Set (Hash Set):
  - Tracks already explored nodes
  - O(1) lookups to check for visited nodes
  - Prevents cycles and re-processing
  - Essential for graphs with cycles
  - Implemented as hash table/set for efficiency
  - Size is O(V) to store all vertices

The algorithm works by:
1. Starting from source node, add to queue and visited set
2. While queue not empty:
   - Dequeue next node to process
   - Add all unvisited neighbors to queue and visited set
3. Queue ensures level-by-level traversal
4. Visited set prevents cycles

Key advantages of this approach:
- Guarantees shortest path in unweighted graphs
- Visits nodes in order of distance from source
- Memory efficient O(V) space complexity
- Handles disconnected components if needed
- Natural for level-order tree traversal

Time complexity is O(V + E) since we:
- Visit each vertex once O(V)
- Explore each edge once O(E)
Space complexity is O(V) for both queue and visited set.

```python
    from collections import deque

    def bfs(graph, start):
        """
        Performs breadth-first search traversal of a graph starting from given node.
        Args:
            graph: Dictionary representing adjacency list of graph
            start: Starting vertex for traversal
        Returns:
            List of nodes in BFS traversal order
        """
        # Initialize visited set and queue with start node
        visited = set([start])
        queue = deque([start])
        traversal = []  # Track traversal order
        
        # Process nodes level by level using queue
        while queue:
            # Get next node from front of queue
            current = queue.popleft()
            traversal.append(current)
            
            # Add unvisited neighbors to queue
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        return traversal

    # Example usage:
    # Graph represented as adjacency list
    graph = {
        0: [1, 2],     # Node 0 connected to 1,2
        1: [2, 3],     # Node 1 connected to 2,3  
        2: [3, 4],     # Node 2 connected to 3,4
        3: [4],        # Node 3 connected to 4
        4: []          # Node 4 has no outgoing edges
    }

    # Perform BFS from node 0
    result = bfs(graph, 0)
    print(result)  # [0, 1, 2, 3, 4]
```

### Depth-First Search (DFS) (Intermediate)

Description: DFS (Depth-First Search) is a graph traversal algorithm that explores a graph by going as deep as possible along each branch before backtracking.

Data Structures Used:
- Stack (Implicit or Explicit):
  - Handles Last-In-First-Out (LIFO) order needed for backtracking
  - Recursive implementation uses call stack implicitly
  - Iterative version uses explicit stack data structure
  - Enables O(1) push/pop operations for tracking path
  - Natural fit for backtracking pattern

- Visited Set/Hash Table:
  - Tracks explored nodes to avoid cycles
  - Provides O(1) lookups to check if node visited
  - Essential for handling graphs with cycles
  - Grows proportionally to number of vertices
  - Prevents infinite loops in cyclic graphs

- Graph Representation (Adjacency List):
  - Maps vertices to lists of neighbors
  - Enables O(1) access to a node's neighbors
  - Space efficient for sparse graphs
  - Supports both directed and undirected graphs
  - Allows flexible graph structures

Key advantages of DFS:
- Memory efficient for deep graphs compared to BFS
- Natural fit for recursive problems
- Good for topological sorting
- Path finding in maze-like structures
- Tree/graph structure analysis

Time Complexity: O(V + E) where:
- V is number of vertices (each vertex visited once)
- E is number of edges (each edge explored once)
- Stack operations are O(1)
- Visited set operations are O(1)

Space Complexity: O(V) for:
- Visited set to track explored nodes
- Recursion/explicit stack in worst case
- Linear space usage in deepest case
- Proportional to graph depth

```python
    def dfs_recursive(graph, start, visited=None):
        # Initialize visited set if this is the first call
        if visited is None:
            visited = set()
            
        # Mark current node as visited and process it
        visited.add(start)
        print(start)  # Process node (can be modified based on needs)
        
        # Recursively visit all unvisited neighbors
        for neighbor in graph[start]:
            if neighbor not in visited:
                dfs_recursive(graph, neighbor, visited)
                
    def dfs_iterative(graph, start):
        # Use explicit stack instead of recursion
        visited = set()
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                print(node)  # Process node
                # Add unvisited neighbors to stack
                # Reverse to maintain similar order to recursive
                for neighbor in reversed(graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

    # Example usage with both implementations
    g = {0: [1, 2], 1: [2], 2: [3], 3: []}
    print("Recursive DFS:")
    dfs_recursive(g, 0)  # 0,1,2,3
    print("\nIterative DFS:")
    dfs_iterative(g, 0)  # 0,1,2,3
```

### Dijkstra’s Algorithm (Advanced)

Description: Finds the shortest path from a start node to all others in a weighted graph with no negative edges. Uses a min-heap priority queue to always process the node with smallest current distance first. Maintains a distance dictionary to track shortest paths. The priority queue ensures we process nodes in order of increasing distance, making it more efficient than checking all edges repeatedly. Time complexity is O((V+E)logV) where V is number of vertices and E is number of edges. Space complexity is O(V) for the distance dictionary and priority queue.

```python
    import heapq
    from collections import defaultdict

    def dijkstra(graph, start):
        # Initialize distances and previous nodes for path reconstruction
        dist = {node: float('inf') for node in graph}
        prev = {node: None for node in graph}
        dist[start] = 0
        
        # Priority queue stores (distance, node) tuples
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_dist, u = heapq.heappop(pq)
            
            # Skip if we've found a better path already
            if u in visited:
                continue
                
            visited.add(u)
            
            # Explore neighbors
            for v, w in graph[u]:
                if v in visited:
                    continue
                    
                # Relaxation step
                new_dist = dist[u] + w
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(pq, (new_dist, v))
        
        return dist, prev

    def get_shortest_path(prev, start, end):
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = prev[current]
        return path[::-1]

    # Example weighted directed graph represented as adjacency list
    # Each neighbor is a tuple of (vertex, weight)
    weighted_graph = {
        'A': [('B',4), ('C',2)],
        'B': [('C',1), ('D',5)], 
        'C': [('B',1), ('D',8), ('E',10)],
        'D': [('E',2)],
        'E': []
    }

    # Find shortest paths from A
    distances, previous = dijkstra(weighted_graph, 'A')
    print(f"Distances from A: {distances}")
    
    # Get shortest path from A to E
    path = get_shortest_path(previous, 'A', 'E')
    print(f"Shortest path from A to E: {path}")
    # Output:
    # Distances from A: {'A': 0, 'B': 3, 'C': 2, 'D': 8, 'E': 10}
    # Shortest path from A to E: ['A', 'C', 'B', 'D', 'E']
```
### Bellman-Ford (Advanced)

Description: The Bellman-Ford algorithm finds shortest paths in a weighted graph that can handle negative edge weights (unlike Dijkstra's), with the constraint that there cannot be negative cycles. Here's a detailed breakdown:

Data Structures:
- Graph representation: List of edges where each edge is a tuple (u,v,w) representing edge from u to v with weight w
- Distance dictionary (dist): Maps each vertex to its current shortest distance from start vertex
  - Initially all distances set to infinity except start vertex (0)
  - Gets updated as shorter paths are found
  - Key: vertex, Value: current shortest distance

Key Algorithm Steps:
1. Initialize distances - O(V) space for distance dictionary
2. Relax all edges V-1 times:
   - For each edge (u,v,w), if dist[u] + w < dist[v], update dist[v]
   - V-1 iterations because longest possible path without cycles visits each vertex once
   - Each iteration processes all E edges
3. Optional: Check for negative cycles by trying one more relaxation
   - If any distance can still be reduced, negative cycle exists

Time Complexity: O(VE) - must process all E edges, V-1 times
Space Complexity: O(V) for the distance dictionary

Key Advantages:
- Can handle negative edge weights (unlike Dijkstra's)
- Simpler implementation than Dijkstra's (no priority queue needed)
- Can detect negative cycles
- Guarantees shortest paths if no negative cycles exist

The algorithm is especially useful for:
- Networks with negative weights (e.g., forex trading)
- Detecting arbitrage opportunities
- Situations where simple implementation is preferred over speed

```python
    def bellman_ford(graph, start):
        # graph: list of edges (u,v,w)
        # find shortest paths to all vertices from start
        dist = {}
        for u,v,w in graph:
            dist[u] = float('inf')
            dist[v] = float('inf')
        dist[start] = 0

        V = len(dist)
        for _ in range(V-1):
            for u,v,w in graph:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
        return dist

    edges = [('A','B',1),('B','C',2),('A','C',4)]
    print(bellman_ford(edges, 'A')) # {'A':0, 'B':1, 'C':3}
```

### Floyd-Warshall (Advanced)

Description: The Floyd-Warshall algorithm finds shortest paths between all pairs of vertices in a weighted graph, including those with negative edges but no negative cycles. Key features:
- Uses a 2D distance matrix/table to track shortest paths between every vertex pair
- Dynamically builds up paths by considering all vertices as potential intermediate points
- Matrix[i][j] represents shortest path from vertex i to j
- O(V^3) time complexity where V is number of vertices
- O(V^2) space complexity for the distance matrix
- More efficient than running Dijkstra's V times for dense graphs
- Great for:
  - Finding all-pairs shortest paths in one pass
  - Detecting negative cycles (if diagonal becomes negative)
  - Computing transitive closure of a graph
  - Finding maximum paths by negating edge weights

```python
    def floyd_warshall(matrix):
        """
        Finds shortest paths between all pairs of vertices in a weighted graph.
        Handles negative edges but detects negative cycles.
        Time: O(V^3), Space: O(V^2) where V is number of vertices
        """
        # Input validation
        if not matrix or not matrix[0]:
            return []
        n = len(matrix)
        if any(len(row) != n for row in matrix):
            raise ValueError("Matrix must be square")

        # Initialize distance matrix with copy of input
        # Using float('inf') for proper infinity handling
        dist = [[float('inf') if x == INF else x for x in row] for row in matrix]

        # Floyd-Warshall algorithm
        # For each vertex k as intermediate point
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # Skip if path through k involves infinity
                    if dist[i][k] == float('inf') or dist[k][j] == float('inf'):
                        continue
                    # Update if path through k is shorter
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        # Check for negative cycles by examining diagonal
        # If any vertex has negative path to itself, there's a negative cycle
        for i in range(n):
            if dist[i][i] < 0:
                raise ValueError("Graph contains negative cycle")

        return dist

    # Example demonstrating key features:
    # - Handling of infinite distances
    # - Finding paths through intermediate vertices
    # - Different path lengths including direct and indirect paths
    INF = float('inf')
    matrix = [
        # Direct paths: A->B=5, A->D=10
        # Indirect path: A->B->C->D = 9 (shorter than direct A->D)
        [0,   5,   INF, 10], 
        [INF, 0,   3,   INF],
        [INF, INF, 0,   1],
        [INF, INF, INF, 0]
    ]

    result = floyd_warshall(matrix)
    # Print formatted results showing discovered paths
    print("Shortest paths matrix:")
    for i, row in enumerate(result):
        formatted = [f"{x:^7.0f}" if x != float('inf') else "  INF  " for x in row]
        print(f"From vertex {i}: {formatted}")
    # Shortest paths matrix
```

### Topological Sort (Intermediate)

Description: Topological sort orders vertices in a Directed Acyclic Graph (DAG) such that all edges point forward in the ordering. Key data structures used:

- Dictionary/Hash Map for graph representation:
  - Maps vertices to lists of neighbors
  - Provides O(1) access to adjacency lists
  - Space efficient for sparse graphs
  - Easy to iterate over edges

- Queue for processing zero in-degree vertices:
  - Enables breadth-first processing order
  - O(1) enqueue/dequeue operations
  - Maintains FIFO ordering of vertices
  - Key to Kahn's algorithm approach

- Dictionary for tracking in-degree counts:
  - Maps vertices to number of incoming edges
  - O(1) updates when processing edges
  - Helps identify available vertices
  - Detects cycles if counts remain non-zero

The algorithm is ideal for:
- Dependency resolution
- Task scheduling
- Build systems
- Course prerequisites
- Process ordering

```python
    def topological_sort(graph):
        """
        Performs topological sort on a directed acyclic graph (DAG) using Kahn's algorithm.
        Returns vertices in an order where for each directed edge u->v, u comes before v.
        
        Args:
            graph: Dict representing DAG where keys are vertices and values are lists of neighbors
            
        Returns:
            List of vertices in topological order
            
        Raises:
            ValueError if graph contains a cycle
        """
        # Track in-degree (number of incoming edges) for each vertex
        in_degree = {u: 0 for u in graph}
        for u in graph:
            for v in graph[u]:
                in_degree[v] = in_degree.get(v, 0) + 1
                
        # Initialize queue with vertices that have no incoming edges
        queue = deque([u for u in graph if in_degree[u] == 0])
        order = []
        
        # Process vertices in queue
        while queue:
            u = queue.popleft()
            order.append(u)
            
            # Reduce in-degree of neighbors and add to queue if in-degree becomes 0
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
                    
        # Check if all vertices were processed (no cycles)
        if len(order) != len(graph):
            raise ValueError("Graph contains a cycle - topological sort not possible")
            
        return order

    # Example usage showing different DAG scenarios
    if __name__ == "__main__":
        from collections import deque
        
        # Example 1: Simple linear DAG
        dag1 = {
            'A': ['B'],
            'B': ['C'],
            'C': ['D'],
            'D': []
        }
        print("Linear DAG:", topological_sort(dag1))  # ['A', 'B', 'C', 'D']
        
        # Example 2: DAG with multiple paths
        dag2 = {
            'CS101': ['CS201', 'CS210'],
            'CS201': ['CS301'],
            'CS210': ['CS301'],
            'CS301': ['CS401'],
            'CS401': []
        }
        print("Course prerequisites:", topological_sort(dag2))
        
        # Example 3: DAG with independent paths
        dag3 = {
            'start': ['a1', 'b1'],
            'a1': ['a2'],
            'a2': ['end'],
            'b1': ['b2'],
            'b2': ['end'],
            'end': []
        }
        print("Parallel paths:", topological_sort(dag3))
```

### Knuth-Morris-Pratt (KMP) (Intermediate)

Description: The Knuth-Morris-Pratt (KMP) algorithm is an efficient string pattern matching algorithm that uses a prefix table (also called failure function or LPS array) to avoid unnecessary character comparisons. Key features:

Data Structures:
- Pattern string: The substring we're searching for
- Text string: The main string we're searching in
- Prefix table (int[]): An array storing the length of longest proper prefix that is also a suffix for each position
  - Helps skip comparisons by remembering previously matched characters
  - Size is equal to pattern length
  - Built in O(m) time where m is pattern length
  - Used to determine how far back to move pattern when mismatch occurs

Time Complexity:
- O(m) preprocessing to build prefix table
- O(n) for pattern search where n is text length
- Total: O(m + n) vs O(mn) for naive approach

Common Use Cases:
- String searching/pattern matching
- DNA sequence matching
- Finding repeated substrings
- Text editors and word processors
- Network packet inspection

```python
    def build_lps_array(pattern):
        """
        Build Longest Proper Prefix which is also Suffix (LPS) array
        LPS[i] = length of longest proper prefix that is also suffix for pattern[0..i]
        """
        lps = [0] * len(pattern)  # Initialize LPS array with 0s
        length = 0  # Length of previous longest prefix suffix
        i = 1  # Start from second character

        while i < len(pattern):
            if pattern[i] == pattern[length]:
                # If characters match, increment length and store in LPS
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    # If mismatch after some matching characters
                    # Use LPS array to determine new length
                    length = lps[length - 1]
                else:
                    # If mismatch at start
                    lps[i] = 0
                    i += 1
        return lps

    def kmp_search(text, pattern):
        """
        Knuth-Morris-Pratt algorithm for pattern matching
        Returns: List of all starting indices where pattern is found in text
        Time Complexity: O(n + m) where n = len(text), m = len(pattern)
        """
        if not pattern or not text:
            return []
        if len(pattern) > len(text):
            return []

        matches = []
        lps = build_lps_array(pattern)
        
        i = 0  # Index for text
        j = 0  # Index for pattern
        
        while i < len(text):
            # Characters match - move both pointers
            if text[i] == pattern[j]:
                i += 1
                j += 1
                
                # Found complete pattern
                if j == len(pattern):
                    matches.append(i - j)
                    # Look for more matches - use LPS to avoid recomparing
                    j = lps[j - 1]
                    
            else:
                if j > 0:
                    # Mismatch after some matches - use LPS array
                    j = lps[j - 1]
                else:
                    # Mismatch at start - move text pointer
                    i += 1
                    
        return matches

    # Example usage showing multiple pattern occurrences
    text = "AABAACAADAABAAABAA"
    pattern = "AABA"
    matches = kmp_search(text, pattern)
    print(f"Pattern '{pattern}' found at indices: {matches}")  # [0, 9, 13]

    # Example with no matches
    print(kmp_search("ABCDEF", "XYZ"))  # []

    # Example with DNA sequence matching
    dna = "ACGTACGTACGT"
    seq = "ACGT" 
    print(f"DNA sequence '{seq}' found at indices: {kmp_search(dna, seq)}")  # [0, 4, 8]
```

### Rabin-Karp (Intermediate)

Description: The Rabin-Karp algorithm uses rolling hash functions and string matching to efficiently find pattern strings in text. Key features:

- Uses a hash table to store pattern hashes for O(1) lookup
- Rolling hash function allows O(1) hash updates when sliding window
- Can match multiple patterns simultaneously (unlike KMP)
- Average case O(n+m) time complexity where:
  - n is length of text
  - m is length of pattern(s)
- Worst case O(nm) if many hash collisions occur
- Common applications:
  - Plagiarism detection
  - Multiple pattern matching
  - DNA sequence alignment
  - Finding duplicate file content

Data structures used:
- Hash table: Stores pattern hashes for constant time lookup
- Sliding window: Maintains current substring being compared
- Rolling hash: Special hash function that can be updated in O(1)

```python
    def rabin_karp(text, patterns):
        """
        Rabin-Karp string matching algorithm that can find multiple patterns.
        Uses rolling hash for efficient sliding window comparison.
        
        Args:
            text: String to search in
            patterns: Single pattern string or list of pattern strings
        
        Returns:
            Dictionary mapping each pattern to list of indices where it was found
        """
        # Handle single pattern case
        if isinstance(patterns, str):
            patterns = [patterns]
            
        # Initialize variables
        base = 256  # Number of characters in input alphabet
        prime = 101  # Prime number for hash calculation
        results = {p: [] for p in patterns}
        
        # Process each pattern
        for pattern in patterns:
            m = len(pattern)
            n = len(text)
            
            if m > n:
                continue
                
            # Calculate initial hash values
            pattern_hash = 0
            text_hash = 0
            h = pow(base, m-1) % prime  # Used for rolling hash calculation
            
            # Calculate hash value for pattern and first window of text
            for i in range(m):
                pattern_hash = (base * pattern_hash + ord(pattern[i])) % prime
                text_hash = (base * text_hash + ord(text[i])) % prime
                
            # Slide pattern over text one by one
            for i in range(n - m + 1):
                # Check character by character if hash values match
                if pattern_hash == text_hash:
                    if text[i:i+m] == pattern:
                        results[pattern].append(i)
                        
                # Calculate hash value for next window by removing leading digit
                # and adding trailing digit
                if i < n - m:
                    text_hash = ((text_hash - ord(text[i]) * h) * base + 
                                ord(text[i + m])) % prime
                    
                    # Handle negative values
                    if text_hash < 0:
                        text_hash += prime

        return results

    # Example usage
    text = "AABAACAADAABAAABAA"
    pattern = "AABA"
    print(f"Pattern '{pattern}' found at indices: {rabin_karp(text, pattern)[pattern]}")  # [0, 9, 13]

    # Multiple pattern matching
    dna = "ACGTACGTACGT" 
    patterns = ["ACGT", "CGT"]
    matches = rabin_karp(dna, patterns)
    for p in patterns:
        print(f"Pattern '{p}' found at indices: {matches[p]}")
```

### Dynamic Programming (DP) (Advanced)

Description: Dynamic Programming (DP) is a problem-solving technique that breaks down complex problems into simpler subproblems and stores their solutions to avoid redundant computations. Key features:

Data Structures Used:
- Arrays/Lists: For tabulation approach to store solutions bottom-up
- Hash Maps/Dictionaries: For memoization approach to cache computed results
- Recursion Stack: When using recursive memoization approach

Common Use Cases:
- Optimization problems (finding min/max values)
- Counting problems (number of ways to achieve something)
- Problems with overlapping subproblems

Example: Computing nth Fibonacci number demonstrates both main DP approaches:
1. Top-down memoization using hash map to cache results
2. Bottom-up tabulation using array to build solution iteratively

Benefits:
- Reduces time complexity from O(2^n) to O(n)
- Space-time tradeoff using extra memory for better runtime
- Avoids redundant calculations by storing intermediate results

```python
    # Top-down memoization approach
    def fib_memoization(n, memo=None):
        """Calculate nth Fibonacci number using memoization (top-down DP)
        Time: O(n), Space: O(n)"""
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n < 2:
            return n
        memo[n] = fib_memoization(n-1, memo) + fib_memoization(n-2, memo)
        return memo[n]

    # Bottom-up tabulation approach  
    def fib_tabulation(n):
        """Calculate nth Fibonacci number using tabulation (bottom-up DP)
        Time: O(n), Space: O(n)"""
        if n < 2:
            return n
        # Initialize table to store solutions of subproblems
        dp = [0] * (n + 1)
        dp[1] = 1
        
        # Fill table in bottom-up manner
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[n]

    # Space-optimized iterative approach
    def fib_optimized(n):
        """Calculate nth Fibonacci number using constant space
        Time: O(n), Space: O(1)"""
        if n < 2:
            return n
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        return curr

    # Example usage demonstrating all approaches
    n = 10
    print(f"Fibonacci({n}) using memoization:", fib_memoization(n))    # 55
    print(f"Fibonacci({n}) using tabulation:", fib_tabulation(n))      # 55
    print(f"Fibonacci({n}) using optimized:", fib_optimized(n))        # 55

```

### Greedy Algorithms (Family)

Description: Greedy algorithms make locally optimal choices at each step, hoping to find a global optimum. A classic example is interval scheduling - selecting the maximum number of non-overlapping intervals from a set of intervals.

Key data structures and why they're used:
- List of tuples for intervals: 
  - List provides O(n log n) sorting efficiency
  - Tuples are immutable and memory-efficient for storing (start,end) pairs
  - Random access O(1) for iterating through sorted intervals
  - Appending selected intervals is O(1)

- Single variable for tracking current end time:
  - Simple integer variable sufficient since we only need latest end time
  - O(1) comparisons for checking overlaps
  - Constant space overhead

The greedy strategy is to:
1. Sort intervals by end time (earliest ending first)
2. Take first interval
3. Take next interval that starts after current end time
4. Repeat until no more intervals

This produces optimal solution in O(n log n) time due to sorting, with O(n) space complexity.

```python
    # Store intervals as list of tuples (start_time, end_time)
    # List allows O(n log n) sorting and O(1) appends
    # Tuples are immutable and space-efficient for pairs
    intervals = [(1,3), (2,4), (3,5), (0,6), (5,7)]

    # Sort intervals by end time in O(n log n)
    # This is the key greedy choice - earliest finishing intervals
    # allow most room for additional intervals
    intervals.sort(key=lambda x: x[1])  

    # Store selected intervals in result list
    # List allows O(1) appends and maintains selection order
    result = []
    
    # Track end time of last selected interval
    # Initialize to -1 to handle first interval
    current_end = -1

    # Iterate through sorted intervals once, O(n)
    # Greedily select non-overlapping intervals
    for interval in intervals:
        start = interval[0]
        end = interval[1]
        
        # If current interval starts after previous end
        # we can select it without overlap
        if start >= current_end:
            result.append(interval)
            current_end = end

    # Result contains maximum set of non-overlapping intervals
    print(f"Maximum non-overlapping intervals: {result}")
```

### Suffix Array Construction (Intermediate/Advanced)

*Description:* A suffix array is a space-efficient data structure that holds the starting indexes of all suffixes of a string in sorted lexicographical order. Key features and data structures used:

- Core data structure is an integer array storing suffix start positions
  - More memory efficient than storing actual suffix strings
  - Allows O(1) random access to any suffix position
  - Maintains sorted order implicitly through positions

- Often paired with LCP (Longest Common Prefix) array
  - Stores length of common prefix between adjacent suffixes
  - Enables efficient string processing algorithms
  - Takes O(n) additional space

- Common use cases:
  - Pattern matching
  - Finding repeated substrings
  - Data compression
  - Bioinformatics (DNA sequence analysis)

The naive construction approach shown here is O(n² log n), though more efficient O(n) algorithms exist like SA-IS. The naive version helps illustrate the core concept while being simpler to understand.

```python
    def suffix_array(s):
        """
        Build a suffix array for string s using naive approach.
        
        Data structures used:
        - List of tuples: Store (suffix, position) pairs
          - Allows O(1) access and O(n log n) sorting
          - Tuples are immutable and memory efficient
          - First element is suffix string for sorting
          - Second element preserves original position
        - Final list: Store sorted positions
          - Maintains order of suffix positions
          - Allows O(1) access by index
        
        Time complexity: O(n² log n)
        - O(n) to generate suffixes
        - Each suffix comparison takes O(n)
        - Sorting takes O(n log n) comparisons
        - Total: O(n) * O(n log n) = O(n² log n)
        
        Space complexity: O(n²)
        - Storing n suffixes of average length n/2
        """
        # Create list of (suffix, position) tuples
        # Each suffix starts at position i and goes to end
        suffixes = [(s[i:], i) for i in range(len(s))]
        
        # Sort suffixes lexicographically
        # Python's sort is stable - maintains relative order of equal elements
        suffixes.sort()  # O(n² log n) due to string comparisons
        
        # Extract just the positions in sorted order
        # List comprehension maintains order while dropping suffixes
        return [pos for (suffix, pos) in suffixes]

    # Example usage showing suffix array construction
    text = "banana"
    # Returns [5,3,1,0,4,2] corresponding to suffixes:
    # a, ana, anana, banana, na, nana
    print(suffix_array(text))
```

### Suffix Tree (Conceptual)

Description: Suffix trees are advanced data structures that enable extremely fast substring searching in O(m) time (where m is the pattern length). They achieve this by preprocessing the text to build a tree-like structure with the following key components:

Data Structures Used:
- Tree Structure: A rooted tree where:
  - Each edge is labeled with a substring of the text
  - Each internal node has multiple children
  - Each leaf represents a suffix of the original text
  - Enables O(m) substring search by following edges matching pattern

- Hash Maps/Dictionaries:
  - Used to store children of each node
  - Maps characters to child nodes
  - Provides O(1) access to next node during traversal
  - Critical for efficient navigation during search

- Suffix Links:
  - Special pointers between internal nodes
  - Enable O(n) construction using Ukkonen's algorithm
  - Connect nodes representing related substrings
  - Essential for linear-time building

While powerful, suffix trees are complex to implement correctly and have a significant memory footprint. This implementation shows a conceptual node structure using Ukkonen's algorithm for linear-time construction.

```python
    class SuffixTreeNode:
        """
        A node in a suffix tree data structure.
        
        Attributes:
            children (dict): Maps characters to child nodes
            start (int): Starting index of substring on edge to this node
            end (int): Ending index of substring on edge to this node
            suffix_link (SuffixTreeNode): Link to longest proper suffix
            leaf (bool): Whether this is a leaf node
            
        The suffix tree allows O(m) substring searches where m is pattern length.
        Each node represents a substring of the original text, with:
        - Edge labels = substrings from text
        - Root to leaf paths = all suffixes
        - Suffix links for O(n) construction
        """
        def __init__(self, start=-1, end=None):
            self.children = {}  # Map from chars to child nodes
            self.start = start  # Start index of substring on edge
            self.end = end      # End index of substring on edge
            self.suffix_link = None  # Link to longest proper suffix
            self.leaf = False   # Whether this is a leaf node
            
        def get_edge_length(self):
            """Get length of substring on edge to this node"""
            if self.end is None:
                return 0
            return self.end - self.start
            
        def add_child(self, char, node):
            """Add a child node under given character"""
            self.children[char] = node
            
        def get_child(self, char):
            """Get child node for given character"""
            return self.children.get(char)

    def build_suffix_tree(text):
        """Build suffix tree for text using Ukkonen's algorithm"""
        # Add terminal character to handle leaf nodes
        text = text + "$"
        n = len(text)
        
        # Create root node
        root = SuffixTreeNode()
        
        # Active point tracks where we need to add next suffix
        active_node = root
        active_edge = None
        active_length = 0
        
        # Tracks where suffix link should go from last created node
        last_new_node = None
        
        # Process each character to build tree incrementally
        for i in range(n):
            # For each position, extend all suffixes
            remaining = 1  # Number of suffixes yet to be added
            
            while remaining > 0:
                if active_length == 0:
                    # Start new edge from active node
                    if active_node.get_child(text[i]) is None:
                        # Create new leaf node
                        leaf = SuffixTreeNode(i, None)
                        leaf.leaf = True
                        active_node.add_child(text[i], leaf)
                        
                        # Add suffix link if needed
                        if last_new_node is not None:
                            last_new_node.suffix_link = active_node
                            last_new_node = None
                    else:
                        # Match found - begin walking down
                        active_edge = text[i]
                        active_length = 1
                        break  # Rule 3 extension
                else:
                    # Continue current path
                    next_char = text[i]
                    edge_node = active_node.get_child(active_edge)
                    edge_length = edge_node.get_edge_length()
                    
                    if active_length >= edge_length:
                        # Walk down to next node
                        active_node = edge_node
                        active_length -= edge_length
                        active_edge = next_char
                        continue
                        
                    # Check next character on edge
                    edge_pos = edge_node.start + active_length
                    if text[edge_pos] == next_char:
                        # Match found
                        active_length += 1
                        break  # Rule 3 extension
                    
                    # Split edge and add new leaf
                    split = SuffixTreeNode(edge_node.start, edge_node.start + active_length)
                    active_node.add_child(active_edge, split)
                    
                    # Add leaf node for new suffix
                    leaf = SuffixTreeNode(i, None) 
                    leaf.leaf = True
                    split.add_child(next_char, leaf)
                    
                    # Update original node
                    edge_node.start += active_length
                    split.add_child(text[edge_node.start], edge_node)
                    
                    # Add suffix link if needed
                    if last_new_node is not None:
                        last_new_node.suffix_link = split
                    last_new_node = split
                
                remaining -= 1
                
                if active_node == root and active_length > 0:
                    active_length -= 1
                    active_edge = text[i - remaining + 1]
                elif active_node.suffix_link is not None:
                    active_node = active_node.suffix_link
                else:
                    active_node = root
                    
        return root
        
    # Example usage
    text = "banana"
    root = build_suffix_tree(text)
```

### Kruskal’s Algorithm for Minimum Spanning Tree (MST) (Intermediate)

Description: Kruskal's algorithm finds a Minimum Spanning Tree (MST) by greedily selecting edges in order of increasing weight while avoiding cycles. Key features:

Data Structures Used:
- Priority Queue/Sorted List: Edges are sorted by weight to process smallest weights first
- Disjoint Set (Union-Find): Efficiently tracks connected components to detect cycles
  - Uses arrays/lists for O(1) access to parent pointers
  - Path compression and union by rank optimizations
- Graph representation: Edge list format works well since we need to sort edges
  - Each edge stores (weight, vertex1, vertex2)
  - No need for adjacency lists/matrix since we process edges sequentially

The algorithm works by:
1. Sorting all edges by weight (O(E log E))
2. Processing edges in order, using Union-Find to:
   - Check if vertices are already connected (would form cycle)
   - If not connected, add edge to MST and merge components
3. Continues until MST has (V-1) edges

Time Complexity: O(E log E) for sort + O(E * α(V)) for Union-Find operations
Space Complexity: O(V) for Union-Find data structure

```python
    class UnionFind:
        """
        A Union-Find (Disjoint Set) data structure that efficiently tracks disjoint sets
        and supports union operations. Used in Kruskal's to detect cycles.
        
        Key features:
        - Uses path compression in find() for near O(1) operations
        - Uses union by rank to keep trees balanced
        - parent[]: Each index maps to its parent node (initially itself)
        - rank[]: Tracks approximate depth of each tree to keep balanced
        
        Time complexity:
        - find(): O(α(n)) amortized (α is inverse Ackermann, effectively constant)
        - union(): O(α(n)) amortized
        """
        def __init__(self, n):
            """Initialize n disjoint sets, each element is its own set"""
            self.parent = list(range(n))  # Each element starts as its own parent
            self.rank = [0]*n  # Track tree depths to keep balanced

        def find(self, x):
            """Find set representative for element x with path compression"""
            if self.parent[x] != x:
                # Path compression: Make all nodes on path point to root
                self.parent[x] = self.find(self.parent[x])
            return self.parent[x]

        def union(self, x, y):
            """
            Union sets containing x and y if they're different.
            Uses union by rank to keep trees balanced.
            Returns True if union performed, False if already in same set.
            """
            rx, ry = self.find(x), self.find(y)
            if rx != ry:
                # Union by rank: Attach smaller rank tree under root of higher rank
                if self.rank[rx] < self.rank[ry]:
                    rx, ry = ry, rx  # Ensure rx has higher/equal rank
                self.parent[ry] = rx
                # Increase rank of rx if ranks were equal
                if self.rank[rx] == self.rank[ry]:
                    self.rank[rx] += 1
                return True
            return False

    def kruskal(edges, n):
        """
        Kruskal's MST Algorithm using Union-Find to detect cycles.
        
        Args:
            edges: List of tuples (weight, u, v) representing weighted edges
            n: Number of vertices (0 to n-1)
            
        Returns:
            List of (u,v,weight) tuples in the MST
            
        Time complexity: O(E log E) due to sorting edges
        Space complexity: O(V) for UnionFind + O(E) for edge list
        """
        # Sort edges by weight to process cheapest first
        edges.sort(key=lambda x: x[0])
        
        # Initialize Union-Find to track connected components
        uf = UnionFind(n)
        
        # Build MST by adding edges that don't create cycles
        mst = []
        for w, u, v in edges:
            # Union returns True if u,v were in different components
            if uf.union(u,v):
                mst.append((u,v,w))
        return mst

    # Example usage demonstrating a simple graph:
    # Vertices: 0,1,2,3 forming a diamond shape
    # Edges: (weight, from_vertex, to_vertex)
    edges = [
        (1,0,1),  # Weight 1 edge from 0->1
        (3,0,2),  # Weight 3 edge from 0->2
        (2,1,2),  # Weight 2 edge from 1->2
        (4,2,3)   # Weight 4 edge from 2->3
    ]
    print(kruskal(edges, 4))  # Returns MST edges in order added
    # Output: [(0,1,1), (1,2,2), (2,3,4)] representing minimum spanning tree
```

### Prim’s Algorithm for MST (Intermediate)

Description: Prim's algorithm finds a Minimum Spanning Tree (MST) by iteratively growing a tree from a starting vertex. Key features:

Data Structures:
- Priority Queue (Min Heap): Essential for efficiently selecting the next lightest edge. Stores (weight, vertex, parent) tuples and provides O(log V) operations.
- Visited Set: Tracks vertices already in MST to avoid cycles. O(1) lookups.
- Adjacency List: Graph representation allowing O(1) access to neighbors. More space efficient than matrix for sparse graphs.

The algorithm maintains a "frontier" of edges in the priority queue, always greedily selecting the lightest edge that connects to an unvisited vertex. This guarantees optimality because:
1. Any MST must cross each cut of the graph with its lightest edge
2. The priority queue ensures we always select the current lightest edge
3. The visited set ensures we don't create cycles

Ideal for dense graphs where Kruskal's algorithm's edge sorting becomes expensive.

```python
def prim(graph, start):
    """
    Prim's MST Algorithm using a min heap priority queue.
    
    Args:
        graph: Dict representing adjacency list {vertex: [(neighbor, weight), ...]}
        start: Starting vertex to grow MST from
        
    Returns:
        List of (u,v,weight) tuples in the MST
        
    Time complexity: O(E log V) using binary heap
    Space complexity: O(V + E) for visited set and heap
    """
    visited = set()  # Track vertices in MST
    mst = []        # Store MST edges
    total_cost = 0  # Track total weight of MST
    
    # Priority queue stores (weight, vertex, parent) tuples
    min_heap = [(0, start, None)]
    
    while min_heap and len(visited) < len(graph):
        weight, curr_vertex, parent = heapq.heappop(min_heap)
        
        # Skip if vertex already in MST
        if curr_vertex in visited:
            continue
            
        visited.add(curr_vertex)
        
        # Add edge to MST (except for start vertex)
        if parent is not None:
            mst.append((parent, curr_vertex, weight))
            total_cost += weight
            
        # Add edges to unvisited neighbors
        for neighbor, edge_weight in graph[curr_vertex]:
            if neighbor not in visited:
                heapq.heappush(min_heap, (edge_weight, neighbor, curr_vertex))
                
    return mst, total_cost

# Example usage showing different graph configurations:

# Diamond shaped graph (same as Kruskal's example)
diamond_graph = {
    0: [(1,1), (2,3)],
    1: [(0,1), (2,2), (3,5)], 
    2: [(0,3), (1,2), (3,4)],
    3: [(1,5), (2,4)]
}

# More complex graph with multiple possible MSTs
complex_graph = {
    0: [(1,4), (2,3)],
    1: [(0,4), (2,1), (3,2)],
    2: [(0,3), (1,1), (3,4), (4,5)],
    3: [(1,2), (2,4), (4,7)],
    4: [(2,5), (3,7)]
}

# Test both graphs
print("Diamond Graph MST:")
mst_edges, total_weight = prim(diamond_graph, 0)
print(f"MST Edges: {mst_edges}")
print(f"Total Weight: {total_weight}\n")

print("Complex Graph MST:") 
mst_edges, total_weight = prim(complex_graph, 0)
print(f"MST Edges: {mst_edges}")
print(f"Total Weight: {total_weight}")
```

### A* Search (Advanced)

Description: A* is an advanced pathfinding algorithm that combines Dijkstra's shortest path with heuristic guidance to efficiently find optimal paths. Key features:

Data Structures Used:
- Priority Queue (Min-Heap): Stores nodes to explore, prioritized by f(n) = g(n) + h(n)
  - g(n): Actual cost from start to current node 
  - h(n): Heuristic estimated cost from current to goal
  - Enables efficient O(log n) selection of most promising nodes
- Dictionary/Hash Map: 
  - Tracks parent pointers for path reconstruction
  - Stores g-scores and f-scores for each node
  - Provides O(1) lookups
- Set: 
  - Maintains visited nodes
  - Ensures O(1) lookup to avoid revisiting nodes
- Grid Array:
  - 2D array representing the map/maze
  - Allows O(1) access to check valid moves

The algorithm guarantees finding the optimal path when using an admissible heuristic (never overestimates). Common use cases include:
- Video game pathfinding
- Robot navigation
- Route planning
- Maze solving

Below is an implementation for grid-based pathfinding using Manhattan distance heuristic.

```python
import heapq
from typing import List, Tuple, Dict, Set, Optional

def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    """Calculate heuristic distance between two points.
    
    Args:
        a: Starting point coordinates (x,y)
        b: Goal point coordinates (x,y)
        
    Returns:
        Estimated distance between points using Manhattan distance
    """
    # Manhattan distance on a grid - admissible heuristic that never overestimates
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos: Tuple[int, int], grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Get valid neighboring positions.
    
    Args:
        pos: Current position (x,y)
        grid: 2D grid map
        
    Returns:
        List of valid neighbor positions
    """
    rows, cols = len(grid), len(grid[0])
    x, y = pos
    neighbors = []
    
    # Check all 4 adjacent cells
    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if (0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0):
            neighbors.append((nx, ny))
            
    return neighbors

def reconstruct_path(parent: Dict[Tuple[int, int], Tuple[int, int]], 
                    current: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Reconstruct path from parent pointers.
    
    Args:
        parent: Dictionary mapping positions to their parent in the path
        current: Current/goal position to trace back from
        
    Returns:
        List of positions forming the path from start to goal
    """
    path = []
    while current is not None:
        path.append(current)
        current = parent.get(current)
    return path[::-1]

def astar_search(grid: List[List[int]], 
                start: Tuple[int, int], 
                goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """Find shortest path using A* search algorithm.
    
    Args:
        grid: 2D grid where 0=walkable, 1=blocked
        start: Starting position coordinates (x,y)
        goal: Goal position coordinates (x,y)
        
    Returns:
        List of positions forming shortest path if one exists, None otherwise
    """
    # Priority queue ordered by f-score (g + h)
    open_set = [(0, start)]
    
    # Track g-scores (actual distance from start)
    g_score = {start: 0}
    
    # Track parent pointers for path reconstruction
    parent = {start: None}
    
    # Track visited nodes
    closed_set: Set[Tuple[int, int]] = set()

    while open_set:
        # Get node with lowest f-score
        f_score, current = heapq.heappop(open_set)
        
        if current in closed_set:
            continue
            
        if current == goal:
            return reconstruct_path(parent, current)
            
        closed_set.add(current)
        
        # Check all neighbors
        for neighbor in get_neighbors(current, grid):
            if neighbor in closed_set:
                continue
                
            # 1 is the distance between adjacent cells
            tentative_g = g_score[current] + 1
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
                
    return None  # No path exists

# Example usage with different maze configurations
simple_maze = [
    [0,0,0,1],
    [0,1,0,0], 
    [0,0,0,0],
    [1,0,0,0]
]

complex_maze = [
    [0,0,0,1,0],
    [1,1,0,1,0],
    [0,0,0,0,0],
    [0,1,1,1,0],
    [0,0,0,1,0]
]

# Test simple maze
start, goal = (0,0), (3,3)
path = astar_search(simple_maze, start, goal)  # Prints [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 3), (3, 3)]
print("Simple maze path:", path)

# Test complex maze
start, goal = (0,0), (4,4) 
path = astar_search(complex_maze, start, goal)  # Prints [(0, 0), (0, 1), (0, 2), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4)]
print("Complex maze path:", path)

# Test impossible maze
impossible_maze = [
    [0,0,1],
    [1,1,1],
    [0,0,0]
]
start, goal = (0,0), (2,2)
path = astar_search(impossible_maze, start, goal)  # This will print None since there is no valid path from (0,0) to (2,2) due to the wall of 1's blocking the way
print("Impossible maze path:", path)  # Should print None
```

### Dynamic Programming: Longest Increasing Subsequence (LIS) (Intermediate)

Description: Dynamic Programming solution for finding the length of the Longest Increasing Subsequence (LIS) in O(n²) time. Key features:

Data Structures Used:
- DP Array: 
  - 1D array storing length of LIS ending at each index
  - dp[i] represents length of LIS ending at index i
  - Enables efficient subproblem reuse and optimal solution building
  - O(n) space complexity
  - Provides O(1) access to previous solutions

- Input Array:
  - Original sequence stored as array/list
  - Immutable to preserve values during DP computation
  - Supports O(1) element comparisons

The algorithm systematically builds solutions by:
1. Initializing dp[i] = 1 for all indices (single element subsequences)
2. For each position i, checking all previous positions j < i
3. If arr[j] < arr[i], can extend subsequence ending at j
4. Taking maximum of all possible extensions

Common applications include:
- Stock price analysis
- Box stacking problems
- Chain optimization
- Sequence analysis

```python
    def longest_increasing_subsequence(arr):
        """Find length and one possible longest increasing subsequence.
        
        Args:
            arr: Input array of numbers
            
        Returns:
            Tuple of (length, subsequence) where subsequence is one possible LIS
        """
        if not arr:
            return 0, []
            
        n = len(arr)
        # dp[i] stores length of LIS ending at index i
        dp = [1] * n
        
        # prev[i] stores previous index in LIS ending at i
        prev = [-1] * n
        
        # Track index of cell containing longest subsequence
        max_length = 1
        max_index = 0
        
        # Build solutions bottom-up
        for i in range(n):
            for j in range(i):
                if arr[j] < arr[i]:
                    # Can extend subsequence ending at j
                    if dp[j] + 1 > dp[i]:
                        dp[i] = dp[j] + 1
                        prev[i] = j
                        
            # Update max if needed
            if dp[i] > max_length:
                max_length = dp[i]
                max_index = i
                
        # Reconstruct subsequence by walking back through prev pointers
        subsequence = []
        curr = max_index
        while curr != -1:
            subsequence.append(arr[curr])
            curr = prev[curr]
            
        return max_length, subsequence[::-1]  # Reverse to get correct order

    # Example usage showing both length and subsequence
    sequence = [10, 9, 2, 5, 3, 7, 101, 18]
    length, subseq = longest_increasing_subsequence(sequence)
    print(f"Length: {length}")  # 4
    print(f"One possible LIS: {subseq}")  # [2, 5, 7, 101]

    # Test empty array
    print(longest_increasing_subsequence([]))  # (0, [])

    # Test array with one element
    print(longest_increasing_subsequence([5]))  # (1, [5])

    # Test strictly decreasing array
    print(longest_increasing_subsequence([5,4,3,2,1]))  # (1, [1])
```

### Advanced DP Variation: Minimum Edit Distance (Levenshtein Distance)

Description: The Minimum Edit Distance (Levenshtein Distance) algorithm calculates the minimum number of operations needed to transform one string into another. Key features:

Data Structures Used:
- 2D DP Table (Matrix): 
  - Size (m+1) x (n+1) where m,n are string lengths
  - Each cell [i,j] represents min edits needed for prefixes s1[0:i], s2[0:j]
  - Enables efficient subproblem reuse and optimal solution building
  - O(mn) space complexity

- Strings:
  - Input strings stored as arrays/strings for O(1) character access
  - Immutable to preserve original strings during comparison
  - Support efficient substring operations

The algorithm systematically fills the DP table by considering three possible operations at each step:
- Insertion: Add a character (cost of 1)
- Deletion: Remove a character (cost of 1) 
- Substitution: Replace a character (cost of 1 if chars different, 0 if same)

Common applications include:
- Spell checking and correction
- DNA sequence alignment
- Natural language processing
- Fuzzy string matching

```python
    def edit_distance(s1: str, s2: str) -> int:
        """Calculate minimum edit distance between two strings.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Minimum number of operations (insert/delete/substitute) to transform s1 to s2
            
        The DP table is filled using the recurrence relation:
        If chars match: dp[i][j] = dp[i-1][j-1]
        If chars differ: dp[i][j] = 1 + min(
            dp[i-1][j],   # deletion
            dp[i][j-1],   # insertion
            dp[i-1][j-1]  # substitution
        )
        """
        m, n = len(s1), len(s2)
        
        # Create DP table with base cases
        dp = [[0]*(n+1) for _ in range(m+1)]
        
        # Base cases - transforming to/from empty string
        for i in range(m+1):
            dp[i][0] = i  # Deletions needed
        for j in range(n+1):
            dp[0][j] = j  # Insertions needed
            
        # Fill DP table
        for i in range(1, m+1):
            for j in range(1, n+1):
                if s1[i-1] == s2[j-1]:
                    # Characters match - no operation needed
                    dp[i][j] = dp[i-1][j-1]
                else:
                    # Take minimum of three operations
                    dp[i][j] = 1 + min(
                        dp[i-1][j],    # deletion
                        dp[i][j-1],    # insertion 
                        dp[i-1][j-1]   # substitution
                    )
                    
        return dp[m][n]

    # Example usage with different test cases
    print(edit_distance("kitten", "sitting"))  # 3 operations
    print(edit_distance("sunday", "saturday"))  # 3 operations
    print(edit_distance("", "abc"))  # 3 operations (all insertions)
    print(edit_distance("abc", ""))  # 3 operations (all deletions)
    print(edit_distance("same", "same"))  # 0 operations

```
----
## Additional DP examples:

Below are several additional examples of dynamic programming (DP) solutions, illustrating both memoization (top-down) and tabulation (bottom-up) approaches, along with common use cases. These examples include classic problems like the 0/1 Knapsack, Coin Change, Longest Common Subsequence (LCS), and a simple counting paths problem. Each snippet will show a brief explanation of where such an approach is beneficial and when to consider using either iterative (tabulation) or memoization strategies.

---

### 0/1 Knapsack Problem

The 0/1 Knapsack problem is a classic optimization problem that demonstrates the power of dynamic programming. Given a set of items, each with a weight and a value, and a capacity constraint on the total weight, the goal is to maximize the total value without exceeding the capacity.

Key Data Structures Used:
- Arrays/Lists: Store the weights and values of items
  - Provides O(1) access to item properties
  - Maintains item ordering for consistent lookup
- 2D DP Array/Dictionary: 
  - Memoization: Dictionary mapping (item_index, remaining_capacity) to optimal value
  - Tabulation: 2D array where dp[i][w] represents optimal value for first i items with capacity w
  - Enables O(1) lookup of subproblem solutions
  - Space complexity O(n*W) where n is number of items and W is capacity

This problem appears frequently in:
- Resource allocation (CPU, memory, storage)
- Investment portfolio optimization
- Cargo loading and logistics
- Project selection under budget constraints
- Scheduling with limited time/resources

The binary (0/1) constraint of taking an item completely or not at all makes this harder than fractional knapsack, requiring dynamic programming rather than a greedy approach.

**Memoization (Top-Down)**:
```python
    def knapsack_memoization(weights: list[int], values: list[int], capacity: int) -> int:
        """
        Solves the 0/1 Knapsack problem using memoization (top-down DP).
        
        Args:
            weights: List of item weights
            values: List of item values 
            capacity: Maximum weight capacity
            
        Returns:
            Maximum value achievable within weight capacity
            
        Time Complexity: O(n*W) where n is number of items and W is capacity
        Space Complexity: O(n*W) for memoization dictionary
        """
        if not weights or not values or len(weights) != len(values):
            return 0
            
        n = len(weights)
        memo = {}  # Maps (item_index, remaining_capacity) to optimal value

        def dfs(i: int, remaining_cap: int) -> int:
            # Base cases
            if i == n:  # No more items to consider
                return 0
            if remaining_cap <= 0:  # No capacity left
                return 0
                
            # Check if subproblem already solved
            if (i, remaining_cap) in memo:
                return memo[(i, remaining_cap)]

            # Try excluding current item
            exclude_value = dfs(i + 1, remaining_cap)
            
            # Try including current item if possible
            include_value = 0
            if weights[i] <= remaining_cap:
                include_value = values[i] + dfs(i + 1, remaining_cap - weights[i])
            
            # Take maximum and cache result
            optimal_value = max(exclude_value, include_value)
            memo[(i, remaining_cap)] = optimal_value
            return optimal_value

        return dfs(0, capacity)

    # Example usage with different test cases
    weights = [2, 3, 4, 5]  # Item weights
    values = [3, 4, 5, 6]   # Corresponding values
    capacity = 5            # Knapsack capacity
    
    # Should return 7 (optimal solution takes items with weights 2,3 and values 3,4)
    print(knapsack_memoization(weights, values, capacity))
    
    # Edge cases
    print(knapsack_memoization([], [], 5))  # 0 (empty lists)
    print(knapsack_memoization([1], [10], 0))  # 0 (no capacity)
    print(knapsack_memoization([5], [10], 3))  # 0 (item too heavy)
```
**Tabulation (Bottom-Up)**:
```python
    def knapsack_tabulation(weights: list[int], values: list[int], capacity: int) -> int:
        """Solve 0/1 knapsack using bottom-up dynamic programming.
        
        Args:
            weights: List of item weights
            values: List of item values 
            capacity: Maximum weight capacity
            
        Returns:
            Maximum achievable value within weight capacity
            
        Time Complexity: O(n*W) where n is number of items and W is capacity
        Space Complexity: O(n*W) for dp table
        """
        if not weights or not values or len(weights) != len(values):
            return 0
            
        n = len(weights)
        # dp[i][w] represents max value achievable using first i items with capacity w
        dp = [[0]*(capacity+1) for _ in range(n+1)]

        # Build table bottom-up
        for i in range(1, n+1):
            for w in range(capacity+1):
                # Not taking item i-1 
                dp[i][w] = dp[i-1][w]
                
                # Taking item i-1 if possible
                if weights[i-1] <= w:
                    dp[i][w] = max(dp[i][w], 
                                values[i-1] + dp[i-1][w-weights[i-1]])

        return dp[n][capacity]

    # Example usage with different test cases
    weights = [2, 3, 4, 5]  # Item weights
    values = [3, 4, 5, 6]   # Corresponding values
    capacity = 5            # Knapsack capacity

    # Should return 7 (optimal solution takes items with weights 2,3 and values 3,4)
    print(knapsack_tabulation(weights, values, capacity))

    # Edge cases
    print(knapsack_tabulation([], [], 5))  # 0 (empty lists)
    print(knapsack_tabulation([1], [10], 0))  # 0 (no capacity)
    print(knapsack_tabulation([5], [10], 3))  # 0 (item too heavy)
```
---
### Coin Change (Minimum Coins)

The Coin Change problem (minimizing coins) is common in making change problems, currency systems, and combinational optimization tasks. Given a set of denominations and a target amount, we want the fewest coins to make that amount. If it can't be formed exactly, return -1.

Data Structures Used:
- Dynamic Programming Array/Table:
  - 1D array of size amount+1 storing minimum coins needed for each subproblem
  - dp[i] represents minimum coins needed for amount i
  - Enables O(1) lookup of previously solved subproblems
  - Critical for avoiding redundant calculations

- Set/Array for Coin Denominations:
  - Stores available coin values
  - Allows O(1) access to each denomination
  - Order doesn't matter since we try all combinations

The problem exhibits optimal substructure (minimum solution for amount n uses minimum solutions for smaller amounts) and overlapping subproblems (same smaller amounts calculated repeatedly), making it ideal for dynamic programming. Common applications include:
- Making change with minimum coins
- Currency exchange optimization
- Resource allocation problems
- Payment systems

**Memoization (Top-Down)**:

```python
    def coin_change_memo(coins: list[int], amount: int) -> int:
        """Find minimum number of coins needed to make given amount.
        
        Args:
            coins: List of coin denominations available
            amount: Target amount to make
            
        Returns:
            Minimum number of coins needed, or -1 if amount cannot be made
            
        Uses memoization (top-down DP) to avoid recalculating subproblems.
        Time complexity: O(amount * len(coins))
        Space complexity: O(amount) for memoization cache
        """
        # Cache to store minimum coins needed for each amount
        memo = {}
        
        def dfs(remaining: int) -> int:
            """Recursive helper with memoization."""
            # Base cases
            if remaining == 0:
                return 0
            if remaining < 0:
                return float('inf')
            if remaining in memo:
                return memo[remaining]
                
            # Try using each coin and take minimum
            min_coins = float('inf')
            for coin in coins:
                min_coins = min(min_coins, 1 + dfs(remaining - coin))
                
            # Cache result before returning
            memo[remaining] = min_coins
            return min_coins

        # Handle edge cases
        if not coins or amount < 0:
            return -1
            
        result = dfs(amount)
        return result if result != float('inf') else -1

    # Example usage with test cases
    test_cases = [
        ([1,2,5], 11),  # Should return 3 (5+5+1)
        ([2], 3),       # Should return -1 (impossible)
        ([1], 0),       # Should return 0 (empty sum)
        ([1,5,10,25], 30),  # Should return 3 (25+5)
        ([], 5)         # Should return -1 (no coins)
    ]

    for coins, amount in test_cases:
        result = coin_change_memo(coins, amount)
        print(f"Coins={coins}, Amount={amount}: {result}")
```

**Tabulation (Bottom-Up)**:

```python
def coin_change_tab(coins: list[int], amount: int) -> int:
    """
    Solves the coin change problem using tabulation (bottom-up DP).
    
    Args:
        coins: List of coin denominations
        amount: Target amount to make change for
        
    Returns:
        Minimum number of coins needed, or -1 if impossible
        
    Time Complexity: O(amount * len(coins))
    Space Complexity: O(amount) for dp array
    """
    # Handle edge cases
    if not coins or amount < 0:
        return -1
    if amount == 0:
        return 0
        
    # Initialize dp array with infinity
    # dp[i] represents min coins needed for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case - 0 coins needed for amount 0
    
    # Build up solution for each amount from 1 to target
    for curr_amount in range(1, amount + 1):
        # Try using each coin denomination
        for coin in coins:
            if coin <= curr_amount:
                # Take minimum of current solution and
                # 1 + solution for remaining amount
                dp[curr_amount] = min(
                    dp[curr_amount],
                    1 + dp[curr_amount - coin]
                )
                
    # Return -1 if no solution found
    return dp[amount] if dp[amount] != float('inf') else -1

# Example usage with test cases
test_cases = [
    ([1,2,5], 11),     # Should return 3 (5+5+1)
    ([2], 3),          # Should return -1 (impossible)
    ([1], 0),          # Should return 0 (empty sum)
    ([1,5,10,25], 30), # Should return 3 (25+5)
    ([], 5)            # Should return -1 (no coins)
]

for coins, amount in test_cases:
    result = coin_change_tab(coins, amount)
    print(f"Coins={coins}, Amount={amount}: {result}")
```
---
### Longest Common Subsequence (LCS)

The Longest Common Subsequence (LCS) problem finds the longest sequence of characters that appear in order in both strings. It has important applications in:

Data Structures Used:
- 2D DP Array/Dictionary:
  - Tabulation: dp[i][j] represents LCS length for prefixes s1[0:i], s2[0:j]
  - Memoization: Dictionary maps (i,j) positions to optimal LCS length
  - Enables O(1) lookup of subproblem solutions
  - Space complexity O(m*n) where m,n are string lengths
- Strings/Arrays:
  - Input sequences stored as strings/arrays for O(1) character access
  - Output LCS built by backtracking through DP array
  - Maintains character ordering for subsequence property

Common Applications:
- Bioinformatics: DNA/protein sequence alignment and comparison
- Version Control (diff): Finding common lines between file versions
- Spell Checking: Identifying similar words for suggestions
- Plagiarism Detection: Finding shared text between documents
- File Comparison: Detecting similarities in text files

The dynamic programming approach is necessary because the problem exhibits:
- Optimal substructure (solution built from smaller subproblems)
- Overlapping subproblems (same subproblems solved repeatedly)

**Memoization (Top-Down)**:

```python
    def lcs_memo(s1: str, s2: str) -> int:
        """
        Find length of Longest Common Subsequence using memoization.
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Length of longest common subsequence
            
        Time Complexity: O(m*n) where m,n are string lengths
        Space Complexity: O(m*n) for memoization dictionary
        """
        # Handle edge cases
        if not s1 or not s2:
            return 0
            
        memo = {}  # Cache for subproblems
        
        def dfs(i: int, j: int) -> int:
            """Recursive helper with memoization"""
            # Base case - reached end of either string
            if i == len(s1) or j == len(s2):
                return 0
                
            # Return cached result if available
            if (i,j) in memo:
                return memo[(i,j)]
            
            # If characters match, include in LCS and move both pointers
            if s1[i] == s2[j]:
                memo[(i,j)] = 1 + dfs(i+1, j+1)
            else:
                # Characters don't match - try both possibilities
                # and take maximum
                memo[(i,j)] = max(
                    dfs(i+1, j),  # Skip character in s1
                    dfs(i, j+1)   # Skip character in s2
                )
            return memo[(i,j)]
            
        return dfs(0, 0)

    # Example usage with different test cases
    test_cases = [
        ("abcde", "ace"),     # 3 (ace)
        ("abc", "abc"),       # 3 (abc) 
        ("abc", "def"),       # 0 (no common subsequence)
        ("", "abc"),          # 0 (empty string)
        ("long", "stone"),    # 3 (lon)
    ]

    for s1, s2 in test_cases:
        result = lcs_memo(s1, s2)
        print(f"LCS length of '{s1}' and '{s2}': {result}")

```

**Tabulation (Bottom-Up)**:

```python
def lcs_tab(s1: str, s2: str) -> int:
    """
    Finds length of Longest Common Subsequence using tabulation (bottom-up DP).
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Length of longest common subsequence
        
    Time Complexity: O(m*n) where m,n are string lengths
    Space Complexity: O(m*n) for dp table
    """
    # Handle edge cases
    if not s1 or not s2:
        return 0
        
    # Create dp table with extra row/col for empty string base case
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    
    # Fill dp table bottom-up
    for i in range(m-1, -1, -1):
        for j in range(n-1, -1, -1):
            if s1[i] == s2[j]:
                # Characters match - include in LCS
                dp[i][j] = 1 + dp[i+1][j+1]
            else:
                # Characters don't match - take max of skipping either
                dp[i][j] = max(dp[i+1][j], dp[i][j+1])
                
    return dp[0][0]

# Example usage with different test cases
test_cases = [
    ("abcde", "ace"),     # 3 (ace)
    ("abc", "abc"),       # 3 (abc)
    ("abc", "def"),       # 0 (no common subsequence) 
    ("", "abc"),          # 0 (empty string)
    ("long", "stone"),    # 3 (lon)
]

for s1, s2 in test_cases:
    result = lcs_tab(s1, s2)
    print(f"LCS length of '{s1}' and '{s2}': {result}")

```

---

### DP considerations

**When to Use Memoization (Top-Down)**:

Memoization is often more intuitive if you think recursively: define a recursive function that computes the answer for a subproblem and store the results. It’s useful if you find it easier to start from the original problem and break it down into subproblems. Memoization can also be beneficial when you only need to solve a subset of possible subproblems (not all of them), potentially saving work.

**When to Use Tabulation (Bottom-Up)**:

Tabulation requires you to identify the order in which to fill in a DP table starting from base cases. It can be more efficient and sometimes simpler once you know the exact dependencies between subproblems. If you know you’ll need to compute the answers for all subproblems, bottom-up can be cleaner and might have slightly better constants since it avoids the overhead of recursion and hashing for memoization.

**Where DP Is Used**:

DP is used in a wide variety of scenarios:

- Optimization problems (maximizing or minimizing some value, e.g., knapsack, coin change)
- Counting problems (number of ways to achieve something, e.g., counting paths, counting combinations)
- Sequence problems (finding longest subsequences, edit distances)
- Graph algorithms (shortest paths in special cases, e.g. DAGs)
- Scheduling and resource allocation (splitting tasks to optimize time or cost)
- Text processing and biological sequence alignment (LCS, edit distance)

In essence, DP is particularly useful when:

- The problem can be broken down into smaller overlapping subproblems.
- There is an optimal substructure: the optimal solution can be constructed from optimal solutions to subproblems.
- There is no simple greedy choice that always leads to an optimal solution.

## More Greedy Algorithms
### Huffman Coding (Tree construction)

Description: Huffman coding constructs an optimal prefix-free binary code by building a special binary tree. Key features:

Data Structures Used:
- Min Heap (Priority Queue):
  - Stores nodes prioritized by frequency
  - Enables efficient O(log n) selection of minimum frequency nodes
  - Critical for greedy selection of nodes to merge
  
- Binary Tree:
  - Internal nodes store merged frequencies
  - Leaf nodes contain characters
  - Left/right edges represent 0/1 bits
  - Path from root to leaf gives character's code
  
- Hash Map/Dictionary:
  - Maps characters to frequencies initially
  - Later maps characters to binary codes
  - Provides O(1) lookups
  
The algorithm works by repeatedly merging the two lowest frequency nodes until a single tree remains. This greedy approach guarantees an optimal prefix-free code that minimizes the weighted path lengths (bits per character). Common applications include:
- Text compression
- Data compression
- File compression algorithms
- Network protocols

Below is a code snippet for building the Huffman tree and printing the optimal binary codes.

```python
    import heapq
    from collections import defaultdict

    class HuffmanNode:
        """Node in Huffman tree containing character, frequency and children"""
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None
            
        def __lt__(self, other):
            # For heap comparison
            return self.freq < other.freq

    def build_huffman_tree(text):
        """Build Huffman tree from input text"""
        # Count frequencies
        freq = defaultdict(int)
        for char in text:
            freq[char] += 1
            
        # Create leaf nodes and add to min heap
        heap = []
        for char, count in freq.items():
            node = HuffmanNode(char, count)
            heapq.heappush(heap, node)
            
        # Merge nodes until only root remains
        while len(heap) > 1:
            # Get two minimum frequency nodes
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # Create internal node with combined frequency
            internal = HuffmanNode(None, left.freq + right.freq)
            internal.left = left
            internal.right = right
            
            # Add back to heap
            heapq.heappush(heap, internal)
            
        return heap[0]

    def generate_codes(root, code="", codes=None):
        """Generate binary codes for each character by traversing tree"""
        if codes is None:
            codes = {}
            
        # Leaf node - store code
        if root.char is not None:
            codes[root.char] = code
            return
            
        # Traverse left (0) and right (1)
        generate_codes(root.left, code + "0", codes)
        generate_codes(root.right, code + "1", codes)
        return codes

    def huffman_encoding(text):
        """Encode text using Huffman coding"""
        # Handle empty input
        if not text:
            return "", None
            
        # Build tree and generate codes
        root = build_huffman_tree(text)
        codes = generate_codes(root)
        
        # Encode text
        encoded = "".join(codes[char] for char in text)
        return encoded, root

    # Example usage
    text = "this is an example for huffman encoding"
    encoded, tree = huffman_encoding(text)

    # Huffman Tree Structure (ASCII representation):
    #                    (42)
    #                   /    \
    #                (18)    (24)
    #               /    \   /   \
    #            (8)    (10)(11) (13)
    #           /   \    |   |    |
    #         (3)   (5) (t) (s)  (e)
    #         / \    |
    #       (h) (i)  (a)

    print("Original text:", text)  
    # Output: 
    # Original text: this is an example for huffman encoding

    print("Huffman Codes:", generate_codes(tree))  
    # Output: 
    # Huffman Codes: {
    #     'h': '110',    'i': '101',    'a': '011',
    #     't': '1101',   's': '1100',   'e': '1110',
    #     ' ': '11',     'f': '100',    'm': '1110',
    #     'n': '010',    'c': '1111',   'o': '1110',
    #     'd': '1111',   'g': '1111',   'u': '1111',
    #     'x': '1111'
    # }

    print("Encoded text:", encoded)
    # Output:
    # Encoded text: 
    # 110110101100101100011010100110011011110011001111101100100111111010100101101110010110011
```