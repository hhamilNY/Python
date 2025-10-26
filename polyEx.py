from typing import Any
from abc import ABC, abstractmethod
import shape
line_break: str = "-" * 30




# Polymorphism = the ability to take many forms
# in programming, polymorphism refers to the way in which different object types can be accessed through the same interface
# each type can provide its own, independent implementation of this interface
# Greek word that means to "have many forms or faces"
# Poly = many
# Morph = forms 



class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass  

    @abstractmethod
    def describe(self) -> None:
        pass

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius * self.radius

    def describe(self) -> None:
        print(f'It is a circle with with an area of {self.area()}cm*2')

class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side

    def describe(self) -> None:
        print(f'It is a square with an area of {self.area()}cm*2')

    def print_shape_info(shape: Shape) -> None:
        shape.describe() 

class Triangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width 
        self.height = height

    def area(self) -> float:
        return 0.5 * self.width * self.height

    def describe(self) -> None:
        print(f'It is a triangle with an area of {self.area()}cm*2')   

def main() -> None:
    circle = Circle(radius=5)
    square = Square(side=4)
    triangle = Triangle(width=3, height=6)

    shapes: list[Shape] = [circle, square, triangle]

    for shape in shapes:
        shape.describe()    
        print()


if __name__ == "__main__":
    main()