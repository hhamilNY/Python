from typing import Self

class ValueError(Exception):
    """Custom exception for invalid input."""
    pass



class Fruit:
    def __init__(self, name: str, grams: float) -> None:
        self.name = name
        self.grams = grams

    def __str__(self) -> str:
        return f'{self.name} has {self.grams}'
    
    def __eq__(self, other: Self) -> bool:
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return f'Fruit(name={self.name!r}, grams={self.grams!r})'    

    def __or__(self, other: Self) -> Self:
        new_name = f'{self.name} & {other.name}'
        return  Fruit(new_name, self.grams + other.grams)   
    
    def __format__(self, format_spec: str):
        match format_spec:
            case 'kg':
                return f'{self.name} weighs {self.grams / 1000:.2f} kg'
            case 'g':
                return f'{self.name} weighs {self.grams:.2f} g'
            case 'lb':
                return f'{self.name} weighs {self.grams / 453.592:.2f} lb'
            case 'f':
                return f'{self.name} weighs {self.grams :.2f} grams (formatted)'  
            case 'desc':
                return f'Fruit: {self.name}, Weight: {self.grams} grams'
            case 'zz':
                return str(self)
            case _:
                raise ValueError(f'Unknown format specifier...')    
    
def main() -> None:
    apple = Fruit('Apple', 150)
    banana = Fruit('Banana', 120)
    orange = Fruit('Orange', 130)
    another_apple = Fruit('Apple', 150)
    
    print(apple)
    print(banana)
    print(apple == banana)  # False
    print(apple == another_apple)  # True

    print(f'{apple:kg}')
    print(format(banana, 'lb')) 
    print(format(apple, 'desc'))
    print(format(banana, 'f'))
   # print(f'{apple:aa}')  # Raises ValueError
   # print(f'{apple:zz}') 
    print(format(banana, 'zz'))     
    print(format(apple, 'zz'))  # Default str representation

    combined_fruit = apple | banana
    print(combined_fruit)  # Fruit with combined name and total grams 

    combined_fruit2 = orange | banana | apple
    print(combined_fruit2)  # Fruit with combined name and total grams

    fruits: list[Fruit] = [Fruit(name='Kiwi', grams=2500),
                            Fruit(name='Plum', grams=1000),
                            Fruit(name='Cherry', grams=250)]      
    for fruit in fruits:
        print(f'Str: {fruit:g}')
        print('Rep: '+repr(fruit))         


if __name__ == '__main__':
    main()  

    