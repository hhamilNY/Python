from typing import Callable, Any
import time

def time_function(func: Callable[[int],int], n: int) -> None:
    
    start_time: float = time.perf_counter()
    result: int = func(n)
    end_time: float = time.perf_counter()
    elapsed_time: float = end_time - start_time
    print(f'{func.__name__}({n}) = {result}')
    print(f'Time taken: {elapsed_time:.6f} seconds') 
    
def fibonacci_recursive(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
    
print(fibonacci_recursive(10))
time_function(func=fibonacci_recursive, n=10)
print(fibonacci_recursive(20))
time_function(func=fibonacci_recursive, n=20)
print(fibonacci_recursive(30))
time_function(func=fibonacci_recursive, n=30)
print(fibonacci_recursive(35))
time_function(func=fibonacci_recursive, n=35)


def fibonacci_iterative(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fibonacci_iterative(10))
time_function(func=fibonacci_iterative, n=10)
print(fibonacci_iterative(20))
time_function(func=fibonacci_iterative, n=20)
print(fibonacci_iterative(30))
time_function(func=fibonacci_iterative, n=30)
print(fibonacci_iterative(35))
time_function(func=fibonacci_iterative, n=35)

time_function(func=fibonacci_iterative, n=50)

time_function(func=fibonacci_recursive, n=50)

#time_function(func=fibonacci_iterative, n=100)  

    
