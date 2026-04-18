import requests as req
from termcolor import colored

class TodoAPI:
    """
    Problem Type: API Interaction, HTTP Requests
    
    Problem Statement:
    Using the JSONPlaceholder API (https://jsonplaceholder.typicode.com/todos/), implement a class to interact with the API and demonstrate the functions of the requests package. The class should be able to fetch all todos, fetch a single todo by ID, create a new todo, update an existing todo, and delete a todo.
    
    Methods:
    __init__(): Initializes the TodoAPI class.
    __repr__(): Returns a string representation of the TodoAPI instance.
    fetch_all_todos(): Fetches all todos from the API.
    fetch_todo_by_id(todo_id): Fetches a single todo by its ID.
    create_todo(title, completed, user_id): Creates a new todo with the given title, completed status, and user ID.
    update_todo(todo_id, title=None, completed=None, user_id=None): Updates an existing todo with the given ID. Only the provided fields will be updated.
    delete_todo(todo_id): Deletes a todo with the given ID.
    
    Example:
    api = TodoAPI()
    api.fetch_all_todos()
    api.fetch_todo_by_id(1)
    api.create_todo("New Todo", False, 1)
    api.update_todo(1, completed=True)
    api.delete_todo(1)
    
    Diagram:
    
        +-------------------+
        |   TodoAPI Class   |
        +-------------------+
        | - __init__        |
        | - __repr__        |
        | - fetch_all_todos |
        | - fetch_todo_by_id|
        | - create_todo     |
        | - update_todo     |
        | - delete_todo     |
        +-------------------+
    """
    
    BASE_URL = "https://jsonplaceholder.typicode.com/todos"
    
    def __init__(self):
        """
        Initializes the TodoAPI class.
        """
        pass
    
    def __repr__(self):
        """
        Returns a string representation of the TodoAPI instance.
        """
        return f"TodoAPI(BASE_URL={self.BASE_URL})"
    
    def fetch_all_todos(self):
        """
        Fetches the first 15 todos from the API.
        
        Returns:
        List[Dict]: A list of the first 15 todos.
        """
        response = req.get(f"{self.BASE_URL}?_limit=15")
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def fetch_todo_by_id(self, todo_id):
        """
        Fetches a single todo by its ID.
        
        Parameters:
        todo_id (int): The ID of the todo to fetch.
        
        Returns:
        Dict: The todo with the given ID.
        """
        response = req.get(f"{self.BASE_URL}/{todo_id}?_limit=1")
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def create_todo(self, title, completed, user_id):
        """
        Creates a new todo with the given title, completed status, and user ID.
        
        Parameters:
        title (str): The title of the new todo.
        completed (bool): The completed status of the new todo.
        user_id (int): The user ID associated with the new todo.
        
        Returns:
        Dict: The created todo.
        """
        payload = {
            "title": title,
            "completed": completed,
            "userId": user_id
        }
        response = req.post(self.BASE_URL, json=payload)
        # Check if the request was successful
        if response.status_code == 201:
            return response.json()
        else:
            response.raise_for_status()
    
    def update_todo(self, todo_id, title=None, completed=None, user_id=None):
        """
        Updates an existing todo with the given ID. Only the provided fields will be updated.
        
        Parameters:
        todo_id (int): The ID of the todo to update.
        title (str, optional): The new title of the todo.
        completed (bool, optional): The new completed status of the todo.
        user_id (int, optional): The new user ID associated with the todo.
        
        Returns:
        Dict: The updated todo.
        """
        payload = {}
        if title is not None:
            payload["title"] = title
        if completed is not None:
            payload["completed"] = completed
        if user_id is not None:
            payload["userId"] = user_id
        
        response = req.put(f"{self.BASE_URL}/{todo_id}", json=payload)
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def delete_todo(self, todo_id):
        """
        Deletes a todo with the given ID.
        
        Parameters:
        todo_id (int): The ID of the todo to delete.
        
        Returns:
        None
        """
        response = req.delete(f"{self.BASE_URL}/{todo_id}")
        # Check if the request was successful
        if response.status_code == 200:
            return {"message": "Todo deleted successfully"}
        else:
            response.raise_for_status()


api = TodoAPI()

import json
print(colored(json.dumps(api.fetch_all_todos(), indent=4), 'green'), end="\n\n")
print("---Delete a todo---")
print(colored(json.dumps(api.delete_todo(1), indent=4), 'green'), end="\n\n")
print("---Fetch all todos---")
print(colored(json.dumps(api.fetch_all_todos(), indent=4), 'green'), end="\n\n")
print("---Fetch a todo by id---")
print(colored(json.dumps(api.fetch_todo_by_id(1), indent=4), 'green'), end="\n\n")
print("---Create a new todo---")
print(colored(json.dumps(api.create_todo("New Todo", False, 1), indent=4), 'green'), end="\n\n")
print("---Fetch all todos---")
print(colored(json.dumps(api.fetch_all_todos(), indent=4), 'green'), end="\n\n")
print("---Update a todo---")
print(colored(json.dumps(api.update_todo(1, completed=True), indent=4), 'green'), end="\n\n")
print("---Fetch all todos---")
print(colored(json.dumps(api.fetch_all_todos(), indent=4), 'green'), end="\n\n")

