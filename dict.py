# person: dict[str, str | int ] = {'name': 'Bob', 'age': 25}

type Person  = dict[str, str | int | bool | dict[str, str] | list[ dict [str, str]] ]


person: Person  = {
  "firstName": "John",
  "lastName": "Doe",
  "age": 30,
  "isStudent": False,
  "address": {
    "street": "123 Main St",
    "city": "Anytown",
    "zipCode": "12345"
  },
  "phoneNumbers": [
    {
      "type": "home",
      "number": "555-123-4567"
    },
    {
      "type": "work",
      "number": "555-987-6543"
    }
  ],
  "email": "john.doe@example.com"
}

print(person['firstName'])
print(person['age'])
print(person['phoneNumbers'])