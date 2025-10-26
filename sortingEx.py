# Sorting in python , sort or sorted() functions
# sort() method sorts the list in place and returns None
# sorted() function returns a new sorted list from the elements of any iterable
# Lists[]. Tuples(), Dictionarieds{}, Sets{}, Objects

from re import A
from typing import Any, Union


line_break: str = "-" * 30

# # A function that returns the length of the value:
def myFunc(e):
  return len(e)
print()
print('Lists sorting example:')

cars = ['Ford', 'Mitsubishi', 'BMW', 'VW']
print('Original cars list:')
print(cars)
print()
cars.sort(reverse=True, key=myFunc)
print(cars)

print()
print(line_break)

Afruits = ['banana', 'apple', 'cherry', 'date', 'fig', 'grape']
print('Original fruits list:')
print(Afruits)
print()
Afruits.sort(reverse=True, key=myFunc)
print(Afruits)

Afruits.sort(reverse=False, key=myFunc)
print(Afruits)


print()
print(line_break)


# tuple2 (sequence)
print()
print('Tuples sorting example:')

tuple2 = ('banana', 'apple', 'cherry', 'date', 'fig', 'grape')
print('Original fruits Tuple:')
print(tuple2)
print()
sorted_tuple = tuple(sorted(tuple2, reverse=True, key=myFunc))
print(sorted_tuple)
sorted_tuple = tuple(sorted(tuple2, reverse=False, key=myFunc))
print(sorted_tuple)
print()
print(line_break)

# Dictionary {}
dict1 = {'banana': 3, 
         'apple': 4, 
         'cherry': 2, 
         'date': 5, 
         'fig': 1, 
         'grape': 2}
print()
print('Dictionary sorting example:')
print('Original fruits Dictionary:')
print(dict1)
print()
# Sort by key
sorted_dict_by_key = dict(sorted(dict1.items(), reverse=True, key=myFunc))

print('sorted_dict_by_key')
print(sorted_dict_by_key)
# Sort by value
sorted_dict_by_value = dict(sorted(dict1.items(), key=lambda item: item[1], reverse=True))

print('sorted_dict_by_value')
print(sorted_dict_by_value)


# Sort by key
# key=lambda item: item[0] to select the item from dictionary
sorted2_dict_by_key = dict(sorted(dict1.items(), reverse=True, key=lambda item: item[0]))

print('sorted2_dict_by_key')
print(sorted2_dict_by_key)
# Sort by value
# key=lambda item: item[1] to select the item from dictionary

sorted2_dict_by_value = dict(sorted(dict1.items(), key=lambda item: item[1], reverse=False))

print('sorted2_dict_by_value')
print(sorted2_dict_by_value)
print()
print(line_break)

# Objects:

class AFruit:
    def __init__(self, name: str, calories: int) -> None:
        self.name = name
        self.calories = calories

    def __repr__(self) -> str:
        return f"{self.name}: {self.calories} cal"
print()    
print('Object sorting example:')
fruits: list[AFruit] = [AFruit("banana", 105),
              AFruit("apple", 95),
              AFruit("cherry", 50),
              AFruit("date", 20),
              AFruit("fig", 37),
              AFruit("grape", 62)]
    

# Sort by calories
# key=lambda fruit: fruit.calories to select the item from dictionary
print()
print('Original fruits list:')
print(fruits)
print()
sorted_fruits_by_calories = sorted(fruits, key=lambda fruit: fruit.calories)
print('sorted_fruits_by_calories')
print(sorted_fruits_by_calories)    

# Sort by name
# key=lambda fruit: fruit.name to select the item from dictionary
sorted_fruits_by_name = sorted(fruits, key=lambda fruit: fruit.name)
print('sorted_fruits_by_name')  
print(sorted_fruits_by_name)    
