from dataclasses import dataclass, KW_ONLY 

@dataclass
class EmergencyContact ():
    name: str
    relation: str
    phone: str

@dataclass
class Contacts():
    emergency_contact: EmergencyContact

@dataclass
class Address():
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    
@dataclass
class Person():
    name: str
    age: int
    email: str
    address: Address
    contacts: Contacts

person: Person  =  Person(
    name= 'John',
    age= 30,
    email= 'john.doe@example.com',
    address= Address(
        street= '123 Main St',
        city= "Anytown",
        state= 'NSW',
        postal_code= '2000',
        country= 'Australia'
        ),
   contacts =Contacts(
        emergency_contact= EmergencyContact(
            name= 'Bob',
            relation='Father',
            phone="555-123-4567"               
        ),
   ),   
)


print(f'{person.name= }')
print(f'{person.age= }')
print(f'{person.address.city= }')
print(f'{person.contacts.emergency_contact.name= }')
print(f'{person.contacts.emergency_contact.phone= }')