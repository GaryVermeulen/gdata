#
# processKB.py
#

import pickle

from simpConfig import Node
from simpConfig import N_ary_Tree
from simpConfig import NodeNotFoundException


def buildKB_Tree(kb):

    tree = N_ary_Tree()
    root = 'thing'
    tree.add(root, 'all', 'NN', ["everything"]) # Root to start from

    for tmpDict in kb:
        newNodeParent = tmpDict["superclass"]
        newNode = tmpDict["name"]
        similar = tmpDict["similar"]
        tag = tmpDict["tag"]
        canDo = tmpDict["canDo"]

        if tree.isNode(newNode):
            print('Node already exist: ', newNode)
        else:
            if tree.isNode(newNodeParent):
                print('Adding: ', newNode, similar, tag, canDo, newNodeParent)
                tree.add(newNode, similar, tag, canDo, newNodeParent)
            else:
                # Doesn't work correctly and not needed if input is ordered
                print('! No parent/superclass {} found for: {}'.format(newNodeParent, newNode))
                stack = getSuperClassList(kb, newNode, [])
                for r in range(len(stack)):
                    s = stack.pop()
                    newNodeParent = s["superclass"]
                    newNode = s["name"]
                    similar = s["similar"]
                    tag = s["tag"]
                    canDo = s["canDo"]
                    print('...Adding: ', newNode, similar, tag, canDo, newNodeParent)
                    tree.add(newNode, ppt, tag, canDo, newNodeParent)                
    return tree


def loadKB_Text():
    # Read the ordered starter kb file
    # For now only handling NNPs and NNs--we'll deal with plurals later

    nnxList = []
    
    with open('kb/orderedInputLong.txt', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                print(tmp)
                tmpDict = {
                    "name":tmp[0],
                    "similar":tmp[1],
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
    # Save new working KB list of dictionaries...
    with open('pickles/kbDict.pkl', 'wb') as fp:
        pickle.dump(kb, fp)
        print('Aunt Bee made a kbDict pickle')
    fp.close()

    return


def saveKB_Tree(kbTree):
    # Save new working KB tree...
    with open('pickles/kbTree.pkl', 'wb') as fp:
        pickle.dump(kbTree, fp)
        print('Aunt Bee made a kbTree pickle')
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
