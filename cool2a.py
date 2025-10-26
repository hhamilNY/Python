from itertools import product 


def main() -> None:

    #For example, product(A, B) returns the same as:    ((x,y) for x in A for y in B). The leftmost iterators are in the outermost for-loop, so the output tuples cycle in a manner similar to an odometer (with the rightmost element changing on every iteration).

    #To compute the product of an iterable with itself, specify the number of repetitions with the optional repeat keyword argument. For example, product(A, repeat=4) means the same as product(A, A, A, A).

    #product('ab', range(3)) --> ('a',0) ('a',1) ('a',2) ('b',0) ('b',1) ('b',2) 

    prod: product  = product('AB',range(3))

    #If iterable is specified the tuple is initialized from iterable's items.
    print(tuple(prod))

    


if __name__ == "__main__":
    main()
    
#(*iterables, repeat=1)
