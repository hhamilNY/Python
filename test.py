
import numbers

line_break: str = '-' * 25

def gen():
    for n in range(100):
        yield n

def main() -> None:
   
   *x, y = 1, 2 #Unpacking with star operator   
   print(f'{x=}, {y=}')  
   print(line_break) 
   numbers= gen()
   print(next(numbers))
   print(50 in numbers)
   print(next(numbers))
   print(line_break)


if __name__ == "__main__":
    main()
