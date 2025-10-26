
# super() = Function used in a child class to call a method from its parent class (superclass) 
# Allows you to extend the functionlity of the inherited methods
#from turtle import shape
#from typing import turtle  
from typing import Union, Any


class Shape:
    def __init__(self, color: str, is_filled: bool) -> None:
        self.color = color
        self.is_filled = is_filled

    def describe(self) -> None:
        print(f"It is  color {self.color}, and {'filled' if self.is_filled else 'not filled'}.")

class Circle(Shape):
    def __init__(self, radius: float, color: str, is_filled: bool) -> None:
        super().__init__(color, is_filled)
        self.radius = radius

    def describe(self) -> None:
        print(f'It is a circle with with an area of {3.14 * self.radius * self.radius}cm*2')
        super().describe()


class Square(Shape):
    def __init__(self, side: float, color: str, is_filled: bool) -> None:
        super().__init__(color, is_filled)
        self.side = side

    def area(self) -> float:
        return self.side * self.side
    

    
    # def print_shape_info(shape: Shape) -> None:
    #    hape.describe()
    #     if isinstance(shape, Circle):   
    #         print(f"It is a circle with radius {shape.radius}.")
    #     elif isinstance(shape, Square): 
    #         print(f"It is a square with side {shape.side}.")
    #     elif isinstance(shape, Triangle):
    #         print(f"It is a triangle with width {shape.width} and height {shape.height}.")
    #     print()

class Triangle(Shape):
    def __init__(self, width: float, height: float, color: str, is_filled: bool) -> None:
        super().__init__(color, is_filled) # Shape is the superclass
        self.width = width 
        self.height = height

  


   
def main() -> None:
    circle = Circle(radius=5, color="red", is_filled=True)
    square = Square(side=4, color="blue", is_filled=False)
    triangle = Triangle(width=3, height=4, color="green", is_filled=True)

    print(f'{Circle =  }') 
    circle.describe()
    print
    square.describe()
    print(f'(square.area()= {square.area()}')
    triangle.describe()

    # shapes: list[Shape] = [
    #     Circle(radius=5, color="red", is_filled=True),
    #     Square(width=4, color="blue", is_filled=False),
    #     Triangle(width=3, height=4, color="green", is_filled=True)
    # ]
   
    # for shape in shapes:
    #     print_shape_info(shape)

if __name__ == "__main__":
    main()
