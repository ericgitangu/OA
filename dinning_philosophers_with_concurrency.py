from concurrent.futures import ThreadPoolExecutor
import threading
from termcolor import colored
import time

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
    
    Approach:
    To ensure that all philosophers get a chance to eat and to avoid race conditions, we use the following approach:
    1. Each fork is represented by a threading.Lock() to ensure mutual exclusion when a philosopher picks up a fork.
    2. Philosophers always pick up the lower-numbered fork first to avoid deadlock. This means that if a philosopher's left fork has a lower number than their right fork, they will pick up the left fork first, and vice versa.
    3. We use a ThreadPoolExecutor to manage the concurrent execution of the philosophers' actions, ensuring that multiple philosophers can attempt to eat simultaneously without causing race conditions.
    4. The use of context managers (with statements) ensures that forks are properly acquired and released, maintaining thread safety.
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
        start_time = time.time()
        with self.forks[first_fork]:
            with self.forks[second_fork]:
                pick_left_fork(philosopher)
                pick_right_fork(philosopher)
                eat(philosopher)
                put_left_fork(philosopher)
                put_right_fork(philosopher)
            end_time = time.time()
            print(colored(f"-" * 100, "blue"), flush=True)
            print(colored(f"\nPhilosopher {philosopher + 1} finished eating in {end_time - start_time:.4f} seconds", "green"))
            
# Implementation of the functions:
def pick_left_fork(philosopher):
    print(colored(f"\nPhilosopher {philosopher + 1} picked up left fork 👈", "magenta"))

def pick_right_fork(philosopher):
    print(colored(f"\nPhilosopher {philosopher + 1} picked up right fork 👉", "green"))

def eat(philosopher):
    print(colored(f"\nPhilosopher {philosopher + 1} is eating", "yellow"))

def put_left_fork(philosopher):
    print(colored(f"\nPhilosopher {philosopher + 1} put down left fork", "green"))

def put_right_fork(philosopher):
    print(colored(f"\nPhilosopher {philosopher + 1} put down right fork", "green"))
PHILOSOPHERS = 5
philosophers = DiningPhilosophers(PHILOSOPHERS)
print(philosophers)
with ThreadPoolExecutor(max_workers=PHILOSOPHERS) as executor:
    for i in range(PHILOSOPHERS):
        print(colored("\nPhilosopher {} is thinking 🤔".format(i + 1), "blue"), flush=True)
        executor.submit(philosophers.wants_to_eat, i, pick_left_fork, pick_right_fork, eat, put_left_fork, put_right_fork)
        print(colored("\nPhilosopher {} finished thinking 🤔".format(i + 1), "blue"), flush=True)
