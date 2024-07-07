# Linked list to the next level...
# Attempt to find SVO while being able
# to learn (add/modify) rules to find SVO

from svoRuleClasses import *

import pickle
pickleFileIn = 'data/processedCorpora.p'


# Create a simple data class to store
# a wee bit more complex data within
# node of LL
#class Data:
#    def __init__(self, name, number):
#        self.name   = name
#        self.number = number
#
#    def printData(self):
#        print('name:   ', self.name)
#        print('number: ', self.number)


# Create a Node class to create a node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


# Create a LinkedList class
class LinkedList:
    def __init__(self):
        self.head = None

    # Method to add a node at begin of LL
    def insertAtBegin(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    # Method to add a node at any index
    # Indexing starts from 0.
    def insertAtIndex(self, data, index):
        new_node = Node(data)
        current_node = self.head
        position = 0
        if position == index:
            self.insertAtBegin(data)
        else:
            while(current_node != None and position+1 != index):
                position = position+1
                current_node = current_node.next

            if current_node != None:
                new_node.next = current_node.next
                current_node.next = new_node
            else:
                print("Index not present")

    # Method to add a node at the end of LL
    def insertAtEnd(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        current_node = self.head
        while(current_node.next):
            current_node = current_node.next

        current_node.next = new_node

    # Update node of a linked list
    # at given position
    def updateNode(self, val, index):
        current_node = self.head
        position = 0
        if position == index:
            current_node.data = val
        else:
            while(current_node != None and position != index):
                position = position+1
                current_node = current_node.next

            if current_node != None:
                current_node.data = val
            else:
                print("Index not present")

    # Method to remove first node of linked list
    def remove_first_node(self):
        if(self.head == None):
            return

        self.head = self.head.next

    # Method to remove last node of linked list
    def remove_last_node(self):
        if self.head is None:
            return

        current_node = self.head
        while(current_node.next.next):
            current_node = current_node.next

        current_node.next = None

    # Method to remove at given index
    def remove_at_index(self, index):
        if self.head == None:
            return

        current_node = self.head
        position = 0
        if position == index:
            self.remove_first_node()
        else:
            while(current_node != None and position+1 != index):
                position = position+1
                current_node = current_node.next

            if current_node != None:
                current_node.next = current_node.next.next
            else:
                print("Index not present")

    # Method to remove a node from linked list
    def remove_node(self, data):
        current_node = self.head

        if current_node.data == data:
            self.remove_first_node()
            return

        while(current_node != None and current_node.next.data != data):
            current_node = current_node.next

        if current_node == None:
            return
        else:
            current_node.next = current_node.next.next

    # Print the size of linked list
    def sizeOfLL(self):
        size = 0
        if(self.head):
            current_node = self.head
            while(current_node):
                size = size+1
                current_node = current_node.next
            return size
        else:
            return 0

    # print method for the linked list
    def printLL(self):
        current_node = self.head
        while(current_node):
            print(current_node.data)
            current_node.data.printData()
            current_node = current_node.next

    # Are all data.numbers > 0?
    def allDataTrue(self):
        current_node = self.head
        while(current_node):
            if current_node.data.number <= 0:
                return False
            current_node = current_node.next
        return True


if __name__ == "__main__":

    expandedCorpora = pickle.load( open(pickleFileIn, "rb" ) )

    print('len expandedCorpora: ', len(expandedCorpora))
    print('type expandedCorpora: ', type(expandedCorpora))

    for corpus in expandedCorpora:
        print('len of corpus: ', len(corpus))
        
        bookName = corpus[0]
        bookText = corpus[1]
            
        print('bookName: ', bookName)
        print('bookText: ')
        print(type(bookText))
        print(len(bookText))

        tmpCnt = 0
        for s in bookText:
            tmpCnt += 1
            print('=========: ', tmpCnt)
            #s.printAll()
            #print('---------')

            llist = LinkedList()
            nnxObj = Data(s.inputSent, s.taggedSent)
            

            nnxObj.printData()
            

            print('---------')
            
    """
    # create a new linked list
    llist = LinkedList()

    # add nodes to the linked list
    dataA = Data('a', 1)
    llist.insertAtEnd(dataA)

    dataB = Data('b', 2)
    llist.insertAtEnd(dataB)

    dataC = Data('c', 3)
    llist.insertAtBegin(dataC)

    dataD = Data('d', 4)
    llist.insertAtEnd(dataD)

    dataG = Data('g', -5)
    llist.insertAtIndex(dataG, 2)

    # print the linked list
    print("Node Data")
    llist.printLL()

    print("Are all nmbers greater than zero?")
    print(llist.allDataTrue())

    # remove a nodes from the linked list
    print("\nRemove First Node")
    llist.remove_first_node()
    print("Remove Last Node")
    llist.remove_last_node()
    print("Remove Node at Index 1")
    llist.remove_at_index(1)

    # print the linked list again
    print("\nLinked list after removing a node:")
    llist.printLL()

    print("\nUpdate node Value")
    dataZ = Data('z', 10)
    llist.updateNode(dataZ, 0)
    llist.printLL()

    print("\nSize of linked list :", end=" ")
    print(llist.sizeOfLL())

    print("Are all nmbers greater than zero?")
    print(llist.allDataTrue())

    """    
