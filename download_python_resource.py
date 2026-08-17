import requests
import os
from pathlib import Path
import time

# Create folders
Path("documents/Python").mkdir(parents=True, exist_ok=True)
Path("documents/Python/Beginner").mkdir(exist_ok=True)
Path("documents/Python/Intermediate").mkdir(exist_ok=True)
Path("documents/Python/Advanced").mkdir(exist_ok=True)

PYTHON_RESOURCES = [
    # Beginner Level
    {
        "title": "A Byte of Python - Complete Guide",
        "url": "https://python.swaroopch.com/",
        "level": "Beginner",
        "type": "html",
        "description": "Best for absolute beginners"
    },
    {
        "title": "Python for Everybody - Course Materials",
        "url": "https://www.py4e.com/",
        "level": "Beginner",
        "type": "html",
        "description": "Free course with video + materials"
    },
    {
        "title": "Think Python - Free PDF",
        "url": "https://greenteapress.com/wp/think-python-2/",
        "level": "Beginner",
        "type": "pdf",
        "description": "Great for learning programming concepts"
    },
]

def create_python_cheatsheet():
    """Create a Python crash course cheatsheet with UTF-8 encoding"""
    cheatsheet = """
# PYTHON CRASH COURSE CHEATSHEET

## 1. BASICS
# Variables and Data Types
name = "Python"          # String
age = 30                 # Integer
height = 5.9             # Float
is_fun = True            # Boolean

# Print
print("Hello, Python!")
print(f"Name: {name}, Age: {age}")

## 2. DATA STRUCTURES
# Lists (Ordered, Mutable)
fruits = ["apple", "banana", "orange"]
fruits.append("grape")
print(fruits[0])  # apple

# Tuples (Ordered, Immutable)
colors = ("red", "green", "blue")
print(colors[1])  # green

# Dictionaries (Key-Value pairs)
person = {
    "name": "Alice",
    "age": 25,
    "city": "NYC"
}
print(person["name"])  # Alice

# Sets (Unique values)
numbers = {1, 2, 3, 4, 5}
numbers.add(6)

## 3. STRING OPERATIONS
text = "Hello Python"
print(text.lower())      # hello python
print(text.upper())      # HELLO PYTHON
print(text.split())      # ['Hello', 'Python']
print(text.replace("Python", "World"))

## 4. CONDITIONALS
age = 20

if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Ternary operator
status = "Adult" if age >= 18 else "Minor"

## 5. LOOPS
# For loop
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# For loop with list
for fruit in fruits:
    print(fruit)

# While loop
count = 0
while count < 5:
    print(count)
    count += 1

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

## 6. FUNCTIONS
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

result = greet("Alice")
print(result)  # Hello, Alice!

# Lambda functions
add = lambda x, y: x + y
print(add(3, 5))  # 8

# *args and **kwargs
def print_all(*args, **kwargs):
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_all(1, 2, 3, name="Alice", age=25)

## 7. FILE OPERATIONS
# Read file
with open("file.txt", "r") as f:
    content = f.read()

# Write file
with open("file.txt", "w") as f:
    f.write("Hello, World!")

# Append to file
with open("file.txt", "a") as f:
    f.write("\\nNew line")

## 8. EXCEPTION HANDLING
try:
    num = int("abc")
except ValueError:
    print("Invalid integer")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Execution complete")

## 9. CLASSES & OBJECTS
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def speak(self):
        return f"{self.name} makes a sound"

dog = Animal("Buddy", "Dog")
print(dog.speak())

# Inheritance
class Dog(Animal):
    def speak(self):
        return f"{self.name} barks"

## 10. LIST METHODS
my_list = [1, 2, 3, 4, 5]
my_list.append(6)        # Add element
my_list.extend([7, 8])   # Add multiple
my_list.remove(3)        # Remove element
my_list.pop()            # Remove last element
my_list.sort()           # Sort in place
my_list.reverse()        # Reverse
print(len(my_list))      # Length
print(max(my_list))      # Maximum
print(min(my_list))      # Minimum
print(sum(my_list))      # Sum

## 11. STRING METHODS
text = "  Hello Python  "
print(text.strip())      # Remove whitespace
print(text.replace("Python", "World"))
print(text.find("Python"))  # Find index
print(text.startswith("Hello"))
print(text.endswith("Python"))
print(text.count("l"))   # Count occurrences

## 12. DICTIONARY METHODS
person = {"name": "Alice", "age": 25}
print(person.keys())           # All keys
print(person.values())         # All values
print(person.items())          # Key-value pairs
print(person.get("name"))      # Get with default
person.update({"city": "NYC"}) # Update

## 13. IMPORTS
# Standard library
import math
print(math.sqrt(16))   # 4.0

# Specific functions
from datetime import datetime
now = datetime.now()
print(now)

# Alias
import numpy as np

## 14. USEFUL BUILT-IN FUNCTIONS
# map() - Apply function to all items
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))

# filter() - Filter items
evens = list(filter(lambda x: x % 2 == 0, numbers))

# enumerate() - Get index and value
for i, val in enumerate(numbers):
    print(f"Index {i}: {val}")

# zip() - Combine lists
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
combined = list(zip(list1, list2))

# range() - Create sequence
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)

## 15. COMMON PATTERNS
# Check if value in list
if 5 in numbers:
    print("Found")

# Loop through dictionary
for key, value in person.items():
    print(f"{key}: {value}")

# Create dictionary from lists
keys = ['a', 'b', 'c']
values = [1, 2, 3]
new_dict = dict(zip(keys, values))

# Swap variables
x, y = 10, 20
x, y = y, x  # Now x=20, y=10

# Create list of lists
matrix = [[i+j for j in range(3)] for i in range(3)]

## 16. DEBUGGING TIPS
# Print debugging
print("Variable:", variable)

# Type checking
print(type(variable))

# Help function
help(str.split)

# Assertions
assert age > 0, "Age must be positive"

## 17. COMMON LIBRARIES
# pip install <library>

# Data manipulation
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt

# Web requests
import requests

# JSON handling
import json

# Regular expressions
import re

# Date and time
from datetime import datetime, timedelta

## 18. QUICK EXAMPLES

# Example 1: Calculate factorial
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

# Example 2: Check if prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(17))  # True

# Example 3: Reverse string
text = "Python"
reversed_text = text[::-1]
print(reversed_text)  # nohtyP

# Example 4: Count word frequency
text = "python python java python"
words = text.split()
frequency = {}
for word in words:
    frequency[word] = frequency.get(word, 0) + 1
print(frequency)  # {'python': 3, 'java': 1}

# Example 5: List to dictionary
keys = ['a', 'b', 'c']
values = [1, 2, 3]
result = {k: v for k, v in zip(keys, values)}
print(result)  # {'a': 1, 'b': 2, 'c': 3}

---
Happy Coding!
"""
    
    # FIX: Add encoding="utf-8" parameter
    with open("documents/Python/PYTHON_CHEATSHEET.txt", "w", encoding="utf-8") as f:
        f.write(cheatsheet)
    print("[OK] Created: Python Cheatsheet")

