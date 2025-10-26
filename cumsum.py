import sys
from typing import Generator

def cumiulative_sum() -> Generator[float, float, None]:
    total: float = 0
    while True:
    #   new_value: float = yield total
    #   total += new_value
        total += yield total

def main() -> None:
    cumulative_generator: Generator[float, float, None] = cumiulative_sum()
    next(cumulative_generator)

    while True:
       
       try:
         value: float = float(input('Enter a value: '))
         current_sum: float = cumulative_generator.send(value)
         print(f' Cumulative Sum: {current_sum}')

       except (ValueError, KeyboardInterrupt) as e:
        print('Error: ', e)
        sys.exit()
          


if __name__ == '__main__':
    main()

