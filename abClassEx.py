from abc import ABC, abstractmethod

line_break: str = "-" * 30

class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass
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


class Vehcile(ABC):
    @abstractmethod
    def drive(self):
        pass    
    @abstractmethod
    def stop(self):
        pass

class Car(Vehcile):
    def drive(self):
        print("Car is driving.")
    def stop(self):
        print("Car has stopped.")

        
class Bike(Vehcile):
    def drive(self):
        print("Bike is driving.")
    def stop(self):
        print("Bike has stopped.")

class Boat(Vehcile):
    def drive(self):
        print("Boat is sailing.")
    def stop(self):
        print("Boat has anchored.")

class Motorcycle(Vehcile):
    def drive(self):
        print("Motorcycle is driving.")
    def stop(self):
        print("Motorcycle has stopped.")

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

    print()
    print(line_break)   
    car = Car()
    bike = Bike()
    boat = Boat()
    car.drive()
    car.stop()   
    bike.drive()
    bike.stop()
    boat.drive()
    boat.stop()
    motorcycle = Motorcycle()
    motorcycle.drive()
    motorcycle.stop()
    

if __name__ == "__main__":
    main()

