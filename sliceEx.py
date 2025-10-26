numbers: list[int] = list(range(1,11))
text: str ='Hello, World!'

line_break: str = '-' * 25

print(f'{numbers=}')
print(f'{text=}')

print(line_break)


rev: slice = slice(None, None, -1)
f_five: slice = slice(None,5)

print(f'{numbers[rev]=}')
print(f'{text[rev]=}')

print(line_break)

print(f'{numbers[f_five]=}')
print(f'{text[f_five]=}')