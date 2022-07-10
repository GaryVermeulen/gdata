class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
    # Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

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

# Use the insert method to add nodes
# Orginal sample data
#root = Node(12)
#root.insert(6)
#root.insert(14)
#root.insert(3)

nodeA = 3
nodeB = 6
nodeC = 12
nodeD = 14
nodeE = 32
nodeF = 64


#nodeA = ['A', 'red', 'apple', 'tree']
#nodeB = ['B', 'blue', 'bird', 'sky']
#nodeC = ['C', 'green', 'bean', 'tree']
#nodeD = ['D', 'dog', 'paw', 'tail']
#nodeE = ['E', 'cat', 'paw', 'claw']
#nodeF = ['F', 'frank', 'man', 'hat']
#
root = Node(nodeD)
root.insert(nodeA)
root.insert(nodeB)
root.insert(nodeC)
root.insert(nodeE)
root.insert(nodeF)

print('root.PrintTree')
root.PrintTree()
print('inorder')
print(root.inorderTraversal(root))
print('preorder')
print(root.PreorderTraversal(root))
print('postorder')
print(root.PostorderTraversal(root))

print('--------')
print(root.findval(3))
print('--------')
print(root.findval(1))

#print(root.findval(['E', 'cat', 'paw', 'claw']))

print('--------')
ret = root.getVal(1)
print(ret)