def main():
    print("=" * 70)
    print("Python Learning Resources Downloader")
    print("=" * 70)
    
    # Create cheatsheet
    create_python_cheatsheet()
    
    print("\n[INFO] Creating directory structure...")
    
    print("\n" + "=" * 70)
    print("Web-based Resources (Copy URLs to browser):")
    print("=" * 70)
    print("\n1. A Byte of Python")
    print("   URL: https://python.swaroopch.com/")
    print("   How to save: Ctrl+S in browser or Ctrl+P > Save as PDF")
    
    print("\n2. Python for Everybody")
    print("   URL: https://www.py4e.com/")
    
    print("\n3. Think Python")
    print("   URL: https://greenteapress.com/wp/think-python-2/")
    
    print("\n" + "=" * 70)
    print("GitHub Repositories (Recommended):")
    print("=" * 70)
    print("\nRun these commands in your terminal:\n")
    
    repos = [
        ("30 Days of Python", "https://github.com/Asabeneh/30-Days-Of-Python.git"),
        ("100 Days of Python", "https://github.com/jackfrued/Python-100-Days.git"),
        ("Python Algorithms", "https://github.com/TheAlgorithms/Python.git"),
    ]
    
    for i, (name, url) in enumerate(repos, 1):
        print(f"{i}. {name}")
        print(f"   git clone {url} documents/Python/{name.replace(' ', '-')}")
        print()
    
    print("=" * 70)
    print("[OK] Python Cheatsheet saved to: documents/Python/PYTHON_CHEATSHEET.txt")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
        print("\n[SUCCESS] All done! Now run this command to clone repositories:")
        print("\ngit clone https://github.com/Asabeneh/30-Days-Of-Python.git documents/Python/30-Days\n")
    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("Try closing any file explorer windows and run again.")