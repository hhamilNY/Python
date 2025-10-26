class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):      
        return self.size

    def __getitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value    
    
    def __setitem__(self, index, value):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(index):
            current = current.next
        current.value = value   

    def __delitem__(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        if index == 0:
            self.head = current.next
        else:
            for _ in range(index - 1):
                current = current.next
            current.next = current.next.next
        self.size -= 1

#defines behavior for 'in' operator
    def __contains__(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False    

#add a new node to the end of the list
    def append(self, value): 
        new_node = Node(value)
        if not self.head:
            self.head = new_node
              
        else:   
            current = self.head
            while current.next:
                current = current.next   
            current.next =new_node
        self.size += 1


    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values)
    
    def __repr__(self):
        return f"linkedList(size={self.size})"

    #example usage
def main():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    print(len(ll)) #output: 3
    print(ll[1]) #output: 20
    print(ll)   #output: 10 -> 20 -> 30
    del ll[1]
    print(ll)   #output: 10 -> 30   
    print(30 in ll) #output: True
    ll[1] = 25  
    print(ll)   #output: 10 -> 25
    print(repr(ll)) #output: linkedList(size=2)

if __name__ == "__main__":
    main()
    



       