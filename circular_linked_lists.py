class CircularListNode:
    def __init__(self, value=0, next=None):
        # Initialize a node with a given value and a reference to the next node
        self.value = value
        self.next = next

    def __iter__(self):
        # Initialize the iterator by setting the current node to self and a flag to check if iteration started
        self.current = self
        self.started = False
        return self

    def __next__(self):
        # If the current node is None or we have looped back to the start node and already started, stop iteration
        if self.current is None or (self.current == self and self.started):
            raise StopIteration
        # Mark that we have started the iteration
        self.started = True
        # Store the value of the current node
        value = self.current.value
        # Move to the next node
        self.current = self.current.next
        # Return the stored value
        return value

    def __repr__(self):
        # Create a list to store the string representation of each node's value
        nodes = []
        current = self
        while True:
            # Append the current node's value to the list
            nodes.append(str(current.value))
            # Move to the next node
            current = current.next
            # If we have looped back to the start node, break the loop
            if current == self:
                break
        # Return a string representation of the circular linked list
        return " -> ".join(nodes) + " -> " + str(self.value) + " (loop)"

def traverse_circular_linked_list(head):
    """
    Problem Type: Linked List Traversal, Circular Linked List
    
    Problem Statement:
    Given the head of a circular linked list, traverse the list and return the __repr__ of the nodes.
    
    Parameters:
    head (CircularListNode): The head node of the circular linked list.
    
    Returns:
    str: The __repr__ of the nodes in the circular linked list.
    
    Example:
    head = CircularListNode(1)
    head.next = CircularListNode(2, CircularListNode(3, CircularListNode(4, head)))
    traverse_circular_linked_list(head) -> '1 -> 2 -> 3 -> 4 -> 1 (loop)'
    
    Diagram:
    
        1 -> 2 -> 3 -> 4
             ^         |
             |_________|
    """
    # Return the string representation of the circular linked list using the __repr__ method
    return repr(head)

# Example usage:
head = CircularListNode(1)
# Create a circular linked list: 1 -> 2 -> 3 -> 4 -> 1 (loop)
head.next = CircularListNode(2, CircularListNode(3, CircularListNode(4, head)))
# Print the string representation of the circular linked list
print(traverse_circular_linked_list(head))  # Output: '1 -> 2 -> 3 -> 4 -> 1 (loop)'

# Print the string representation of the head node, which will show the entire list
print(head)
