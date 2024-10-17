from concurrent.futures import ThreadPoolExecutor
import threading
import time
import random
from termcolor import colored

class MeetingRoomScheduler:
    """
    Problem Type: Meeting Room Scheduling (Overlapping Intervals)
    
    Problem Statement:
    Simulate a real-world meeting room scheduling system where multiple users can book and cancel meeting rooms concurrently. Ensure that the system can handle a large number of users (e.g., a million plus) without deadlock or performance degradation.
    
    Parameters:
    max_rooms (int): The maximum number of meeting rooms available.
    
    Methods:
    __init__(max_rooms): Initializes the scheduler with a maximum number of meeting rooms.
    __call__(user_id, start_time, end_time): Allows a user to book a meeting room.
    __repr__(): Returns a string representation of the MeetingRoomScheduler instance.
    __len__(): Returns the number of meeting rooms currently booked.
    book_room(user_id, start_time, end_time): Allows a user to book a meeting room.
    cancel_booking(user_id, start_time, end_time): Allows a user to cancel a booking.
    get_bookings(): Returns a list of all current bookings.
    
    Example:
    scheduler = MeetingRoomScheduler(max_rooms=10)
    user_id = 1
    scheduler(user_id, "10:00", "11:00")
    scheduler.cancel_booking(user_id, "10:00", "11:00")
    
    Diagram:
    
        +-------------------------+
        | MeetingRoomScheduler    |
        +-------------------------+
        | - __init__              |
        | - __call__              |
        | - __repr__              |
        | - __len__               |
        | - book_room             |
        | - cancel_booking        |
        | - get_bookings          |
        +-------------------------+
    """
    
    def __init__(self, max_rooms):
        self.max_rooms = max_rooms
        self.bookings = []
        self.lock = threading.Lock()
    
    def book_room(self, user_id, start_time, end_time):
        """
        Allows a user to book a meeting room.
        
        Parameters:
        user_id (int): The ID of the user booking the room.
        start_time (str): The start time of the booking.
        end_time (str): The end time of the booking.
        
        Returns:
        bool: True if the booking is successful, False otherwise.
        """
        with self.lock:
            if len(self.bookings) < self.max_rooms:
                self.bookings.append((user_id, start_time, end_time))
                print(colored(f"User {user_id} booked a room from {start_time} to {end_time}.", 'green'), end="\n\n")
                return True
            else:
                print(colored("No available rooms for booking.", 'red'), end="\n\n")
                return False
    
    def cancel_booking(self, user_id, start_time, end_time):
        """
        Allows a user to cancel a booking.
        
        Parameters:
        user_id (int): The ID of the user canceling the booking.
        start_time (str): The start time of the booking.
        end_time (str): The end time of the booking.
        """
        with self.lock:
            booking = (user_id, start_time, end_time)
            if booking in self.bookings:
                self.bookings.remove(booking)
                print(colored(f"User {user_id} canceled the booking from {start_time} to {end_time}.", 'red'), end="\n\n")
    
    def __call__(self, user_id, start_time, end_time):
        """
        Allows a user to book a meeting room.
        
        Parameters:
        user_id (int): The ID of the user booking the room.
        start_time (str): The start time of the booking.
        end_time (str): The end time of the booking.
        """
        return self.book_room(user_id, start_time, end_time)
    
    def __repr__(self):
        """
        Returns a string representation of the MeetingRoomScheduler instance.
        """
        return f"MeetingRoomScheduler(max_rooms={self.max_rooms}, current_bookings={len(self.bookings)})"
    
    def __len__(self):
        """
        Returns the number of meeting rooms currently booked.
        
        Returns:
        int: The number of meeting rooms booked.
        """
        return len(self.bookings)
    
    def get_bookings(self):
        """
        Returns a list of all current bookings.
        
        Returns:
        List[Tuple[int, str, str]]: A list of all current bookings.
        """
        with self.lock:
            return self.bookings.copy()

def user_interaction(scheduler, user_id):
    try:
        time.sleep(random.uniform(0.1, 1.0))
        start_time = f"{random.randint(9, 16):02d}:00"
        end_time = f"{int(start_time.split(':')[0]) + 1:02d}:00"
        scheduler(user_id, start_time, end_time)
        time.sleep(random.uniform(0.1, 1.0))
        if random.choice([True, False]):  # 50% chance to cancel
            scheduler.cancel_booking(user_id, start_time, end_time)
    except Exception as e:
        print(colored(f"Error for user {user_id}: {e}", 'red'), end="\n\n")

# Simulate multiple users
scheduler = MeetingRoomScheduler(max_rooms=5)
num_users = 20

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(user_interaction, scheduler, i) for i in range(num_users)]

    # Wait for all tasks to complete
    for future in futures:
        future.result()

print(colored(f"Final state: {scheduler}", 'blue'))
final_bookings = scheduler.get_bookings()
for booking in final_bookings:
    print(colored(f"Booking details - User ID: {booking[0]}, Start Time: {booking[1]}, End Time: {booking[2]}", 'blue'))
