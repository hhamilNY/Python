from collections import ChainMap
d1: dict[str, int]= {'a': 1, 'b': 2}
d2: dict[str, int]= {'b': 3, 'c': 4}


line_break: str = '-' *30

# changes only occur to the first item in th ChainMap
# the changes will affect the reference to d since it is the first item in the list

cm: ChainMap = ChainMap(d1, d2)

print(f'{cm=}')

cm['a']= -1
cm['z'] = 0

print(f'{cm=}')

cm.pop('b');

print(f'{cm=}')

print(line_break)

d3: dict[str, int]= {'a': 1, 'b': 2}
d4: dict[str, int]= {'b': 3, 'c': 4} 


# all changes will go into the emptyset {} whic is in the first position

cm1: ChainMap[str,int] = ChainMap ({}, d3, d4)
print(f'{cm1=}')

cm1['z']= -1
cm1['y'] = 100
print(f'{cm1=}')

print(line_break)

d5: dict[str, int]= {'a': 1, 'b': 2}
d6: dict[str, int]= {'b': 3, 'c': 4}
cm3: ChainMap = ChainMap(d5, d6)
print(f'{cm3=}')


cm3.maps.append({'g': 7, 'h': 8})
print(f'{cm3=}')

cm3.maps[1].update({'q':20})
print(f'{cm3=}')
print(f'{d5=}')

print(line_break)

e1: dict[str, int]= {'a': 1, 'b': 2}
e2: dict[str, int]= {'b': 3, 'c': 4}
e3: dict[str, int]= {'d': 5, 'e': 6}
e4: dict[str, int]= {'AA': 1, 'BB':2}


cm4: ChainMap[str,int] = ChainMap(e1, e2, e3)
print(f'{cm4=}')
print(f'{cm4.parents=}')

cm4 = cm4.new_child(e4)
print(f'{e4=}')
print(f'{cm4=}')
print(f'{cm4.parents=}')

print(line_break)