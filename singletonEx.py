from typing import Any

class Singleton: 
    _instance: 'Singleton | None' = None
    _initialized: bool = False 

    def __new__(cls, *args: Any, **kwargs: Any) -> 'Singleton':
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance
    
    def __init__(self, name: str) -> None:
        if not self._initialized:
            self._initialized = True
            self.name = name

 
def main() -> None:
    s1: Singleton = Singleton("First")
    s2: Singleton = Singleton("Second")

    print(f's1 is s2: {s1 is s2}')

    print(f's1 name: {s1.name}')  
    print(f's2 name: {s2.name}')  

    

if __name__ == "__main__":
    main()  