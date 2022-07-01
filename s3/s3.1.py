#
# Simpleton data and slass testing
#

from dataclasses import dataclass

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

    def insertObj(self, data):
    # Compare the new value with the parent node
        if self.data:
            if data.name < self.data.name:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insertObj(data)
            elif data.name > self.data.name:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insertObj(data)
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

    # findval method to compare the value with nodes
    def findval(self, lkpval):
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
        #if lkpval < self.data.name:
        if lkpval < self.data[0]:
            if self.left is None:
                return str(lkpval)+" Not Found"
            return self.left.getVal(lkpval)
        #elif lkpval > self.data.name:
        elif lkpval > self.data[0]:
            if self.right is None:
                return str(lkpval)+" Not Found"
            return self.right.getVal(lkpval)
        else:
            # print(str(self.data) + ' is found')
            return self.data


# Older Class above
# Newer Class below


@dataclass
class NPP:
    # Class attribute
    species = "et al"

    name: str
    Ppt: str
    gender: str
    isA: str
    canDo: str

@dataclass
class NN:
    # Vauge since the lex is so small
    name: str
    Ppt: str
    isA: str
    canDo: str


fCFG = 'simp.cfg'
fData = 'data.txt'

myNPPs = []
myNNs = []

def getData():
    
    with open(fData, 'r') as f:       
        while (line := f.readline().rstrip()):
            if '#' not in line:
                line = line.replace(' ', '')
                line = line.split(";")

                if line[1] == 'NN':
                    print(line)
                    myNNs.append(line)
                elif line[1] == 'NNP':
                    print(line)
                    myNPPs.append(line)
    f.close()
    myNNs.sort()
    myNPPs.sort()
    
# END getData()


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

'''
getData()

# Determine approx mid of list for a somewhat balanced tree
print("i NNs")
for i in myNNs:
    print(i)

print("i NPPS")
for i in myNPPs:
    print(i)

myNPPsLen = len(myNPPs)
rootIndex = int(myNPPsLen / 2)
rootNPPs = Node(myNPPs[rootIndex])

print("NPP ROOT: " + str(rootNPPs))

for obj in myNPPs:
    if obj != rootNPPs:
        rootNPPs.insert(obj)
    print(obj)

print('\n------------ inorder:\n') 
print(rootNPPs.inorderTraversal(rootNPPs))
#
print('\n------------ preorder:\n')
print(rootNPPs.PreorderTraversal(rootNPPs))
#
print('\n------------ postorder:\n')
print(rootNPPs.PostorderTraversal(rootNPPs))

print('\n------------ PrintTree:\n')
rootNPPs.PrintTree()

print("\n========================")

# Determine approx mid of list for a somewhat balanced tree
# Update: No longer a sort list, so may have to figure something else
myNNsLen = len(myNNs)
rootIndex = int(myNNsLen / 2)
rootNNs = Node(myNNs[rootIndex])

print("\nNN ROOT: " + str(rootNNs))

for o in myNNs:
    if o != rootNNs:
        rootNNs.insert(o)
    print(o)


print('\n------------ inorder:\n') 
print(rootNNs.inorderTraversal(rootNNs))
#
print('\n------------ preorder:\n')
print(rootNNs.PreorderTraversal(rootNNs))
#
print('\n------------ postorder:\n')
print(rootNNs.PostorderTraversal(rootNNs))

print('\n------------ PrintTree:\n')
rootNNs.PrintTree()

"""
# Let's add something new...
# Going to need to know what it is: NNP, NN, etc...
objType = 'NN'
name = 'piano'
isA  = 'UNK'
canDo = 'UNK'
if objType == "NN":
    myNouns.append(NN(name,'Ppt',isA,canDo))
    i = len(myNouns)
    print(i)
    nounsRoot.insertObj(myNouns[i-1])
print("\nAfter add:\n")
print(str(myNouns[i-1]))
nounsRoot.PrintTree()
# So now we need to save the new info...
# First save to CFG file
lines = []
# Read existing CFG
with open(fCFG, 'r') as fin:        
    while (line := fin.readline().rstrip()):        
        lines.append(line)
fin.close()
print("\n")
print(len(lines))
print("\n")
inserted = False
    
# Search for the end of the given section ex: NN, NNP, DT, etc.
nw = name
nt = objType
    
lin_no = 0
match = False
exist = False 
for l in lines:
    l = l.replace("-", '')
    l = l.replace(" ", '')
    l = l.replace('"', '')
    l = l.split(">")
    if nw in l:
        exist = True
        break
    
    if l[0] == nt:
        match = True
    if l[0] == '#' and match:
        lines.insert(lin_no, str(nt) + ' -> "' + str(nw) +'"')
        inserted = True
        break
    lin_no += 1
print("\n")
print(len(lines))
print("\n")
        
# Overwrite with new input
if not exist:
    print('Adding nw: ' + nw)
    f = open(fCFG, 'w')
    for l in lines:
        f.write(l + '\n')
    f.close()
"""
#
# TO DO:
#   Add inflections
#   Save to actions.txt and isA.txt
#
'''
# What kind of knowledge can we glean?
#
# Note: walked manually inflected into walk
rawSentence = ['Mary', 'walk', 'Pookie', 'in', 'the', 'park']
'''
print(rawSentence[0])

ret0 = rootNPPs.getVal(rawSentence[0])
print(type(ret0))
print(ret0)
print('\n')

print(rawSentence[2])

ret2 = rootNPPs.getVal(rawSentence[2])
print(type(ret2))
print(ret2)
print('\n')

print(rawSentence[5])

ret5 = rootNNs.getVal(rawSentence[5])
print(type(ret5))
print(ret5)
'''
print('-----------')

