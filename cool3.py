from random import choice, choices, sample

names: list[str] =['Bob', ' George', 'Anna', 'Sophia']

#Choose a random element from a non-empty sequence.

winner: str = choice(names)
print(f'{winner=}')

# gives 2 unique items from the list, make sure that
# items are unique in the list , might want to convert it to a set
#Chooses k unique random elements from a population sequence.
#Returns a new list containing elements from the population while leaving the original population unchanged. The resulting list is in selection order so that all sub-slices will also be valid random samples. This allows raffle winners (the sample) to be partitioned into grand prize and second place winners (the subslices).


winners: list[str] = sample(names, k=2 )
print(f'{winners=}')

random_names: list[str] = choices(names,k=2)
print(f'{random_names=}')

lotto: list[int] = sample(range(55), 6)
print(f'{lotto=}')

