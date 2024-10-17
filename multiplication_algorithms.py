from termcolor import colored
import time

class MultiplicationAlgorithms:
    def __init__(self, num1, num2):
        # Initialize the class with two numbers to be multiplied
        self.num1 = num1
        self.num2 = num2

    def __repr__(self):
        # Return a string representation of the MultiplicationAlgorithms instance
        return f"MultiplicationAlgorithms:\n  - First Number: {self.num1}\n  - Second Number: {self.num2}"

    def naive_multiplication(self):
        """
        Naive multiplication algorithm.
        
        Approach:
        The naive multiplication algorithm multiplies two numbers by adding one number to itself repeatedly.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        result = 0
        # Add num1 to result abs(num2) times
        for _ in range(abs(self.num2)):
            result += self.num1
        # If num2 is negative, negate the result
        if self.num2 < 0:
            result = -result
        return f"Naive Multiplication Result: {result}"

    def python_multiplication(self):
        """
        Python multiplication algorithm.
        
        Approach:
        The Python multiplication algorithm uses the built-in multiplication operator (*).
        This operator is implemented in C for CPython, making it highly optimized for performance.
        It handles both integer and floating-point multiplication, as well as complex numbers.
        
        For integers, the multiplication is performed using the Karatsuba algorithm for large numbers,
        and a simple O(1) multiplication for small numbers.
        
        For floating-point numbers, the multiplication is performed using the IEEE 754 standard.
        
        Time Complexity: O(1) for small numbers, O(n^1.585) for large integers
        Space Complexity: O(1)
        """
        return f"Python Multiplication Result: {self.num1 * self.num2}"

    def karatsuba_multiplication(self):
        """
        Karatsuba multiplication algorithm.
        
        Approach:
        The Karatsuba algorithm multiplies two numbers using a divide-and-conquer approach.
        
        Time Complexity: O(n^log2(3)) ≈ O(n^1.585)
        Space Complexity: O(n)
        """
        # Call the recursive Karatsuba multiplication function
        return f"Karatsuba Multiplication Result: {self._karatsuba(self.num1, self.num2)}"

    def _karatsuba(self, x, y):
        # Base case for recursion: if either number is less than 10, return the product
        if x < 10 or y < 10:
            return x * y
        # Determine the size of the numbers
        n = max(len(str(x)), len(str(y)))
        # Split the size in half
        m = n // 2
        # Split the numbers into high and low parts
        x_high, x_low = divmod(x, 10**m)
        y_high, y_low = divmod(y, 10**m)
        # Recursively calculate three products
        z0 = self._karatsuba(x_low, y_low)
        z1 = self._karatsuba((x_low + x_high), (y_low + y_high))
        z2 = self._karatsuba(x_high, y_high)
        # Combine the three products to get the final result
        return (z2 * 10**(2*m)) + ((z1 - z2 - z0) * 10**m) + z0

    def __call__(self, algorithm_name):
        # Dictionary of available algorithms
        algorithms = {
            "Naive Multiplication": self.naive_multiplication,
            "Karatsuba Multiplication": self.karatsuba_multiplication
        }
        # Call the selected algorithm
        if algorithm_name in algorithms:
            return algorithms[algorithm_name]()
        else:
            # Raise an error if the algorithm is not found
            raise ValueError(f"Algorithm '{algorithm_name}' not found.")

def benchmark_algorithm(algorithm):
    # Record the start time of the algorithm
    start_time = time.time()
    # Execute the algorithm and store the result
    result = algorithm()
    # Record the end time of the algorithm
    end_time = time.time()
    # Calculate the duration taken by the algorithm
    duration = end_time - start_time
    # Return the result and the duration
    return result, duration

def main():
    # List of test cases with pairs of numbers to be multiplied
    test_cases = [
        (1234, 5678),
        (12345, 67890),
        (123456, 789012),
        (1234567, 8901234)
    ]

    # Iterate through each test case
    for num1, num2 in test_cases:
        # Create an instance of MultiplicationAlgorithms for the current test case
        multiplication_algorithms = MultiplicationAlgorithms(num1, num2)
        # Dictionary of available multiplication algorithms
        algorithms = {
            "Naive Multiplication": multiplication_algorithms.naive_multiplication,
            "Python Multiplication": multiplication_algorithms.python_multiplication,
            "Karatsuba Multiplication": multiplication_algorithms.karatsuba_multiplication
        }

        # Print the representation of the MultiplicationAlgorithms instance
        print(colored(f"\n{repr(multiplication_algorithms)}", 'magenta'))

        # Iterate through each algorithm
        for name, algorithm in algorithms.items():
            # Benchmark the current algorithm
            result, duration = benchmark_algorithm(algorithm)
            # Print the algorithm name
            print(colored(f"{name}:", 'blue'))
            # Print the result of the multiplication
            print(colored(f"Result: {result}", 'green'))
            # Print the time taken by the algorithm
            print(colored(f"Time taken: {duration:.6f} seconds", 'yellow'))
        # Print a separator line
        print(f"{'-' * 100}")

if __name__ == "__main__":
    # Call the main function to execute the test cases
    main()
    """
    This module provides two multiplication algorithms: Naive Multiplication and Karatsuba Multiplication.

    Naive Multiplication:
    ---------------------
    The naive multiplication algorithm performs the standard long multiplication method.
    It iterates through each digit of the first number and multiplies it by each digit of the second number,
    summing the intermediate results to get the final product.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    Karatsuba Multiplication:
    -------------------------
    The Karatsuba multiplication algorithm is a divide-and-conquer algorithm that reduces the multiplication
    of two n-digit numbers to at most three multiplications of n/2-digit numbers. It achieves this by
    recursively breaking down the numbers into smaller parts and combining the results using the formula:

    Let x and y be the two numbers to be multiplied, and let m be the number of digits in the larger number.
    Split x into two parts: x_high and x_low, and y into two parts: y_high and y_low, where each part has m/2 digits.

    The product of x and y can be computed as:
    z0 = x_low * y_low
    z1 = (x_low + x_high) * (y_low + y_high)
    z2 = x_high * y_high

    The final result is given by:
    result = (z2 * 10^(2*m)) + ((z1 - z2 - z0) * 10^m) + z0

    Time Complexity: O(n^log2(3)) ≈ O(n^1.585)
    Space Complexity: O(n)

    Example Usage:
    --------------
    multiplication_algorithms = MultiplicationAlgorithms(123456789, 987654321)
    result_naive = multiplication_algorithms.naive_multiplication()
    result_karatsuba = multiplication_algorithms.karatsuba_multiplication()

    print(f"Naive Multiplication Result: {result_naive}")
    print(f"Karatsuba Multiplication Result: {result_karatsuba}")
    """
