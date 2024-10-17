from termcolor import colored


class LongestPalindromicSubstring:
    def __init__(self, s: str):
        self.s = s
        self.longest_palindrome = self._find_longest_palindromic_substring()

    def _find_longest_palindromic_substring(self) -> str:
        """
        Finds the longest palindromic substring in the given string.

        Returns:
        str: The longest palindromic substring.
        """
        n = len(self.s)
        if n == 0:
            return ""

        # Table to store the palindrome status
        dp = [[False] * n for _ in range(n)]
        start = 0
        max_length = 1

        # All substrings of length 1 are palindromes
        for i in range(n):
            dp[i][i] = True

        # Check for substrings of length 2
        for i in range(n - 1):
            if self.s[i] == self.s[i + 1]:
                dp[i][i + 1] = True
                start = i
                max_length = 2

        # Check for substrings of length greater than 2
        for length in range(3, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if self.s[i] == self.s[j] and dp[i + 1][j - 1]:
                    dp[i][j] = True
                    start = i
                    max_length = length

        return self.s[start:start + max_length]

    def __repr__(self):
        return f"LongestPalindromicSubstring(s='{self.s}', longest_palindrome='{self.longest_palindrome}')"

    def __contains__(self, item):
        return item in self.longest_palindrome

    def __len__(self):
        return len(self.longest_palindrome)

# Example usage:
if __name__ == "__main__":
    test_strings = [
        "babad", "cbbd", "a", "ac", "racecar", "noon", "level", "deified", "civic", "radar",
        "abba", "madam", "refer", "rotor", "wow", "mom", "dad", "pop", "gig", "non",
        "babad", "cbbd", "a", "ac", "racecar", "noon", "level", "deified", "civic", "radar",
        "abba", "madam", "refer", "rotor", "wow", "mom", "dad", "pop", "gig", "non",
        "babadbabad", "cbbdcbbd", "aa", "aca", "racecarracecar", "noonnoon", "levellevel", "deifieddeified", "civiccivic", "radarradar",
        "abbaabba", "madammadam", "referrefer", "rotorrotor", "wowwow", "mommom", "daddad", "popop", "gigig", "nonon",
        "babadxyzbabad", "cbbdxyzcbbd", "axyza", "acxyzac", "racecarxyzracecar", "noonxyznoon", "levelxyzlevel", "deifiedxyzdeified", "civicxyzcivic", "radarxyzradar",
        "abbaxyzabba", "madamxyzmadam", "referxyzrefer", "rotorxyzrotor", "wowxyzwow", "momxyzmom", "dadxyzdad", "popxyzpop", "gigxyzgig", "nonxyznon",
        "a" * 100, "ab" * 50, "abc" * 33 + "a", "abcd" * 25, "abcde" * 20,
        "abcdefghij" * 10, "abcdefghijk" * 9 + "a", "abcdefghijklm" * 7 + "a",
        "abcdefghijklmno" * 6 + "a", "abcdefghijklmnop" * 5 + "a",
        "abcdefghijklmnopqrst" * 4 + "a", "abcdefghijklmnopqrstuv" * 3 + "a",
        "abcdefghijklmnopqrstuvwx" * 2 + "a", "abcdefghijklmnopqrstuvwxyz" * 2,
        "a" + "b" * 98 + "a", "a" + "b" * 49 + "a" + "b" * 49 + "a",
        "a" + "b" * 24 + "a" + "b" * 24 + "a" + "b" * 24 + "a" + "b" * 24 + "a",
        "a" + "b" * 12 + "a" + "b" * 12 + "a" + "b" * 12 + "a" + "b" * 12 + "a" + "b" * 12 + "a" + "b" * 12 + "a" + "b" * 12 + "a",
        "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a" + "b" * 6 + "a", 
        "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a" + "b" * 3 + "a",
        "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a" + "b" * 2 + "a",
    ]

    for test_string in test_strings:
        lps = LongestPalindromicSubstring(test_string)
        print(colored(f"The longest palindromic substring of '{test_string}' is '{lps.longest_palindrome}'", 'green'))
        substrings_to_check = ["bab", "aba", "racecar", "noon", "level"]
        for substring in substrings_to_check:
            print(colored(f"Is '{substring}' in the longest palindromic substring? {substring in lps}", 'yellow'))
        print(colored(f"Length of the longest palindromic substring: {len(lps)}", 'blue'))
        print()


