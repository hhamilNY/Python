from typing import NamedTuple
from dataclasses import dataclass
from copy import replace, copy, deepcopy


# replace is a shallow copy of an object with some attributes replaced with new values
# you can only use replace with dataclass and NamedTuple
# you can use copy to make a shallow copy of any object
# you would need to use deepcopy from copy module to # # make a deep copy of an object to cget a list object/ # reference object to be copied as well





@dataclass(frozen=True)
class Item:
    name: str
    cost: float

cup: Item = Item('Cup', 10.0)
golden_cup: Item = copy(cup)
replace_cup: Item = replace(cup, name='New Golden Cup', cost=100.0)

print(f'cup: {id(cup) = }')
print (cup)
print(f'golden_cup: {id(golden_cup) = }')
print(golden_cup) 
print(f'replace_cup: {id(replace_cup) = }')
print(replace_cup)

class Point(NamedTuple):
    x: int
    y: int


# point1 is immutable and can never change the values
point1: Point = Point(10, 20)
point2: Point = point1._replace(x=100)  