sentenceData = []
bigData = getAllData()

for line in bigData:
    
    #print(line)

    res = any(item in rawSentence for item in line)

    if res:
        sentenceData.append(line)
    
for line in sentenceData:
    print(line)
    
print('\n')
print(rawSentence)

dataSentence = []

for word in rawSentence:
    for wordData in sentenceData:
        if word == wordData[0]:
            dataSentence.append(tuple((word, wordData)))

print('--------')
for word in dataSentence:
    print(word)

print('--------')

# wh-determiner
# Can we determine:
# who, when, where, what, which, how, why
#

# WHO
print('WHO:')
for who in dataSentence:
    if 'NNP' in who[1]:
        print(who[1])

# WHEN
# Assumptions:
#   VB  - Implies now
#   VBD - Implies past tense
#   VBG - Implies now
#   VBN - Implies past tense
#   VBZ - Impiles now
print('WHEN:')
for when in dataSentence:
    if ('VB' or 'VBG' or 'VBZ') in when[1]:
        print(when[1])
    
# WHERE
print('WHERE:')
for where in dataSentence:
    if 'NN' in where[1]:
        if 'p' in where[1][2]:
            print(where[1][2])
            print(where[1])        
# WHAT
print('WHAT: TODO')
# Pronoun:  'What is your name?'
#           'What we need is commitment'
# Determiner:   'What time is it?'
#               'He was robbed of what little money he had'
# Adverb:   'What does it matter?'
#           'What about half?'

# WHICH
print('WHICH: TODO')
'''
pronoun · determiner
determiner: which

    asking for information specifying one or more people or things from a definite set.
    "which are the best varieties of grapes for long keeping?"

pronoun · determiner
pronoun: which

    used referring to something previously mentioned when introducing a clause giving further information.
    "a conference in Vienna which ended on Friday"
'''

# HOW
print('HOW: TODO')
'''
adverb: how

    1.
    in what way or manner; by what means.
    "how does it work?"
    2.
    used to ask about the condition or quality of something.
    "how was your vacation?"
    used to ask about someone's physical or mental state.
    "how are the children?"
    3.
    used to ask about the extent or degree of something.
    "how old are you?"
    used to express a strong feeling such as surprise about the extent of something.
    "how kind it was of him"
    4.
    the way in which; that.
    "she told us how she had lived out of a suitcase for a week"
    in any way in which; however.
    "I'll do business how I like"
'''

# WHY
print('WHY: TODO')
