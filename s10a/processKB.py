#
# processKB.py
#

import pickle

# Classes For an n-ary Tree KB
#
class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.parentNode = ''
        self.ppt = ''
        self.tag = ''
        self.canDo = []
        self.children = children or []

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

    def add(self, new_key, canDo, parent_key=None):
        new_node = Node(new_key)
        new_node.canDo = canDo
        new_node.parentNode = parent_key
        if parent_key == None:
            self.root = new_node
            self.size = 1
        else:
            parent_node = self.find_node(self.root, parent_key)
            if not(parent_node):
                print(' ' + str(parent_key) + ' Is not a parent--cannot add: ' + new_key)
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


def buildKB_Tree(kb):

    tree = N_ary_Tree()
    hb = 'Higgs_Boson'

    tree.add(hb, ["TBD"]) # Root to start from

    for tmpDict in kb:
        newNodeParent = tmpDict["superclass"]
        newNode = tmpDict["name"]
        ppt = tmpDict["ppt"]
        tag = tmpDict["tag"]
        canDo = tmpDict["canDo"]
                       
        if tree.isNode(newNodeParent):
            tree.add(newNode, ppt, tag, canDo, newNodeParent)
        else:
            print('starters: No parent/superclass {} found for: {}'.format(newNodeParent, newNode))
    """
    results = getEntries('nnp')
    
    for i in results:
        newNodeParent = i["superclass"]
        newNode = i["name"]
        canDo = i["canDo"]
                    
        if tree.isNode(newNodeParent):
            tree.add(newNode, canDo, newNodeParent)
        else:
            print('No parent/superclass {} found for: {}'.format(newNodeParent, newNode))
    """
    return tree



def loadKB():
    # Read the starter kb files
    # For now only handling NNPs and NNs--we'll deal with plurals later

    nnpList = []
    nnxList = []
    
    with open('kb/nnp', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                tmpDict = {
                    "name":tmp[0],
                    "ppt":tmp[1],
                    "tag":'NNP',
                    "superclass":tmp[2],
                    "canDo":tmp[3]
                }
                nnpList.append(tmpDict)
    f.close()

    with open('kb/nn', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                tmpDict = {
                    "name":tmp[0],
                    "ppt":tmp[1],
                    "tag":'NN',
                    "superclass":tmp[2],
                    "canDo":tmp[3]
                }
                nnxList.append(tmpDict)
    f.close()               
                                   
    return nnpList + nnxList


def saveKB(kb):
    # Save new working KB...
    with open('newKB.pkl', 'wb') as fp:
        pickle.dump(kb, fp)
        print('Aunt Bee made a newKB pickle')
    fp.close()

    return 


if __name__ == "__main__":

    print('Processing KB...')
    
    kb = loadKB()
    print('kb:')
    print(len(kb))
    print(type(kb))
    for k in kb:
        print(k)
    print('-' * 5)

    saveKB(kb)
    print('-' * 5)

    t = buildKB_Tree(kb)
    print('-' * 5)
    print('processKB Complete.')
