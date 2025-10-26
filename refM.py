from typing import Any
from copy import deepcopy


#reference mistake

a: list[int] = [10, 20, 30, 40, 50]
b: list[int] = a 

print(f'{id(a)=}')
print(f'{id(b)=}')  

a.append(1111)
b.append(2222)


print(f'{a=}')
print(f'{b=}')


# best to use deepcopy to create a true copy of the list
# very expensive operation for large lists
c: list[int] = [10, 20, 30, 40, 50]
d: list[int] = deepcopy(c)

print(f'{id(c)=}')
print(f'{id(d)=}')

print(f'{c=}')
print(f'{d=}')