class ValueError(Exception):
    """Custom exception for invalid input."""
    pass

def do_math() -> None:
    print('Please enter a number for "a" and "b ".')
    try:
        a: float = float(input('a: '))
        b: float = float(input('b: '))
        print(f'The Sum of {a} + {b} is {a+ b}')
    except (ValueError, TypeError):
        print('Please add only numbers')
        do_math()

def main():
    do_math()

if __name__ == '__main__':
    main()
    

