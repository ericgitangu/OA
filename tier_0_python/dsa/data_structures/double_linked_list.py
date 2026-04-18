from termcolor import colored

class DoublyListNode:
    def __init__(self, value=0, next=None, prev=None):
        self.value = value
        self.next = next
        self.prev = prev

    def __repr__(self):
        return f"DoublyListNode(value={self.value})"

def traverse_doubly_linked_list(head):
    """
    Problem Type: Linked List Traversal, Doubly-Linked List
    
    Problem Statement:
    Given the head of a doubly-linked list, traverse the list and print the value of each node in order.
    
    Parameters:
    head (DoublyListNode): The head node of the doubly-linked list.
    
    Returns:
    None: The function prints the values of the nodes in the doubly-linked list in order.
    
    Example:
    head = DoublyListNode(1, DoublyListNode(2, DoublyListNode(3, DoublyListNode(4))))
    traverse_doubly_linked_list(head) -> 1 <-> 2 <-> 3 <-> 4 <-> None
    """
    current = head
    while current:
        print(colored(current.value, 'cyan'), end=colored(" <-> ", 'yellow'))
        current = current.next
    print(colored("None", 'red'))

# Example usage:
head = DoublyListNode(1, DoublyListNode(2, DoublyListNode(3, DoublyListNode(4))))
traverse_doubly_linked_list(head)  # Output: 1 <-> 2 <-> 3 <-> 4 <-> None

class CircularListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next