#
# simpTree.py -- An attempt at a n-ary Tree KB 
#



class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.attributes = {'name':key}
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
	
    def get_attributes(self, node, key):
        if node == None or node.key == key:
            return node.attributes
        for child in node.children:
            return_node = self.find_node(child, key)
            if return_node:
                return return_node.attributes
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

    def add(self, new_key, parent_key=None):
        new_node = Node(new_key)
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


def getNewEntries():

    newEntries = []

    inFile = '/home/gary/src/s7/kb/newEntries.txt'

    with open(inFile, "r") as f:
        while (line := f.readline().rstrip()):
            print(type(line))
            print(line)
            tmp = eval(line)
            newEntries.append(tmp)
    f.close()

    return newEntries


def getStartEntries():

    newEntries = []

    inFile = '/home/gary/src/s7/kb/start.txt'

    with open(inFile, "r") as f:
        while (line := f.readline().rstrip()):
            print(type(line))
            print(line)
            tmp = eval(line)
            newEntries.append(tmp)
    f.close()

    return newEntries





if __name__ == "__main__":

    tree = N_ary_Tree()

    hb = 'Higgs_boson'

    tree.add(hb) # Root to start from
    

    """
    thing = 'Thing'
    animal = 'Animal'
    vehicle = 'Vehicle'
    device = 'Device'
    mammal = 'Mammal'
    bus = 'Bus'
    computer = 'Computer'
    instrument = 'Instrument'
    canine = 'Canine'
    feline = 'Feline'
    human = 'Human'
    telescope = 'Telescope'
    
    woman = 'Woman'

    bug = 'bug'
    unknown = 'unknownParent'
        
    
    tree.add(thing, hb)
    tree.add(animal, thing)
    tree.add(vehicle, thing)
    tree.add(device, thing)
    tree.add(mammal, animal)
    tree.add(bus, vehicle)
    tree.add(computer, device)
    tree.add(instrument, device)
    tree.add(canine, mammal)
    tree.add(feline, mammal)
    tree.add(human, mammal)
    tree.add(telescope, instrument)
    tree.add(man, human)
    tree.add(woman, human)
    
    #    tree.add(bug, unknown)
    """

    starters = getStartEntries()

    for i in starters:
        print('i: ', i)
        keyValue = i["superclass"]
        newNode = i["name"]
        
        print('keyValue: ', keyValue)
        keyValue = keyValue.capitalize()
        print('keyValue: ', keyValue)

        print('newNode: ', newNode)
        newNode = newNode.capitalize()
        print('newNode: ', newNode)
            
        if tree.isNode(keyValue):
            print('Found: ', keyValue)    
            tree.add(newNode, keyValue)
        else:
            print('No parent/superclass {} found for: {}'.format(keyValue, newNode))



    print('N-ary tree size:', tree.length())
    print(tree)

    man = 'Man'
    print('man: ', man)
    #result = tree.depth(human)
    print(tree.depth(man))
    #print(len(result) + 1)

    print(tree.isNode(man))
    print('------')
#    print(tree.isNode(bug))
#    print('------')
#    if tree.isNode(bug) == None:
#        print('Yep, there is no: ', bug)
    print('---getNewEntries---')
    
    results = getNewEntries()

    print('------')
    print(results)

    print('------')
    
    for i in results:
        print('i: ', i)
        keyValue = i["superclass"]
        newNode = i["name"]
        
        print('keyValue: ', keyValue)
        keyValue = keyValue.capitalize()
        print('keyValue: ', keyValue)

        print('newNode: ', newNode)
        newNode = newNode.capitalize()
        print('newNode: ', newNode)
            
        if tree.isNode(keyValue):
            print('Found: ', keyValue)    
            tree.add(newNode, keyValue)
        else:
            print('No parent/superclass {} found for: {}'.format(keyValue, newNode))

    print('------')
    print('N-ary tree size:', tree.length())
    print(tree)
