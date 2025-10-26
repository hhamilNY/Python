from dataclasses import dataclass, KW_ONLY 

#short for data class with the replacement commented below
@dataclass(kw_only=True)
class Fruit:
    name: str
    grams: float

   
#class Fruit:
#    def __init__(self, *, name: str, grams: float) -> None:
#       self.name = name
#       self.grams = grams


class Basket:
    def __init__(self, *, fruits: list[Fruit]) -> None:
        self.fruits = fruits 
    def __getitem__(self, item: str) -> list[Fruit]: 
        return [fruit for fruit in self.fruits if fruit.name.lower() == item]
    

def main() -> None:
    fruits: list[Fruit] = [
        Fruit(name='Apple', grams=150),
        Fruit(name='Apple', grams=200),
        Fruit(name='Banana', grams=120),
        Fruit(name='Orange', grams=130),
        Fruit(name='Orange', grams=300),
        Fruit(name='Grapes', grams=200),
    ]
    basket: Basket = Basket(fruits=fruits)

    matches: list[Fruit] = basket['apple']
    print(f'Found {len(matches)} apples in the basket:')
    print(f'Matches: {matches}')

    matches: list[Fruit] = basket['banana']
    print(f'Found {len(matches)} banana in the basket:')
    print(f'Matches: {matches}')
     

if __name__ == '__main__':
    main()