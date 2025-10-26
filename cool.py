from functools import partial       
def specifications(color: str, name:str, amount: int) -> None:
    print(f'Specs: {color=}, {name=}, {amount=}')


specifications('RED', 'Bob', 10)
specifications('Blue', 'Ann', 10)
specifications('Green', 'Bob', 20)

amount_spec: partial = partial(specifications, 'RED', 'Bob')
amount_spec(10)

color_name_spec: partial = partial(specifications,  amount=20)
color_name_spec('RED', 'Bob')

color_spec: partial = partial(specifications, name= 'Susan', amount = 25)
color_spec('Black')

name_spec: partial = partial(specifications, 'Red', amount=20)
name_spec('Greg')
