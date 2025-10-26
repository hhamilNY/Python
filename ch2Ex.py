from collections import ChainMap

#from dog import Dog


d1: dict[str, int]= {'a': 1, 'b': 2}
d2: dict[str, int]= {'b': 3, 'c': 4}

names: list[str] = ['Bob', 'Sally']
cm: ChainMap[str, None] = ChainMap.fromkeys(names, None)
print(f'{cm=}')

cm.update({'Luigi': None})

print(f'{cm=}')
#dog = Dog()
