# mutable  is [] can not change must use 
#def add_to_list(n:int, target_list: list[int] = []) ->list[int]: - otherwise it is shared

def add_to_list(n:int, target_list: list[int] | None = None) ->list[int]:
    if target_list is not None:
        target_list.append(n)
    else:
        target_list = [n]

    return target_list

first: list[int] = add_to_list(1)
print(first)
second: list[int] = add_to_list(2)
print(second)
print(first)

def main():
    pass

if __name__ == '__main__':
    main()