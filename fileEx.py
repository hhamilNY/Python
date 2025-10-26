# Python writing files ( .txt or .csv etc) examples
# https://realpython.com/python-file-handling/      

import json 

line_break: str = "*" * 20

# Example 1: Writing to a text file
with open("example.txt", "w") as file:
    file.write("Hello, World!")
print("Finished writing to example.txt")
print(line_break)

# Example 2: Reading from a text file
with open("example.txt", "r") as file:
    content = file.read()
print(f"Content of example.txt: {content}")
print(line_break)

# Example 3: Writing JSON data to a file
data = {"name": "Alice", 
        "age": 30,
        "city": "New York"}

with open("data.json", "w") as json_file:
    json.dump(data, json_file)
print("Finished writing to data.json")
print(line_break)

# Example 4: Reading JSON data from a file
with open("data.json", "r") as json_file:
    loaded_data = json.load(json_file)
print(f"Content of data.json: {loaded_data}")
print(line_break)

