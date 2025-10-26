from typing import TypedDict

class EmergencyContact (TypedDict):
    name: str
    relation: str
    phone: str

class Contacts(TypedDict):
    emergency_contact: EmergencyContact

class Address(TypedDict):
    street: str
    city: str
    state: str
    postal_code: str
    country: str

class Person(TypedDict):
    name: str
    age: int
    email: str
    address: Address
    contacts: Contacts

person: Person  = {
    'name': 'John',
    'age': 30,
    'email': 'john.doe@example.com',
    'address': {
        'street': '123 Main St',
        'city': "Anytown",
        'state': 'NSW',
        'postal_code': '2000',
        'country': 'Australia',
  },
   'contacts': {
      'emergency_contact': {
            'name': 'Bob',
            'relation': 'Father',
            'phone':"555-123-4567",               
       },
   },
}


print(f'{person['name']= }')
print(f'{person['age']= }')
print(f'{person['address']['city']= }')
print(f'{person['contacts']['emergency_contact']['name']= }')
print(f'{person['contacts']['emergency_contact']['phone']= }')