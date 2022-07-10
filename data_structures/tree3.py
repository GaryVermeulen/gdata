# Data and structures (classes, lists, tuples, hashes, dicts, hybirds)
#

class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
    # Compare the new value with the parent node
        # Original recursive code
        #if self.data:
        #    if data < self.data:
        #        if self.left is None:
        #            self.left = Node(data)
        #        else:
        #            self.left.insert(data)
        #    elif data > self.data:
        #        if self.right is None:
        #            self.right = Node(data)
        #        else:
        #            self.right.insert(data)
        #else:
        #    self.data = data

        # Non-recursive
        #  Create a new node
#        node = TreeNode(data)
        if (self == None):
            #  When adds a first node in bst
            self.data = data
        else:
            find = self
	    #  Add new node to proper position
            while (find != None):
                if (find.data >= data):
                    if (find.left == None):
                        #  When left child empty
			#  So add new node here
                        find.left = data
                        return
                    else:
                        #  Otherwise
                        #  Visit left sub-tree
                        find = find.left		
                else:
                    if (find.right == None):
                        #  When right child empty
                        #  So add new node here
                        find.right = data
                        return
                    else:
                        #  Visit right sub-tree
                        find = find.right


    # Print the tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data)   # WHat does this comma do? ,
        if self.right:
            self.right.PrintTree()

    # Inorder traversal
    # Left -> Root -> Right
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res

    # Preorder traversal
    # Root -> Left ->Right
    def PreorderTraversal(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.PreorderTraversal(root.left)
            res = res + self.PreorderTraversal(root.right)
        return res

    # Postorder traversal
    # Left ->Right -> Root
    def PostorderTraversal(self, root):
        res = []
        if root:
            res = self.PostorderTraversal(root.left)
            res = res + self.PostorderTraversal(root.right)
            res.append(root.data)
        return res

    # findval method to compare the value with nodes
    def findval(self, lkpval):
        print('start')
        if lkpval < self.data:
            if self.left is None:
                return str(lkpval)+" Not Found"
            return self.left.findval(lkpval)
        elif lkpval > self.data:
            if self.right is None:
                return str(lkpval)+" Not Found"
            return self.right.findval(lkpval)
        else:
            print(str(self.data) + ' is found')

    # getVal method to compare the value with nodes
    def getVal(self, lkpval):
        if lkpval < self.data:
            if self.left is None:
                return str(lkpval)+" Not Found"
            return self.left.getVal(lkpval)
        elif lkpval > self.data:
            if self.right is None:
                return str(lkpval)+" Not Found"
            return self.right.getVal(lkpval)
        else:
            # print(str(self.data) + ' is found')
            return self.data

 
    # Iterative function for inorder tree traversal
    def inOrder(root):
     
        # Set current to root of binary tree
        current = root
        stack = [] # initialize stack
     
        while True:
         
            # Reach the left most Node of the current Node
            if current is not None:
             
                # Place pointer to a tree node on the stack
                # before traversing the node's left subtree
                stack.append(current)
         
                current = current.left
 
         
            # BackTrack from the empty subtree and visit the Node
            # at the top of the stack; however, if the stack is
            # empty you are done
            elif(stack):
                current = stack.pop()
                print(current.data, end=" ") # Python 3 printing
         
                # We have visited the node and its left
                # subtree. Now, it's right subtree's turn
                current = current.right
 
            else:
                break
      
        print()

        

fData = 'data.txt'
fDict = 'dict.csv'

def getAllData():

    allData = []
    
    with open(fData, 'r') as f:       
        while (line := f.readline().rstrip()):
            if '#' not in line:
                line = line.replace(' ', '')
                line = line.split(";")

                if line[0] != '#':
                #    print(line)
                    allData.append(line)
                
    f.close()
    return allData
# END getAllData()


def getDict():

    allDict = []
    
    with open(fDict, 'r') as f:       
        while (line := f.readline().rstrip()):
            if '#' not in line:
            #    line = line.replace(' ', '')
                line = line.split(",")

                if line[0] != '#':
                #    print(line)
                    allDict.append(line)
                
    f.close()
    return allDict
# END getDict()



#myDict = getDict()

#print(len(myDict))
#print(type(myDict))

#for d in myDict:
#    print(d)


###
# Not be able to use cuurent tree objects for large
# datasets with Python recursion limit of 1000
#
###
# 
#allData = getAllData()
#
#print(len(allData))
#
#for d in allData:
#    print(d)
#    
#allData.sort()
#
#print(type(allData))
#print(len(allData))
#
#for s in allData:
#    print(s)

# Use the insert method to add nodes
# Orginal sample data
#root = Node(12)
#root.insert(6)
#root.insert(14)
#root.insert(3)

#nodeA = 3
#nodeB = 6
#nodeC = 12
#nodeD = 14
#nodeE = 32
#nodeF = 64

# max dicts
# 2^27 = 134,217,728
#
#MAX = 134217728
#halfMAX = 134217728 / 2
# Python max recursion is 1000
#
MAX = 180000 # 2001 # Max with recursion
halfMAX = MAX / 2
#
print(MAX)
print(str(int(halfMAX)))
#
root = Node(int(halfMAX))
#
for n in range(MAX):
    root.insert(n)


#nodeA = ['A', 'red', 'apple', 'tree']
#nodeB = ['B', 'blue', 'bird', 'sky']
#nodeC = ['C', 'green', 'bean', 'tree']
#nodeD = ['D', 'dog', 'paw', 'tail']
#nodeE = ['E', 'cat', 'paw', 'claw']
#nodeF = ['F', 'frank', 'man', 'hat']
#
#root = Node(nodeD)
#root.insert(nodeA)
#root.insert(nodeB)
#root.insert(nodeC)
#root.insert(nodeE)
#root.insert(nodeF)

#print('root.PrintTree')
#root.PrintTree()
#print('inorder')
#print(root.inorderTraversal(root))
#print('preorder')
#print(root.PreorderTraversal(root))
#print('postorder')
#print(root.PostorderTraversal(root))

#print('--------')
#print(root.findval(3))
#print('--------')
#print(root.findval(1))

#print(root.findval(['E', 'cat', 'paw', 'claw']))

#print('--------')
#ret = root.getVal(1)
#print(ret)

