#
# simpTree.py -- An attempt at a n-ary Tree KB 
#

from simpStuff import getInflections


class Node:
    def __init__(self, key, children=None):
        self.key = key
        self.parentNode = ''
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


def getEntries(which):

    newEntries = []

    if which == 'new':
        inFile = '/home/gary/src/s8/kb/newEntries.txt'
    elif which == 'start':
        inFile = '/home/gary/src/s8/kb/start.txt'
    elif which == 'nnp':
        inFile = '/home/gary/src/s8/kb/nnpEntries.txt'
    else:
        print('Unknown file entry type, must be "new", "start", or "nnp".')
        return newEntries
    
    with open(inFile, "r") as f:
        while (line := f.readline().rstrip()):
            tmp = eval(line)
            newEntries.append(tmp)
    f.close()

    return newEntries


def buildKB():

    tree = N_ary_Tree()
    hb = 'Higgs_Boson'

    tree.add(hb, ["TBD"]) # Root to start from

    starters = getEntries('start')

    for i in starters:
        newNodeParent = i["superclass"]
        newNode = i["name"]
        canDo = i["canDo"]
                    
        if tree.isNode(newNodeParent):
            tree.add(newNode, canDo, newNodeParent)
        else:
            print('starters: No parent/superclass {} found for: {}'.format(newNodeParent, newNode))

    results = getEntries('nnp')
    
    for i in results:
        newNodeParent = i["superclass"]
        newNode = i["name"]
        canDo = i["canDo"]
                    
        if tree.isNode(newNodeParent):
            tree.add(newNode, canDo, newNodeParent)
        else:
            print('No parent/superclass {} found for: {}'.format(newNodeParent, newNode))

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


def peruseData(sA):

    sentSubjects = []
    sentObjects  = []
    allSentVerbs = []
    prpFlag = False

    print('We be persuing...')
    print(sA.inSent)
    print('----')

    t = buildKB()

    sentSubjectsWithPOS = sA.sSubj.split(';')
    print('sentSubjectsWithPOS: ', sentSubjectsWithPOS)

    if sA.sObj != '':
        sentObjectsWithPOS = sA.sObj.split(';')
        print('sentObjectWithPOS: ', sentObjectsWithPOS)
    else:
        sentObjectsWithPOS = []
        print('No objects found in sentence...')        
    

    sentVerbs = sA.sVerb.split(',')
    # Get the verb conjugations/inflections
    for v in sentVerbs:
        v_inflections = getInflections(v, "VB")
        tmp = v_inflections.split(',')
        for i in tmp:
            allSentVerbs.append(i)

    print('sentVerbs: ', sentVerbs)
    sentVerbSet = set(sentVerbs)

    print('sentVerbSet: ', sentVerbSet)
    print('ALL VERBS wInflections:')
    print(allSentVerbs)
    
    allSentVerbSet = set(allSentVerbs)

    print('sA.sType: ', sA.sType)
    
    if sA.sType == 'imperative': # Implies Simp to do something, so can Simp do it?
        simpCanDo = t.get_canDo(t.root, 'Simp')
        simpCanDoSet = set(simpCanDo)
        print('simpCanDoSet: ', simpCanDoSet)

        intersectionSet1 = simpCanDoSet.intersection(allSentVerbSet)
        intersectionSet2 = allSentVerbSet.intersection(simpCanDoSet)
        
        differenceSet1 = allSentVerbSet.difference(simpCanDoSet)
        differenceSet2 = simpCanDoSet.difference(allSentVerbSet)

        print('Simp can 1: ', intersectionSet1)
        print('Simp can 2: ', intersectionSet2)
        
        print('Simp cannot 1: ', differenceSet1)
        print('Simp cannot 2: ', differenceSet2)

        if len(intersectionSet1) == 0 or len(intersectionSet2) == 0:
            intersectionSet3 = sentVerbSet.intersection(simpCanDoSet)
            intersectionSet4 = simpCanDoSet.intersection(sentVerbSet)

            print('Simp can 3: ', intersectionSet3)
            print('Simp can 4: ', intersectionSet4)

            differenceSet5 = sentVerbSet.difference(simpCanDoSet)
            differenceSet6 = simpCanDoSet.difference(sentVerbSet)

            print('Simp cannot 5:', differenceSet5)
            print('Simp can only 6:', differenceSet6)
        else:
            print('set len:', len(intersectionSet1))

    # Can the subject(s) do any of the verbs?
    for s in sentSubjectsWithPOS:
        tmp = s.split(',')
        
        if tmp[1] == 'PRP':
            prpFlag = True

        if tmp[1] in ['NP','NN','NNP']: # We wll deal with NNS later
            sCanDo = t.get_canDo(t.root, tmp[0])

            print('tmp[0]: ', tmp[0])
            print('canDo: ', sCanDo)

            if sCanDo == None:
                sCanDoSet = set()
            else:
                sCanDoSet = set(sCanDo)

            print('sCanDoSet:', sCanDoSet)
        
            print('sentVerbSet:')
            print(sentVerbSet)
      
            intersectionSet1 = sCanDoSet.intersection(allSentVerbSet)
            intersectionSet2 = allSentVerbSet.intersection(sCanDoSet)
        
            differenceSet1 = sCanDoSet.difference(allSentVerbSet)
            differenceSet2 = allSentVerbSet.difference(sCanDoSet)
        
            print(' can 1: ', intersectionSet1)
            print(' can 2: ', intersectionSet2)
            print(' cannot 1: ', differenceSet1)
            print(' cannot 2: ', differenceSet2)
            
        elif tmp[1] == 'PRP':
            print('PRP: tmp[0]: ', tmp[0])

            pp = processPronoun(tmp[0])

            print('processPronoun returned: ', pp)

        else:
            print('sSubj unknown: ', str(sA.sSubj))

    # Checking sentence objects

    for s in sentObjectsWithPOS:
        tmp = s.split(',')
        
        if tmp[1] in ['NP','NN','NNP']: # We wll deal with NNS later
            objCanDo = t.get_canDo(t.root, tmp[0])

            print('OBJ: tmp[0]: ', tmp[0])
            print('OBJ: canDo: ', objCanDo)


    return "Some great wizdom"


def processPronoun(prp):

    wc = []

    print('processPronoun: ', prp)

    convo = getConvo()

    print('----')

    t = buildKB()

    if prp == 'she':
        women = t.find_node(t.root, 'woman')

        for woman in women.children:
            wk = woman.key
            if len(convo) > 0:
                for c in convo:
                    for w in c:
                        if w == wk:
                            wc.append(c)
                          
        for i in wc: # All conversation sentences with women in them
            print('i: ', i)

    elif prp == 'you':
        simpCanDo = t.get_canDo(t.root, 'Simp')
        simpCanDoSet = set(simpCanDo)
        print('simpCanDoSet: ', simpCanDoSet)




    return "PRP relation to conversation"





def getConvo():

    fConvo = 'convoHist.txt'
    convo = []
    
    with open(fConvo, "r") as f:
        while (line := f.readline()):
            line = line.strip()
            if len(line) > 0:
                tmp = eval(line)
                convo.append(tmp)
    f.close()

    return convo






#
#
#
#
if __name__ == "__main__":
    
    t = buildKB()

    print(t)
    print('----')

    t = add2KB(t)

    print(t)
    
    
