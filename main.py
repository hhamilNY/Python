
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def get_count(self):
        return self.count
    
    def count_up(self):
        self.count += 1  
    
    def count_down(self):
        self.count -= 1

    def __str__(self):
        return f"Counter(count={self.count})" 
    
    def __repr__(self):
        return f"Counter(count={self.count})"   

    def __add__(self, other):
        if isinstance(other, Counter):
            return Counter.from_count(self.count + other.count)
        raise Exception("ivalid.type")  
    
    def __sub__(self, other):
        if isinstance(other, Counter):
            return Counter.from_count(self.count - other.count)
        raise Exception("ivalid.type")
    

def main():
    print("Hello from object!")


if __name__ == '__main__':
    main()
