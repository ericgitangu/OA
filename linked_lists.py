from termcolor import colored

class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"ListNode(value={self.value})"

def traverse_linked_list(head):
    """
    Problem Type: Linked List Traversal
    
    Problem Statement:
    Given the head of a linked list, traverse the linked list and print the value of each node in order.
    
    Parameters:
    head (ListNode): The head node of the linked list.
    
    Returns:
    None: The function prints the values of the nodes in the linked list in order.
    
    Example:
    head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
    traverse_linked_list(head) -> 1 -> 2 -> 3 -> 4 -> None
    
    Diagram:
    
        1 -> 2 -> 3 -> 4 -> None
    """
    current = head
    while current:
        print(colored(current.value, 'cyan'), end=colored(" -> ", 'yellow'))
        current = current.next
    print(colored("None", 'red'))

# Example usage:
head = ListNode(1, ListNode(2, ListNode(3, ListNode(4))))
traverse_linked_list(head)  # Output: 1 -> 2 -> 3 -> 4 -> None
