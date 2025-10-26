from itertools import permutations, combinations_with_replacement

def permutations_example () -> None:
    pass
    
def main() -> None:

    perms: permutations[str] = permutations(['A', 'B', 'C']) # type: ignore
    permA: permutations[str] = permutations(['A', 'B', 'C']) # type: ignore



    for a, b, c in tuple(permA):
        print(a,b,c)

    type str_combs = combinations_with_replacement[str] # type: ignore
    combs: str_combs = combinations_with_replacement(['A', 'B', 'C'],3) # type: ignore
    print(tuple(combs))

    combsA: str_combs = combinations_with_replacement(['A', 'B', 'C'],3) # type: ignore

    for a, b, c in tuple(combsA):
        print(a,b,c)
        

if __name__ == "__main__":
    main()