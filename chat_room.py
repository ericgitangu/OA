from concurrent.futures import ThreadPoolExecutor
import threading
import time
import random
from termcolor import colored

class ChatRoom:
    """
    Problem Type: Real-time Communication, Synchronization
    
    Problem Statement:
    Simulate a real-world chat room where multiple users can send and receive messages concurrently. Ensure that the system can handle a large number of users (e.g., a million plus) without deadlock or performance degradation.
    
    Parameters:
    max_users (int): The maximum number of users that can join the chat room.
    
    Methods:
    __init__(max_users): Initializes the chat room with a maximum number of users.
    __call__(user_id, message): Allows a user to send a message to the chat room.
    __repr__(): Returns a string representation of the ChatRoom instance.
    __len__(): Returns the number of users currently in the chat room.
    join(user_id): Allows a user to join the chat room.
    leave(user_id): Allows a user to leave the chat room.
    receive_messages(user_id): Allows a user to receive messages from the chat room.
    
    Example:
    chat_room = ChatRoom(max_users=1000000)
    user_id = chat_room.join()
    chat_room(user_id, "Hello, World!")
    messages = chat_room.receive_messages(user_id)
    chat_room.leave(user_id)
    
    Diagram:
    
        +-------------------+
        |    ChatRoom       |
        +-------------------+
        | - __init__        |
        | - __call__        |
        | - __repr__        |
        | - __len__         |
        | - join            |
        | - leave           |
        | - receive_messages|
        +-------------------+
    """
    
    def __init__(self, max_users):
        self.max_users = max_users
        self.users = set()
        self.messages = []
        self.lock = threading.Lock()
        self.message_event = threading.Event()
    
    def join(self):
        """
        Allows a user to join the chat room.
        
        Returns:
        int: The ID of the user joining the chat room.
        """
        user_id = random.randint(1, self.max_users)
        with self.lock:
            if len(self.users) < self.max_users:
                self.users.add(user_id)
                print(colored(f"User {user_id} joined the chat room.", 'green'), end="\n\n")
                return user_id
            else:
                raise Exception("Chat room is full.")
    
    def leave(self, user_id):
        """
        Allows a user to leave the chat room.
        
        Parameters:
        user_id (int): The ID of the user leaving the chat room.
        """
        with self.lock:
            if user_id in self.users:
                self.users.remove(user_id)
                print(colored(f"User {user_id} left the chat room.", 'red'), end="\n\n")
    
    def __call__(self, user_id, message):
        """
        Allows a user to send a message to the chat room.
        
        Parameters:
        user_id (int): The ID of the user sending the message.
        message (str): The message to be sent.
        """
        with self.lock:
            if user_id in self.users:
                self.messages.append((user_id, message))
                self.message_event.set()
                print(colored(f"User {user_id} sent a message: {message}", 'blue'), end="\n\n")
    
    def __repr__(self):
        """
        Returns a string representation of the ChatRoom instance.
        """
        return f"ChatRoom(max_users={self.max_users}, current_users={len(self.users)})"
    
    def __len__(self):
        """
        Returns the number of users currently in the chat room.
        
        Returns:
        int: The number of users in the chat room.
        """
        return len(self.users)
    
    def receive_messages(self, user_id):
        """
        Allows a user to receive messages from the chat room.
        
        Parameters:
        user_id (int): The ID of the user receiving messages.
        
        Returns:
        List[Tuple[int, str]]: A list of messages received by the user.
        """
        received_messages = []
        with self.lock:
            if user_id in self.users:
                received_messages = self.messages.copy()
                self.message_event.clear()
        return received_messages

# Example usage:
def user_interaction(chat_room):
    try:
        user_id = chat_room.join()
        time.sleep(random.uniform(0.1, 1.0))
        messages = [
            "Hello, World!",
            "How's everyone doing?",
            "What's up?",
            "Good morning!",
            "Good night!",
            "Have a great day!",
            "See you later!",
            "Take care!",
            "Nice to meet you!",
            "Welcome to the chat room!"
        ]
        message = random.choice(messages)
        chat_room(user_id, message)
        time.sleep(random.uniform(0.1, 1.0))
        received_messages = chat_room.receive_messages(user_id)
        print(colored(f"User {user_id} received messages: {received_messages}", 'yellow'), end="\n\n")
        chat_room.leave(user_id)
    except Exception as e:
        print(colored(e, 'red'), end="\n\n")

chat_room = ChatRoom(max_users=1000000)

# Using ThreadPoolExecutor to simulate multiple users interacting with the chat room
num_users = 10  # For demonstration purposes, using 10 users
with ThreadPoolExecutor(max_workers=num_users) as executor:
    for _ in range(num_users):
        executor.submit(user_interaction, chat_room)

# Explanation:
# - The ThreadPoolExecutor is used to simulate multiple users interacting with the chat room concurrently.
# - The number of workers is set to the number of users to ensure that each user gets a dedicated thread for interaction.
# - The lock is used to ensure thread safety when users join, leave, send messages, and receive messages.
# - The message_event is used to signal when a new message is sent, allowing users to receive messages in real-time.
# - Dunder methods (__call__, __repr__, __len__) are used to provide a more Pythonic interface for the ChatRoom class.
