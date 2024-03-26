import math

class Calculator:
    @staticmethod
    def floor(x: float) -> int:
        return math.floor(x)
    
    @staticmethod
    def nroot(n: int, x: int) -> float:
        return math.pow(x, 1/n)
    
    @staticmethod
    def reverse(s: str) -> str:
        return s[::-1]
    
    @staticmethod
    def valid_anagram(s1: str, s2: str) -> bool:
        s1 = ''.join(filter(str.isalpha, s1.lower()))
        s2 = ''.join(filter(str.isalpha, s2.lower()))

        count_s1 = {}
        count_s2 = {}

        for char in s1:
            count_s1[char] = count_s1.get(char, 0) + 1
        for char in s2:
            count_s2[char] = count_s2.get(char, 0) + 1

        return count_s1 == count_s2
    
    @staticmethod
    def sort(str_arr: list) -> list:
        return str_arr.sort()