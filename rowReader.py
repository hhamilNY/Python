import sys
import csv
from typing import Generator


def csv_row_reader(file_path: str) -> Generator[list[str], None, None]:
    with open(file_path, 'r') as csv_file:
        for row in csv.reader(csv_file):
            yield row

def main() -> None:
    reader: Generator[list[str], None, None] = csv_row_reader('data.csv')
    line_break: str = '-' * 20


    while True:
        try:
            for i in range(3):
                print(next(reader))
            input('Coninue retrieving rows?')   


        except StopIteration as e:
            print(f'{line_break}')
            print('No more rows......')
            sys.exit()

if __name__ == '__main__':
    main()
