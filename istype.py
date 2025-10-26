from typing import TypeIs, TypeGuard, assert_type

def is_str(object) -> TypeGuard[str]:
    return isinstance(object, str)

def check_type(object: object) -> None:
    if is_str(object):
        # here object is of type str
        assert_type(object, str)
        print(f'string of length {len(object)}')
    else:
        # here object is of type object
        assert_type(object, object)
        print('not a string')

class Orange:
    @staticmethod
    def orange() -> None:
        print('***Orange created***')

class Banana:
    @staticmethod
    def banana() -> None:
        print('***Banana created***')

#TypeIS is better than Type Guard because it works with union types and will allow us to get passt the else ststement in check_fruit 

def is_orange(fruit: object) -> TypeIs[Orange]:
    return isinstance(fruit, Orange)

def is_banana(fruit: object) -> TypeIs[Banana]:
    return isinstance(fruit, Banana)

def check_fruit(fruit: Orange | Banana) -> None:
    if is_orange(fruit):
        assert_type(fruit, Orange)
        fruit.orange()
    else:
        assert_type(fruit, Banana)
        fruit.banana()  

check_fruit(Banana())
check_fruit(Orange())
