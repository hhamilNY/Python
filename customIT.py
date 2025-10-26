from typing import Iterator

class NameList:
    def __init__(self, names_str) -> None:
        self.names_str = names_str 

    def __iter__(self):
        self.names = self.names_str.split(',')
        self.index = 0
        return NameIterator(self.names_str)     

    # def add_name(self, name: str) -> None:
    #     self.names.append(name)

    # def get_names(self) -> list:
    #     return self.names

class NameIterator:
    def __init__(self, names_str) -> None:
            self.names = names_str.split(',')
            self.index = 0

    def __iter__(self):
            return self

    def __next__(self) -> str:
            if self.index < len(self.names):
                name = self.names[self.index].strip()
                self.index += 1
                return name
            else:
                raise StopIteration
            
def main() -> None:
    names = NameList('Alice    , Bob  ,   Charlie')
    for name in names:
        print(name)

if __name__ == "__main__":
    main()
