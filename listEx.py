# List comprehension = A concise way to create lists in python
# Compact and easier to read than traditional loops
# [expression for value in iterable if condition]
# More efficient than using loops to create lists
# It provides a shorter syntax when you want to create a new list based on the values of an existing list.
# It consists of brackets containing an expression followed by a for clause,
# then zero or more for or if clauses.
# The expressions can be anything, meaning you can put in all kinds of objects in lists.

line_break: str = "-" * 30

# Example 1: Create a list of squares of numbers from 0 to 9
squares = [x**2 for x in range(10)]
print(f'Squares: {squares}')
print()
print(line_break)

# Example 2: Create a list of even numbers from 0 to 19
evens = [x for x in range(20) if x % 2 == 0]
print(f'Even numbers: {evens}')
print()
print(line_break)
# Example 3: Create a list of uppercase strings from a list of strings
fruits = ["apple", "banana", "cherry", "date"]
upper_fruits = [fruit.upper() for fruit in fruits]
print(f'Uppercase fruits: {upper_fruits}')
print()
print(line_break)
# Example 4: Create a list of tuples (number, square) for numbers from
# 0 to 9
num_square_tuples = [(x, x**2) for x in range(10)]
print(f'Number-Square tuples: {num_square_tuples}')
print()
print(line_break)
# Example 5: Create a list of characters from a string
string = "hello"
chars = [char for char in string]
print(f'Characters in string: {chars}')
print()
print(line_break)
# Example 6: Create a list of lengths of each word in a list
words = ["hello", "world", "python", "is", "awesome"]
word_lengths = [len(word) for word in words]
print(f'Word lengths: {word_lengths}')
print()
print(line_break)
# Example 7: Create a list of numbers divisible by 3 from 0 to 29
div_by_3 = [x for x in range(30) if x % 3 == 0]
print(f'Numbers divisible by 3: {div_by_3}')
print()
print(line_break)
# Example 8: Create a list of first letters of each word in a list
first_letters = [word[0] for word in words]
print(f'First letters: {first_letters}')
print()
print(line_break)
# Example 9: Create a list of tuples (word, length) for each word in a list
word_length_tuples = [(word, len(word)) for word in words]
print(f'Word-Length tuples: {word_length_tuples}')
print()
print(line_break)
# Example 10: Create a list of numbers from 0 to 19, replacing
# multiples of 3 with "Fizz" and multiples of 5 with "Buzz"

fizz_buzz = [
    "Fizz" if x % 3 == 0 else "Buzz" if x % 5 == 0 else x for x in range(20)
]       
print(f'FizzBuzz list: {fizz_buzz}')
print()
print(line_break)
# Example 11: Flatten a 2D list (matrix) into a 1D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  

flattened = [num for row in matrix for num in row]
print(f'Flattened matrix: {flattened}')
print()
print(line_break)
# Example 12: Create a list of tuples (i, j) for a 3x3 grid
grid_tuples = [(i, j) for i in range(3) for j in range(3)]
print(f'Grid tuples: {grid_tuples}')
print()
print(line_break)
# Example 13: Create a list of words that start with the letter 'a'
words_starting_with_a = [word for word in words if word.startswith('a')]
print(f'Words starting with "a": {words_starting_with_a}')
print()
print(line_break)
# Example 14: Create a list of unique characters from a string
unique_chars = list({char for char in string})
print(f'Unique characters: {unique_chars}')
print()
print(line_break)
# Example 15: Create a list of numbers from 0 to 19, replacing
# multiples of 3 with "Fizz", multiples of 5 with "Buzz",
# and multiples of both 3 and 5 with "FizzBuzz"
fizz_buzz_advanced = [
    "FizzBuzz" if x % 3 == 0 and x % 5 == 0 else
    "Fizz" if x % 3 == 0 else
    "Buzz" if x % 5 == 0 else
    x for x in range(20)
]
print(f'Advanced FizzBuzz list: {fizz_buzz_advanced}')
print()
print(line_break)
import pandas as pd
import numpy as np
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [28, 34, 29, 42],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
}
df = pd.DataFrame(data)
print(f'{df.to_string() }')
print()
print(line_break)
# Example 16: Create a new column 'Age_Group' based on age
df['Age_Group'] = ['Young' if age < 30 else 'Old' for age in df['Age']]
print("After adding 'Age_Group' column:")
print(f'{df.to_string() }')
print()
print(line_break)
# Example 17: Create a list of tuples (Name, City) from the DataFrame
name_city_tuples = [(row['Name'], row['City']) for index, row in df.iterrows()]

print(f'Name-City tuples: {name_city_tuples}')
print()
print(line_break)
# Example 18: Create a list of names in uppercase from the DataFrame
upper_names = [name.upper() for name in df['Name']]

print(f'Uppercase names: {upper_names}')
print()
print(line_break)
# Example 19: Create a list of ages greater than 30
ages_above_30 = [age for age in df['Age'] if age > 30]
print(f'Ages above 30: {ages_above_30}')
print()
print(line_break)
# Example 20: Create a list of dictionaries for each row in the DataFrame
row_dicts = [row.to_dict() for index, row in df.iterrows()]
print(f'Row dictionaries: {row_dicts}')
print()
print(line_break)
# Example 21: Create a list of indices for rows where Age is less than 30
indices_below_30 = [index for index, row in df.iterrows() if row['Age'] < 30]
print(f'Indices with Age below 30: {indices_below_30}')
print()
print(line_break)
# Example 22: Create a list of cities in lowercase from the DataFrame
lower_cities = [city.lower() for city in df['City']]
print(f'Lowercase cities: {lower_cities}')
print()
print(line_break)
# Example 23: Create a list of names with their lengths
name_length_tuples = [(name, len(name)) for name in df['Name']]
print(f'Name-Length tuples: {name_length_tuples}')
print()
print(line_break)
# Example 24: Create a list of ages incremented by 5
incremented_ages = [age + 5 for age in df['Age']]
print(f'Incremented ages: {incremented_ages}')
print()
print(line_break)
# Example 25: Create a list of boolean values indicating if Age is even
is_age_even = [age % 2 == 0 for age in df['Age']]
print(f'Is Age Even: {is_age_even}')
print()
print(line_break)
# Example 26: Create a list of formatted strings for each person

formatted_strings = [f"{row['Name']} is {row['Age']} years old and lives in {row['City']}" for index, row in df.iterrows()]
print(f'Formatted strings: {formatted_strings}')
print()
print(line_break)
# Example 27: Create a list of ages squared
ages_squared = [age**2 for age in df['Age']]
print(f'Ages squared: {ages_squared}')
print()
print(line_break)
# Example 28: Create a list of names that contain the letter 'a'
names_with_a = [name for name in df['Name'] if 'a' in name.lower()]
print(f'Names containing "a": {names_with_a}')
print()
print(line_break)
# Example 29: Create a list of cities with more than 6 characters
cities_longer_than_6 = [city for city in df['City'] if len(city) > 6]
print(f'Cities longer than 6 characters: {cities_longer_than_6}')
print()
print(line_break)
# Example 30: Create a list of tuples (Name, Age_Group) from the DataFrame
name_agegroup_tuples = [(row['Name'], row['Age_Group']) for index, row in df.iterrows()]
print(f'Name-Age_Group tuples: {name_agegroup_tuples}')
print()
print(line_break)
# End of examples

# The above examples demonstrate various ways to use list comprehensions
# to create and manipulate lists in Python, including integration with pandas DataFrames.   +