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

    def add(self, new_key, ppt, tag, canDo, parent_key=None):
        new_node = Node(new_key)
        new_node.ppt = ppt
        new_node.tag = tag
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
    root = 'thing'
    tree.add(root, '', '', ["TBD"]) # Root to start from

    for tmpDict in kb:
        newNodeParent = tmpDict["superclass"]
        newNode = tmpDict["name"]
        ppt = tmpDict["ppt"]
        tag = tmpDict["tag"]
        canDo = tmpDict["canDo"]

        if tree.isNode(newNode):
            print('Node already exist: ', newNode)
        else:
            if tree.isNode(newNodeParent):
                print('Adding: ', newNode, ppt, tag, canDo, newNodeParent)
                tree.add(newNode, ppt, tag, canDo, newNodeParent)
            else:
                # Doesn't work correctly and not needed if input is ordered
                print('! No parent/superclass {} found for: {}'.format(newNodeParent, newNode))
                stack = getSuperClassList(kb, newNode, [])
                for r in range(len(stack)):
                    s = stack.pop()
                    newNodeParent = s["superclass"]
                    newNode = s["name"]
                    ppt = s["ppt"]
                    tag = s["tag"]
                    canDo = s["canDo"]
                    print('...Adding: ', newNode, ppt, tag, canDo, newNodeParent)
                    tree.add(newNode, ppt, tag, canDo, newNodeParent)                
    return tree


def loadKB_Text():
    # Read the ordered starter kb file
    # For now only handling NNPs and NNs--we'll deal with plurals later

    nnxList = []
    
    with open('kb/orderedInput.txt', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                tmpDict = {
                    "name":tmp[0],
                    "ppt":tmp[1],
                    "tag":tmp[2],
                    "canDo":tmp[3],
                    "superclass":tmp[4],
                }
                nnxList.append(tmpDict)
    f.close()
                                   
    return nnxList


def getSuperClassList(kb, node, stack):
    # Logic is incorrect
    for k in kb:
#        print(k)
#        print('k[name]: ', k['name'])
        name       = k['name']
        superclass = k['superclass']
        
        if node == name:
            stack.append(k)
            kb.pop(0)            
            return getSuperClassList(kb, superclass, stack)
            
    return stack


def saveKB_Dict(kb):
    # Save new working KB...
    with open('pickles/newKB_Dict.pkl', 'wb') as fp:
        pickle.dump(kb, fp)
        print('Aunt Bee made a newKB_Dict pickle')
    fp.close()

    return


def saveKB_Tree(kbTree):
    # Save new working KB...
    with open('pickles/newKB_Tree.pkl', 'wb') as fp:
        pickle.dump(kbTree, fp)
        print('Aunt Bee made a newKB_Tree pickle')
    fp.close()

    return 



if __name__ == "__main__":

    print('Processing KB...')
    
    kb = loadKB_Text() 
    print('kb:')
    print(len(kb))
    print(type(kb))
    for k in kb:
        print(k)    
        
    print('-' * 5)

    saveKB_Dict(kb)
    print('-' * 5)

    t = buildKB_Tree(kb)
    print('t len: ', t.length())
    print('t:')
    print(t.print_tree(t.root, ''))
    print('-' * 5)

    saveKB_Tree(t)
    print('-' * 5)
    

    print('processKB Complete.')