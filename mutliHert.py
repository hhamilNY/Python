# multiple inheritance = inherit from more than one parent class MyClass:
# class MyClass(Parent1, Parent2, Parent3):

# multiple level inheritance  = from one parent which can inherit from another parent
# class Child(Parent):
#     class GrandChild(Child):
#         pass
# Example:   C(B) <- B(A) <- A(Object)

# Benefits: Allows a class to inherit features from multiple classes
#           Promotes code reusability by combining functionalities from different classes   

from typing import Union, Any


line_break: str = "-" * 30


class Animal:

    def __init__(self, name: str) -> None:
        self.name = name
        print(f"Animal initialized: {self.name}")
    
    def eat(self) -> None:
        print(f"{self.name} is eating.")    

    def sleep(self) -> None:
        print(f"{self.name} is sleeping.")

    

class Prey(Animal):

    def flee(self) -> None:
        print(f"{self.name} is fleeing from a predator!")  
        print(line_break)   

class Predator(Animal):

    def hunt(self) -> None:
        print(f"{self.name} is hunting for prey!")  
        print(line_break)   


class Rabbit(Prey):
    def make_sound(self) -> None:
        print(f"{self.name} says: Squeak!")  
        print(line_break)

class Hawk(Predator):
    def make_sound(self) -> None:
        print(f"{self.name} says: Screech!")  
        print(line_break)

class Fox(Predator, Prey):
    def make_sound(self) -> None:
        print(f"{self.name} says: Ring-ding-ding-ding-dingeringeding!")  
        print(line_break)

def main() -> None:
    rabbit = Rabbit("Bunny")
    hawk = Hawk("Mighty Hawk")
    fox = Fox("Foxy")

    rabbit.eat()
    rabbit.sleep()
    rabbit.flee()
    rabbit.make_sound()

    hawk.eat()
    hawk.sleep()
    hawk.hunt()
    hawk.make_sound()

    fox.eat()
    fox.sleep()
    fox.flee()
    fox.hunt()
    fox.make_sound()

if __name__ == "__main__":
    main()  