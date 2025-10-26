from typing import Generator

def fibonacci_generstor() -> Generator[int, None, None]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, (a + b) 
        

def main() -> None:
    fib_gen: Generator[int, None, None] = fibonacci_generstor()
    n: int = 10
    line_break: str = '-' * 20

    while True:  
        input(f'Tap "enter for next {n} numbers of fibonacci')
        print(line_break)
        for i in range(n):
            print(f'{next(fib_gen)}')

        print(line_break)


if __name__ == '__main__':
    main()