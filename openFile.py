from typing import Any, TextIO 


# The file might not close if there is a exception during the reading of the file

file: TextIO = open("notes.txt", "r")
content: str = file.read()
print(content)
file.close() 

# best to use a try/finally block to ensure the file is closed
file2: TextIO = open("notes.txt", "r")
try:
    content2: str = file2.read()
    print(content2)
finally:
    file2.close()   

# best to use a with statement to ensure the file is closed
# the file is automatically closed when the with block is exited 
with open("notes.txt", "r") as file2:
    content3: str = file2.read()


    print(content3)  


name: str = 'Bob'
number: int = 10
maybe: str = 'x' 

print(isinstance(name, (str, int)))
print(isinstance(number, (str, int)))
print(isinstance(maybe, (str, int)))  

class Animal:
    ... 

class Dog(Animal):
    ...

# Testing the relationships is best to use isinstance instead of Type, when checking for inheritance (subclasses)
print(isinstance(Dog(), Animal ))
print(isinstance(Animal(), Dog ))  # animal is not a dog
print(issubclass(Dog, Animal))
print(issubclass(Animal, Dog))
print(issubclass(Dog, object))
print(issubclass(object, Dog))
print(dir(Dog))
print(dir(Animal))
print(dir(object))
