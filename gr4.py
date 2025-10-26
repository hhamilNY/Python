from itertools import groupby 

from typing import Any, Iterator
from operator import itemgetter

people: list[dict[str,str | int]] = [
    {'name': 'James', 'age':25, 'city': 'New York'},
    {'name': 'Bob', 'age':30, 'city': 'Chicago'},
    {'name': 'Luigi', 'age': 35, 'city': 'New York'},
    {'name': 'David', 'age': 25, 'city': 'Chicago'},
    {'name': 'Sandra', 'age':23, 'city': 'Stockholm'},
    {'name': 'Homer', 'age': 48, 'city': 'Chicago'},

]

get_city: itemgetter = itemgetter('city')
sorted_cities : list[dict[str,str | int]] = sorted(people, key=get_city)
grouped_people: groupby = groupby(sorted_cities, key=get_city)

for city, group in grouped_people:
    print(f'{city}:')
    for person in group:
        print(f'   - {person['name']} (Age {person['age']})')

