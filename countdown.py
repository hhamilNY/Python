class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        else:
            value = self.current
            self.current -= 1
            return value
        
    def __repr__(self):
        return f"Countdown(start={self.current + 1})"   
    
    def __str__(self):
        return f"Countdown currently at {self.current + 1}"             
    
def main():
    countdown = Countdown(5)
    for number in countdown:
        print(number)       
    print(repr(countdown))
    print(str(countdown))

if __name__ == "__main__":
    main()