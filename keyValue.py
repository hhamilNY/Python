from ast import arguments


# *args    = allows you to pass multiple non-key arguments
# **kwargs = allows you to pass multiple keyword- arguments
#          * unpacking operator 
#          ** double unpacking operator
#          1. positional 2. default 3. keyword 4. arbitrary
#          *args must appear before **kwargs in function definitions
#          can be used in function calls to unpack lists/tuples and dictionaries


# Example function using *args and **kwargs
#
# def keyValueFunction(*args: int, **kwargs: int) -> None:
#     print("Arguments (args):")
#     for arg in args:
#         print(arg)
    
#     print("Keyword Arguments (kwargs):")
#     for key, value in kwargs.items():
#         print(f"{key}: {value}")



def print_name(*args) -> None:
    print(f'Name: ')
    for name in args:
        print(name, end=' ')
    print()

#rint_name("Dr", "Bob", "Jackson", "III")


def print_address(**kwargs) -> None:
    print("Address:")
    for key, value in kwargs.items():
        print(f"    {key}: {value}")

    print("Values:")

    for value in kwargs.values():
        print(f"    {value}")

    print("Keys:")

    for key in kwargs.keys():
        print(f"    {key}")

#rint_address(street="123 Main St", city="Anytown", state="CA", zip="12345") 


def shipping_label(*args, **kwargs) -> None:
    print("Shipping Label:")
    for name in args:
        print(name, end=" ")
    print()

    if "apt" in kwargs:
        print(f"{kwargs['street']}, Apt {kwargs['apt']}")
    elif "suite" in kwargs:
        print(f"{kwargs['street']}, Suite {kwargs['suite']}")
    elif "pobox" in kwargs:
        print(f"P.O. Box {kwargs['pobox']}")
    elif "floor" in kwargs:
        print(f"{kwargs['street']}, Floor {kwargs['floor']}")
    elif "building" in kwargs:    
        print(f"{kwargs['street']}, Building {kwargs['building']}")
    else:
        print(f"{kwargs['street']}")
        
    print(f"{kwargs['city']}, {kwargs['state']} {kwargs['zip']}")

line_break: str = '-' * 40

def main() -> None:
    print(line_break)
    print_name("Dr", "Bob", "Jackson", "III")
    print(line_break)
    print_address(street="123 Main St", city="Anytown", state="CA", zip="12345")
    print(line_break)

    shipping_label("Dr", "Bob", "Jackson", "III",
                   street="123 Main St", apt="4B", city="Anytown", state="CA", zip="12345")
    print(line_break)
    shipping_label("Ms", "Alice", "Smith",
                   street="456 Oak Ave", suite="12", city="Othertown", state="NY", zip="67890")
    
    print(line_break)
    shipping_label("Mr", "John", "Doe",
                   street="789 Pine Rd", floor="3", city="Sometown", state="TX", zip="54321")
    print(line_break)
    shipping_label("Mrs", "Jane", "Doe",
                   street="321 Maple St", pobox="987", city="Anycity", state="FL", zip="13579")
    print(line_break)
    shipping_label("Dr", "Emily", "Clark",
                   street="654 Cedar Blvd", building="A", city="Newcity", state="WA", zip="24680")
    print(line_break) 
    


if __name__ == "__main__":
    main()
