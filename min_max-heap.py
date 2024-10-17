import heapq
from termcolor import colored

class MinHeap:
    def __init__(self, arr):
        self.heap = arr
        heapq.heapify(self.heap)

    def __repr__(self):
        return colored(f"Min-Heap: {self.heap}", 'green')

    def pop(self):
        smallest = heapq.heappop(self.heap)
        print(colored(f"Popped element: {smallest}", 'yellow'))
        return smallest

    def push(self, element):
        heapq.heappush(self.heap, element)
        print(colored(f"Heap after push: {self.heap}", 'blue'))

    def __call__(self):
        print(self)

class MaxHeap:
    def __init__(self, arr):
        self.heap = [-num for num in arr]
        heapq.heapify(self.heap)

    def __repr__(self):
        return colored(f"Max-Heap: {[-num for num in self.heap]}", 'green')

    def pop(self):
        largest = -heapq.heappop(self.heap)
        print(colored(f"Popped element: {largest}", 'yellow'))
        return largest

    def __call__(self):
        print(self)

# Example usage:
arr = [10, 1, 4, 6, 8, 5]

min_heap = MinHeap(arr[:])
min_heap()
min_heap.pop()
min_heap.push(2)
min_heap()

max_heap = MaxHeap(arr[:])
max_heap()
max_heap.pop()
max_heap()
