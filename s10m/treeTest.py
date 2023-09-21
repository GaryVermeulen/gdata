#
# treeTest.py -- An attempt at a n-ary Tree KB with MongoDB
#

import pymongo

from commonUtils import connectMongo



"""
*** DB structure for KB in MongoDB

        _id:        "String name"
        similar:    "CSV String, item, item,...,n"
        tag:        "NN" or "NNP"
        isAlive:    True or False
        canDo:      "String of simple canDo, item, item,...,n"
        superclass: "String of parent or superclass"
    
"""


class Node:
    def __init__(self, key):
        self.key         = key 
        self.similar     = ''
        self.tag         = ''
        self.isAlive     = False
        self.canDo       = ''
        self.parent_node = ''
        self.children    = []

    def __str__(self):
        return str(self.key)

    def get_childern(self):
        return self.childern


class N_ary_Tree:

    def __init__(self):
        self.root = None
        self.size = 0

    def find_node(self, node, key):
        if node == None or node.key == key:
            return node
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node
        return None

    def isNode(self, key):
        node = self.find_node(self.root, key)
        if not(node):
            return False
        else:
            return True
	
    def get_canDo(self, node, key):
        if node == None or node.key == key:
            return node.canDo
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.canDo
        return None

    def depth(self, key):
        node = self.find_node(self.root, key)
        if not(node):
            raise NodeNotFoundException('Depth: No element was found with the informed parent key.')
        return self.max_depth(node)

    def max_depth(self, node):
        if not(node.children):
            return 0
        children_max_depth = []
        for child in node.children:
            children_max_depth.append(self.max_depth(child))
        #return 1 + max(children_max_depth)
        return len(children_max_depth) + 1

    def add(self, new_key, similar, tag, isAlive, canDo, parent_node, children):
        new_node = Node(new_key)
        new_node.similar = similar
        new_node.tag = tag
        new_node.isAlive = isAlive
        new_node.canDo = canDo
        new_node.parent_node = parent_node
        new_node.children = children
        if parent_node == None:
            self.root = new_node
            self.size = 1
        else:
            parent_node = self.find_node(self.root, parent_node)
            if not(parent_node):
                print(' ' + str(parent_node) + ' Is not a parent--cannot add: ' + new_key)
                raise NodeNotFoundException('Add: No element was found with the informed parent key.')
            parent_node.children.append(new_node)
            self.size += 1

    def print_tree(self, node, str_aux):
        if node == None: return ""
        str_aux += str(node) + '('
        for i in range(len(node.children)):
            child = node.children[i]
            end = ',' if i < len(node.children) - 1 else ''
            str_aux = self.print_tree(child, str_aux) + end
        str_aux += ')'
        return str_aux

    def is_empty(self):
        return self.size == 0

    def length(self):
        return self.size

    def __str__(self):
        return self.print_tree(self.root, "")


class NodeNotFoundException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)



def buildKB(nnxKB):

    tree = N_ary_Tree()

    root = list(nnxKB.find({"_id":"GodParticle"}))
    children = []

    print('root: ', root)

    tree.add(root[0]["_id"],
             root[0]["similar"],
             root[0]["tag"],
             root[0]["isAlive"],
             root[0]["canDo"],
             root[0]["superclass"],
             children) # Root to start from

    starters = nnxKB.find() 

    for i in starters:
        
        newNode = i["_id"]
        similar = i["similar"]
        tag = i["tag"]
        isAlive = i["isAlive"]
        canDo = i["canDo"]
        newNodeParent = i["superclass"]
        children = []
                    
        if tree.isNode(newNodeParent):
            tree.add(newNode, similar, tag, isAlive, canDo, newNodeParent, children)
        else:
            print('starters: No parent/superclass {} found for: {}'.format(newNodeParent, newNode))

    return tree


def add2KB(tree):

    results = getEntries('new')
  
    for i in results:
        newNodeParent = i["superclass"]
        newNode = i["name"]
        canDo = i["canDo"]
                    
        if tree.isNode(newNodeParent):
            tree.add(newNode, canDo, newNodeParent)
        else:
            print('No parent/superclass {} found for: {}'.format(newNodeParent, newNode))

    return tree



#
#
#
#
if __name__ == "__main__":

    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    taggedCorpus = simpDB["taggedCorpus"]
    
    t = buildKB(nnxKB)

    print(t)
    print('----')

    #t = add2KB(t)

    print(t)
    
    
