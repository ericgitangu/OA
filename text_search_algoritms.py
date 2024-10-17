from termcolor import colored
import time

class TextSearchAlgorithms:
    def __init__(self, text, pattern):
        self.text = text
        self.pattern = pattern

    def __repr__(self):
        return f"Text: {self.text}\nPattern: {self.pattern}"

    def naive_search(self):
        """
        Naive search algorithm.
        
        Approach:
        The naive search algorithm checks for the pattern at every position in the text.
        It compares the pattern with the substring of the text starting at each position.
        
        Time Complexity: O(mn)
        Space Complexity: O(1)
        """
        n = len(self.text)
        m = len(self.pattern)
        result = []
        for i in range(n - m + 1):
            j = 0
            while j < m and self.text[i + j] == self.pattern[j]:
                j += 1
            if j == m:
                result.append(i)
        return result

    def rabin_karp_search(self):
        """
        Rabin-Karp search algorithm.
        
        Approach:
        The Rabin-Karp algorithm uses hashing to find any one of a set of pattern strings in a text.
        It compares the hash value of the pattern with the hash value of the current substring of the text.
        
        Time Complexity: O(n) in average, O(mn) at worst
        Space Complexity: O(1)
        """
        n = len(self.text)
        m = len(self.pattern)
        hpattern = hash(self.pattern)
        result = []
        for i in range(n - m + 1):
            htext = hash(self.text[i:i + m])
            if htext == hpattern and self.text[i:i + m] == self.pattern:
                result.append(i)
        return result

    def kmp_search(self):
        """
        Knuth-Morris-Pratt search algorithm.
        
        Approach:
        The KMP algorithm preprocesses the pattern to create an array of longest proper prefix which is also suffix.
        It uses this array to skip characters while matching.
        
        Time Complexity: O(n)
        Space Complexity: O(m)
        """
        n = len(self.text)
        m = len(self.pattern)
        lps = self._compute_lps_array()
        result = []
        i = 0
        j = 0
        while i < n:
            if self.pattern[j] == self.text[i]:
                i += 1
                j += 1
            if j == m:
                result.append(i - j)
                j = lps[j - 1]
            elif i < n and self.pattern[j] != self.text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
        return result

    def _compute_lps_array(self):
        """
        Helper function to compute the longest proper prefix which is also suffix array for KMP algorithm.
        """
        m = len(self.pattern)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if self.pattern[i] == self.pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    def boyer_moore_search(self):
        """
        Boyer-Moore search algorithm.
        
        Approach:
        The Boyer-Moore algorithm preprocesses the pattern to create bad character and good suffix heuristics.
        It uses these heuristics to skip sections of the text, making it efficient for large alphabets.
        
        Time Complexity: O(n) in average, O(mn) at worst
        Space Complexity: O(k)
        """
        n = len(self.text)
        m = len(self.pattern)
        bad_char = self._bad_character_heuristic()
        result = []
        s = 0
        while s <= n - m:
            j = m - 1
            while j >= 0 and self.pattern[j] == self.text[s + j]:
                j -= 1
            if j < 0:
                result.append(s)
                s += (m - bad_char[ord(self.text[s + m])] if s + m < n else 1)
            else:
                s += max(1, j - bad_char[ord(self.text[s + j])])
        return result

    def _bad_character_heuristic(self):
        """
        Helper function to create the bad character heuristic for Boyer-Moore algorithm.
        """
        m = len(self.pattern)
        bad_char = [-1] * 256
        for i in range(m):
            bad_char[ord(self.pattern[i])] = i
        return bad_char

    def two_way_search(self):
        """
        Simple implementation of Two-Way search algorithm.
        This is a placeholder and should be replaced with the actual Two-Way algorithm.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        n = len(self.text)
        m = len(self.pattern)
        result = []
        for i in range(n - m + 1):
            if self.text[i:i+m] == self.pattern:
                result.append(i)
        return result

    def __call__(self, algorithm_name):
        algorithms = {
            "Naive Search": self.naive_search,
            "Rabin-Karp Search": self.rabin_karp_search,
            "KMP Search": self.kmp_search,
            "Boyer-Moore Search": self.boyer_moore_search,
            "Two-Way Search": self.two_way_search
        }
        if algorithm_name in algorithms:
            return algorithms[algorithm_name]()
        else:
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
    # List of texts to search within
    texts = [
        "AABAACAADAABAABA",  # Text 1
        "ABABDABACDABABCABAB",  # Text 2
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",  # Text 3
        "ABABABABABABABABABABABABABABABABABABABABABABABABAB",  # Text 4
        "ABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCDABCD",  # Text 5
        "A" * 1000 + "B" * 1000 + "C" * 1000,  # Text 6
        "A" * 5000 + "B" * 5000 + "C" * 5000,  # Text 7
        "A" * 10000 + "B" * 10000 + "C" * 10000  # Text 8
    ]
    
    # List of patterns to search for
    patterns = [
        "AABA",  # Pattern 1
        "ABABCABAB",  # Pattern 2
        "AAAAAAAAAA",  # Pattern 3
        "ABABABAB",  # Pattern 4
        "ABCDABCD"  # Pattern 5
    ]
    
    # Function to visualize matches in the text
    def visualize_matches(text, pattern, positions):
        """
        Visualizes the matches of the pattern in the text by highlighting the matched positions.
        
        Parameters:
        text (str): The text in which to search for the pattern.
        pattern (str): The pattern to search for.
        positions (List[int]): The starting positions of matches in the text.
        """
        highlighted_text = list(text)
        for pos in positions:
            for i in range(len(pattern)):
                highlighted_text[pos + i] = colored(highlighted_text[pos + i], 'red', attrs=['reverse', 'bold'])
        return ''.join(highlighted_text)

    for text, pattern in zip(texts, patterns):
        # Create an instance of TextSearchAlgorithms for the current text and pattern
        search_algorithms = TextSearchAlgorithms(text, pattern)
        # Dictionary of available search algorithms
        algorithms = {
            "Naive Search": search_algorithms.naive_search,
            "Rabin-Karp Search": search_algorithms.rabin_karp_search,
            "KMP Search": search_algorithms.kmp_search,
            "Boyer-Moore Search": search_algorithms.boyer_moore_search,
            "Two-Way Search": search_algorithms.two_way_search
        }

        # Print the representation of the TextSearchAlgorithms instance
        print(colored(f"\n{repr(search_algorithms)}", 'magenta'))

        for name, algorithm in algorithms.items():
            # Benchmark the current algorithm
            result, duration = benchmark_algorithm(algorithm)
            # Print the algorithm name
            print(colored(f"{name}:", 'blue'))
            # Print the positions of matches found
            if result:
                print(colored(f"Matches found at positions: {result}", 'green'))
            else:
                print(colored("No matches found.", 'red'))
            # Print the time taken by the algorithm
            print(colored(f"Time taken: {duration:.6f} seconds", 'yellow'))
            # Visualize and print the matches in the text
            if result:
                print(colored(f"Visualized Matches:\n{visualize_matches(text, pattern, result)}", 'cyan'))
        print(f"{'-' * 100}")

if __name__ == "__main__":
    main()
