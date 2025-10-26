from timeit import timeit 


def append_text() -> str:
    result: str = ""
    for i in range(50):
        result += "Hello, World! "
    return result   

def append_text_join() -> str:
    result: list[str] = []
    for i in range(50):
        result.append("Hello, World! ")
    return ''.join(result)

line_break: str = '-' * 40

def main() -> None:
    print(line_break)
    time1 = timeit(append_text, number=10_000)
    print(f'Appending with += took: {time1:.5f} seconds')

    time2 = timeit(append_text_join, number=10000)
    print(f'Appending with join() took: {time2:.5f} seconds')
    print(line_break)

    print(f'Same results? {append_text() == append_text_join()}') 
    print(line_break)

if __name__ == "__main__":
    main()
