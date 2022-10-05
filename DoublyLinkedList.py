from IR import IR
class DoublyLinkedList:

   def __init__(self):
      self.head = None
      self.tail = None

# Adding data elements		
   def push(self, NewVal):
        #Create a new node    
        newNode = IR(NewVal);    
            
        #If list is empty    
        if(self.head == None):    
            #Both head and tail will point to newNode    
            self.head = self.tail = newNode;    
            #head's prev will point to None    
            self.head.prev = None;    
            #tail's next will point to None, as it is the last node of the list    
            self.tail.next = None;    
        else:    
            #newNode will be added after tail such that tail's next will point to newNode    
            self.tail.next = newNode;    
            #newNode's prev will point to tail    
            newNode.prev = self.tail;    
            #newNode will become new tail    
            self.tail = newNode;    
            #As it is last node, tail's next will point to None    
            self.tail.next = None;    

# Print the Doubly Linked list		
   def listprint(self, node):
      while (node is not None):
         #print(node.item),
         prev = node
         node = node.next

   def reverse(self):
        #Node current will point to head    
        current = self.head;    
        #print(current)
            
        #Swap the prev and next pointers of each node to reverse the direction of the list    
        while(current != None):    
            temp = current.next;    
            current.next = current.prev;    
            current.prev = temp;    
            current = current.prev;    
        #Swap the head and tail pointers.    
        temp = self.head;    
        self.head = self.tail;    
        self.tail = temp;    