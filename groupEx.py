from itertools import groupby 
from typing import Any, Iterator


numbers: list[list[int]] = [[1,2], [3,4,5], [6], [7,8,9]]
sorted_numbers: list[list[int]] = sorted(numbers, key=len)
grouped_numbers: groupby = groupby(sorted_numbers, key=len)

print(f'{numbers=}')
print(f'{sorted_numbers=}')
#print(next(grouped_numbers))
print(f'{next(grouped_numbers)=}')

grouped2_numbers: groupby = groupby(sorted_numbers, key=len)
a,b = next(grouped2_numbers)
print (a, list(b))

grouped3_numbers: groupby = groupby(sorted_numbers, key=len)
#a,b = next(grouped2_numbers)

for length, group in grouped3_numbers:
    print (f' {length=}, {list(group)=}')





