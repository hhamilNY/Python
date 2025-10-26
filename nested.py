# Nested class = A class defined within another class
# class OuterClass:
#     class NestedClass:
#         def __init__(self):
#             self.value = 42

#     def create_nested_instance(self):
#         return self.NestedClass()

# Benefits: Allows you to logically group classes that are closely related
#           Encapsulates private details that aren't relevant outside 
#           of the outer class
#           Keeps the namespace clean: reduces the possibility of 
#           naming conflicts
# Improves code organization and readability

from typing import Any

line_break: str = "-" * 30

class Company:
    class Employee:
        def __init__(self, name: str, position: str) -> None:
            self.name = name
            self.position = position

        def get_info(self) -> str:
            return f"{self.name} works as a {self.position}"

    def __init__(self, company_name: str) -> None:
        self.company_name: str = company_name
        self.employees: list[Company.Employee] = []

    def add_employee(self, name: str, position: str) -> None:
        new_employee = self.Employee(name, position)
        self.employees.append(new_employee)

    def list_employees(self) -> None:
        print(f'Employees at {self.company_name}:')
        for emp in self.employees:
            print(emp.get_info())   
        

def main() -> None:
    my_company: Company  = Company("Krusty Krab")
    my_company.add_employee("Alice", "Developer")
    my_company.add_employee("Bob", "Designer")
   

    other_Company: Company = Company("Tech Solutions")
    other_Company.add_employee("Charlie", "Manager")
    other_Company.add_employee("Diana", "Analyst")
    print()
    print(line_break)
    print(f'{my_company.company_name = }')
    my_company.list_employees()

    print()
    print(line_break)

    print(f'{other_Company.company_name = }')
    other_Company.list_employees() 

    print()
    print(line_break) 

    
if __name__ == "__main__":
    main()
# Output:
# Alice works as a Developer
# Bob works as a Designer       
