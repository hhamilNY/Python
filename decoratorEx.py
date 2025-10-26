 # Decorators = A function that modifies the behavior of another function
# Used to add functionality to an existing function without modifying its structure

# def my_decorator(func):
#     def wrapper():
#         print("Something is happening before the function is called.")
#         func()
#         print("Something is happening after the function is called.")
#     return wrapper

# @my_decorator
# def say_hello():
#     print("Hello!")


# Benefits: Enhances code readability and organization
#           Promotes code reusability by applying the same decorator to multiple functions  

def add_sprinkles(func):
    def wrapper(*args, **kwargs ):
        print("Adding sprinkles!")
        func(*args, **kwargs )
    return wrapper

def add_fudge(func):
    def wrapper(*args, **kwargs):
        print("Adding fudge!")
        func(*args, **kwargs)
    return wrapper
 

@add_sprinkles
@add_fudge 
def make_ice_cream(flavor: str = "vanilla") -> None:
    print(f"Here's your {flavor} ice cream.")

def main() -> None:     
    make_ice_cream()
    print()
    print()
    make_ice_cream("chocolate")



if __name__ == "__main__":
    main()  
