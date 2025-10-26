set_a: set[int] = {1, 2, 3, 4, 5}
set_b: set[int] = {4, 5, 6, 7, 8}
set_c: set[int] = {6, 7, 8, 9, 10}

set_a |= set_b 

print(f'{set_a =}')

print(f'{set_b | set_c =}')
print(f'{set_b - set_c =}')
print(f'{set_b & set_c =}')
print(f'{set_b ^ set_c =}')  # sysmatic difference - unique items


