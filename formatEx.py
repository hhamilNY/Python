from typing import Any
import sys

class Book:
    def __init__(self, title: str, pages: int) -> None:
        self.title = title
        self.pages = pages

    def __str__(self):
        return f"Title: {self.title } Pages: {self.pages } "
    
    def __format__(self, format_spec: Any) -> str:
        match format_spec:
            case 'time':
                return f'{self.pages /6:.2f}h'
            case 'caps':
                return self.title.upper()
            
            case _:
                raise ValueError(f'Unknnown specifer {format_spec=} for Book() ')
                sys.exit()


def main() -> None:

    HP: Book = Book('Harry Potter and the Philosopher Stone', 300)
    MP: Book = Book('Mpnty Python and te Holy Grail', 20)

    print(HP)
    print(f'{HP.title =}')
    print(f'{HP.title.upper() =}')
    print(f'{HP:caps}')  #correct usage
    print(f'Read time: {HP:time}')

    print(MP)
    print(f'Read time: {MP:time}')

    print(f'{HP:capG}')  # test exception example
  




if __name__ =='__main__':
    main()
            