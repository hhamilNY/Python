


class Dog:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def get_name(self) -> str:
        return self.name
    
    def get_age(self) -> int:
        return self.age
    

    def bark(self) -> str:
        return "Woof!"
    
    def fetch(self, item: str) -> str:
        return f"Fetched the {item}!"
    
    def sit(self) -> str:
        return "Sitting down."  
    

dog = Dog("Tim", 32)

print(dog.bark())   
print(dog.fetch("ball"))
print(dog.sit())        
print(f'{type(dog)}')
print(f'{isinstance(dog, Dog)}') 
print(isinstance(dog, object))
print(issubclass(Dog, object))
print(issubclass(object, Dog))
print(dir(dog))
print(dir(Dog))
print(dir(object))
print(dir(Dog.bark))
q   = dog.__class__
print(f'{q}')
print(f'{type(q)}')
print(isinstance(q, type))
print(issubclass(q, type))
print(issubclass(type, q))
print(dir(q))
print(dir(type))
print(dir(object))
print(dir(Dog))
print(dir(dog.bark))
# print(dir(Dog.bark.__func__))
# print(dir(Dog.bark.__self__))
# print(dir(Dog.bark.__code__))
# print(dir(Dog.bark.__closure__))
# print(dir(Dog.bark.__annotations__))
# print(dir(Dog.bark.__defaults__))
# print(dir(Dog.bark.__kwdefaults__))
# print(dir(Dog.bark.__module__))
# print(dir(Dog.bark.__name__))
# print(dir(Dog.bark.__qualname__))
# print(dir(Dog.bark.__doc__))
# print(dir(Dog.bark.__dict__))
# print(dir(Dog.bark.__class__))
# print(dir(Dog.bark.__class__.__class__))
# print(dir(Dog.bark.__class__.__class__.__class__))
# print(dir(Dog.bark.__class__.__class__.__class__.__class__))
# print(dir(Dog.bark.__class__.__class__.__class__.__class__.__class__))
# print(dir(Dog.bark.__class__.__class__.__class__.__class__.__class__.__class__))
# print(dir(Dog.bark.__class__.__class__.__class__.__class__.__class__.__class__.__class__))



def main() -> None:
    d= Dog("Buddy", 5)
    print(d.bark()) 
    print(d.fetch("stick"))
    print(d.sit())

if __name__ == "__main__":
    main()  

