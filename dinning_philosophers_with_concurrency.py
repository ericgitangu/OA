from concurrent.futures import ThreadPoolExecutor
import threading
from termcolor import colored

class DiningPhilosophers:
    """
    Problem Type: Synchronization, Dining Philosophers Problem
    
    Problem Statement:
    The Dining Philosophers problem is a classic synchronization problem. It involves a certain number of philosophers sitting at a table, each with a plate of food and a fork on either side. A philosopher needs both forks to eat, but can only pick up one fork at a time. The problem is to design a protocol that the philosophers can use to avoid deadlock and starvation.
    
    Parameters:
    n (int): The number of philosophers.
    
    Methods:
    wants_to_eat(philosopher, pick_left_fork, pick_right_fork, eat, put_left_fork, put_right_fork): The method that simulates a philosopher wanting to eat.
    
    Example:
    philosophers = DiningPhilosophers(5)
    philosophers.wants_to_eat(0, pick_left_fork, pick_right_fork, eat, put_left_fork, put_right_fork)
    
    Diagram:
    
    The Dining Philosophers problem:
    
        P0          P1
       /  \        /  \
      F0   F1    F1   F2
     /        \ /        \
    P4        P2        P3
    \        / \        /
     F4   F3    F3   F4
       \  /        \  /
        P4          P3
    
    Each philosopher needs both forks to eat, but can only pick up one fork at a time.
    """
    
    def __init__(self, n):
        self.n = n
        self.forks = [threading.Lock() for _ in range(n)]

    def __repr__(self):
        return colored(f'DiningPhilosophers(n={self.n}\n', 'magenta')

    def wants_to_eat(self, philosopher, pick_left_fork, pick_right_fork, eat, put_left_fork, put_right_fork):
        left_fork = philosopher
        right_fork = (philosopher + 1) % self.n

        # Ensure thread safety by always picking up the lower-numbered fork first
        first_fork, second_fork = (left_fork, right_fork) if left_fork < right_fork else (right_fork, left_fork)

        with self.forks[first_fork]:
            with self.forks[second_fork]:
                pick_left_fork()
                pick_right_fork()
                eat()
                put_left_fork()
                put_right_fork()

# Example usage:
def pick_left_fork():
    print(colored("Picked up left fork", "green"))

def pick_right_fork():
    print(colored("Picked up right fork", "green"))

def eat():
    print(colored("Eating", "yellow"))

def put_left_fork():
    print(colored("Put down left fork", "red"))

def put_right_fork():
    print(colored("Put down right fork", "red"))

philosophers = DiningPhilosophers(5)
print(philosophers)
with ThreadPoolExecutor(max_workers=5) as executor:
    for i in range(5):
        executor.submit(philosophers.wants_to_eat, i, pick_left_fork, pick_right_fork, eat, put_left_fork, put_right_fork)

