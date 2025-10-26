from random import random, randint,randrange, choice, choices, shuffle, sample, seed

people: list[str] = [
    'Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
print(f'original list: {people}')
shuffle(people)
print(f'shuffled list: {people}')

value:float = random() #0.0 to 1.0
print(f'random value: {value}') 

values: list[int] = [randint(10,20 ) for _ in range(5)]
print(f'randomint() = {values}') 

values2: list[int] = [randrange(0,10, 2) for _ in range(5)]
print(f'randrange() = {values2}') 


people2: list[str] = [
    'Alice', 'Bob', 'Charlie', 'David', 'Eve']


print(f'original list: {people2}')
print(f'choice() = {choice(people2)}')
print(f'choices() = {choices(people2, k=5)}')

#using weights on list of people to increase chances of being chosen


weigths: tuple = (.15, .10, .10, .35, .30)

print(f'choices() with weights = {choices(people2, weights=weigths, k=5)}')

print(f'sample() of 3 int= {sample(([1,1,2,4]), k=3)}')
print(f'sample() from 100= {sample(range(100), k=10)}')

colors: list[str] = ['red', 'blue', 'green']
print(f'{sample(colors, k=5, counts=(10,20,5))}')


#setting seed for reproducibility
seed(1)
print(f'Random values with seed 1: {[random() for _ in range(3)]}')
print(f'Random values with seed 1: {randint(1,5) = }') 
print(f'{sample(range(1000), k=5) = }')


seed(10)
print(f'Random values with seed 10: {[random() for _ in range(3)]}')
print(f'Random values with seed 10: {randint(1,5) = }')
print(f'{sample(range(1000), k=5) = }')










#print(f'Random person: {choice(people)}')
#print(f'Random people: {choices(people, k=3)}')