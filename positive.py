class PositiveInt(int):
    def __new__(cls, value:int) -> int:
        if value <= 0:
            raise ValueError("Value must be positive")
        return super().__new__(cls, value)
    
def main() -> None:
    try:
        p = PositiveInt(10)
        print(f'Created PositiveInt: {p}')
        print(type(p))
                
        
        n = PositiveInt(-5)
        print(f'Created PositiveInt: {n}')
    except ValueError as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()
