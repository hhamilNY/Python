class InventoryItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"InventoryItem(name={self.name}, quantity={self.quantity}, price={self.price})" 
    
    def __str__(self):
        return f"{self.name}: {self.quantity} units at ${self.price} each" 


#Arithemic Operations
#     
    def __add__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            return InventoryItem(self.name, self.quantity + other.quantity, self.price)     
        raise Exception("Invalid type or different item names") 

    def __sub__(self, other):
        if isinstance(other, InventoryItem) and self.name == other.name:
            if self.quantity >=other.quantity:
                return InventoryItem(self.name, self.quantity - other.quantity, self.price)
            raise 
            
        raise Exception("Invalid type or different item names")
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return InventoryItem(self.name, self.quantity, self.price * other)
        raise Exception("Invalid type for multiplication")  
    
    def truediv__(self, other):
        if isinstance(other, (int, float)):
            return InventoryItem(self.name, self.quantity, self.price / other)
        raise Exception("Invalid type for division") 


 #Comaorison Operations   
    def __eq__(self, other):
        if isinstance(other, InventoryItem):
            return (self.name == other.name and
                    self.quantity == other.quantity and
                    self.price == other.price)
        return False
          
    def __lt__(self, other):
        if isinstance(other, InventoryItem):
            return self.quantity < other.quantity
        raise Exception("Invalid type") 
    
    def __gt__(self,other):
        if isinstance(other, InventoryItem):
            return self.quantity > other.quantity
        raise Exception("Invalid type")
    
    
def main():
    item1 = InventoryItem("Widget", 10, 2.50)
    item2 = InventoryItem("Widget", 5, 2.50)
    item3 = InventoryItem("Gadget", 3, 5.00)

    print(item1)  # Uses __str__
    print(repr(item1))  # Uses __repr__

    combined_item = item1 + item2
    print(combined_item)  # Should show 15 units of Widget

    try:
        invalid_combination = item1 + item3
    except Exception as e:
        print(e)  # Should raise an exception

    reduced_item = item1 - item2
    print(reduced_item)  # Should show 5 units of Widget
    try:
        invalid_subtraction = item1 - item3
    except Exception as e:
        print(e)  # Should raise an exception

if __name__ == "__main__":
    main()  