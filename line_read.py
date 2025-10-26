import sys
from typing import Generator

def read(path:str) -> Generator[str, None, str]:
    with open(path, 'r') as file:
        for line in file:
            yield line.strip()
    
    return 'This is the end!'

def main() -> None:
    reader: Generator[str, None, str] = read('note.txt')
    input(f'Tap "enter" for next ')

    while True:
        try:
            print(next(reader))
        except StopIteration as e:
            print('StopIteration:', e.value)
            sys.exit()

        input()

if __name__ == '__main__':
    main()
