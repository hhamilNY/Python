class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def __repr__(self):
        return f"Car(make='{self.make}', model='{self.model}', year={self.year})"
    
    def __eq__(self, other):
        if isinstance(other, Car):
            return (self.make == other.make and
                    self.model == other.model and
                    self.year == other.year)
        return False    
    
def main(): 
    car1 = Car("Toyota", "Corolla", 2020)
    car2 = Car("Toyota", "Corolla", 2020)
    car3 = Car("Honda", "Civic", 2019)

    print(car1)  # Uses __str__
    print(repr(car1))  # Uses __repr__

    print(car1 == car2)  # True
    print(car1 == car3)  # False      

if __name__ == "__main__":
    main()  