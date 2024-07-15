# Linked list to the next level...
# Attempt to find SVO while being able
# to learn (add/modify) rules to find SVO

# Generate a linked list of rules for SVO
# extraction. Loads from starter ruleset,
# of from accumulated ruleset.
#
# I'm seeing a big problem of converting or
# constructing human rules into computer code.
# Not to mention how is the computer going to
# learn new or modify existing rules?
#
# Human teacher or additional data?
#
#

from svoRuleClasses import *

import pickle
ruleFileIn = 'data/nnxRules.txt'


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

# Load rules
def loadRules():
    nnxRules = []
    
    with open(ruleFileIn, 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                tmpRule = (tmp[0],tmp[1],tmp[2])
                nnxRules.append(tmpRule)

    return nnxRules

    


    """
        if tag in nnx:

            RULE 1:    
            if newSentObj.subject == None:
                newSentObj.subject = []
                newSentObj.subject.append(inputWord)
                currentWordPosition += 1
                processedSentence.append(inputWord)
                continue
            RULE 2:
            else:
                RULE 2.1:
                # Check for full name i.e. John Doe
                print('[-1]: ', processedSentence[-1])
                if processedSentence[-1]['tag'] == 'NNP':
                    # Where is it? Subject? object? or indirectObject?
                    # Using strict SVO:
                    if newSentObj.verb == None:
                        newSentObj.subject.append(inputWord)
                    else:
                        if newSentObj.object == None:
                            newSentObj.object = []
                        newSentObj.object.append(inputWord)
                    currentWordPosition += 1
                    processedSentence.append(inputWord)
                    continue


                RULE 2.2:
                # Is there a list? "Planes trains and boats are cool"
                # What if: "Planes, trains, and boats..."????
                if processedSentence[-1]['word'] == 'and':
                    subjectWords = getSubjectWords(newSentObj)
                    objectWords = getObjectWords(newSentObj)
                    
                    if processedSentence[-2]['word'] in subjectWords: 
                        sent.subject.append(inputWord)
                    elif processedSentence[-2]['word'] in objectWords:
                        sent.object.append(inputWord)
                        
                    currentWordPosition += 1
                    processedSentence.append(inputWord)
                    continue

                RULE 2.3:            
                # Default 
                if (newSentObj.verb != None) and (newSentObj.object == None):
                    newSentObj.object = []
                    newSentObj.object.append(inputWord)
                elif newSentObj.verb == None:
                    newSentObj.subject.append(inputWord)
                else:
                    # ?
                    if processedSentence[-1]['tag'] != 'NNP': # Check for John Doe?
                        newSentObj.object.append(inputWord)
                        
                        # Not worrying about direct or indirect objects
                        #
                        #if newSentObj.isVar('_indirectObject'):
                        #    newSentObj._indirectObject.append(inputWord)
                        #else:
                        #    newSentObj._indirectObject = []
                        #    newSentObj._indirectObject.append(inputWord)

        elif tag in prpx:
        
    """


if __name__ == "__main__":

    nnxRules = loadRules()

    
    llist = LinkedList()

    for r in nnxRules:
        nnxObj = Data(r[0], r[1], r[2])
            
        nnxObj.printData()

        llist.insertAtEnd(nnxObj)

    llist.printLL()
            

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
