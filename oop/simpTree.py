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
        print( self.data),
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


print('--- start ---')
#root = Node(27)
#
#root.insert(14)
#root.insert(35)
#root.insert(10)
#root.insert(19)
#root.insert(31)
#root.insert(42)

root = Node('S')

root.insert('VP')
root.insert('VB')
root.insert('see')
root.insert('NP')
root.insert('NP')
root.insert('NP')
root.insert('NNP')
root.insert('bob')
root.insert('VP')
root.insert('VB')
root.insert('run')
root.insert('PP')
root.insert('IN')
root.insert('in')
root.insert('NP')
root.insert('DT')
root.insert('the')
root.insert('NN')
root.insert('park')

print('--- tree constructed ---')
print('    PrintTree:')
root.PrintTree()

print('    inorderTraversal:')
print(root.inorderTraversal(root))

print('    PreorderTraversal:')
print(root.PreorderTraversal(root))

print('    PostorderTraversal:')
print(root.PostorderTraversal(root))


print('--- End ---')
