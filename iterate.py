from itertools import count, cycle, repeat
from typing import Any, Iterator, TypeVar
import timeit

count1: count = count()
count2: count = count(start=5, step=2)
count3: count = count(start=2, step=-1)
count4: count = count(start=0.0, step=0.5)

#T = TypeVar('T')

#def take(n: int, iterable: Iterator[T]) -> list[T]:

for i in range(5):
    print(f'count1: {next(count3)}')

people: list[str] = ['Alice', 'Bob', 'Charlie']
cycled_people: cycle = cycle(people)    

print(f'cycled people: {[next(cycled_people) for _ in range(10)]}') 

repeated: repeat = repeat('Hello', times=5)
print(f'repeated: {[next(repeated) for _ in range(5)]}')  

for i in repeat(None, times=5):
    print(f'Hello {i}')

def while_tree() -> None:
    count: int = 0
    while True:
        count += 1
        if count ==1_000_000:
            break

def itertools_repeat() -> None:
    for _ in repeat(None, times=1_000_000):
        pass

def for_range() -> None:
    for _ in range(1_000_000):
        pass


while_true_time: float = timeit.timeit(while_tree, number=100)
itertools_repeat_time: float = timeit.timeit(itertools_repeat, number=100)  
for_range_time: float = timeit.timeit(for_range, number=100)

print(f'while_true_time: {while_true_time:.3f}s')
print(f'itertools_repeat_time: {itertools_repeat_time:.3f}')
print(f'for_range_time: {for_range_time:.3f}s')  
 

#print(f'while_tree: {timeit.timeit(while_tree, number=100)}')

#print(f'itertools_repeat: {timeit.timeit(itertools_repeat, number=100)}')

#print(f'for_range: {timeit.timeit(for_range, number=100)}')





