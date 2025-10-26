from typing import Union, Any

class Shape:

    def __init__(self, color: str, is_filled: bool) -> None:
        self.color = color
        self.is_filled = is_filled



    def __new__(cls, shape_type: str, *args: Any, **kwargs: Any) -> Union['Circle', 'Square']:
        if shape_type == 'circle':
            return super().__new__(Circle)
        elif shape_type == 'square':
            return super().__new__(Square)
        else:
            raise ValueError(f"Unknown shape type: {shape_type}")


    def area(self) -> float:
        raise NotImplementedError("Subclasses must implement this method")

class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius * self.radius

class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side * self.side

def print_area(shape: Shape) -> None:
    print(f"Area: {shape.area()}")

def main() -> None:
    shapes: list[Shape] = [
    Shape('circle', 5),
    Shape('square', 4)
    ]

    for shape in shapes:
        print_area(shape)

if __name__ == "__main__":
    main()
