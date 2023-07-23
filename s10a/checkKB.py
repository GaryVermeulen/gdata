#
# checkKB.py
#

import pickle

from commonUtils import loadPickle
from commonUtils import savePickle
from commonUtils import insertKBNode

from simpConfig import Sentence
from simpConfig import Node
from simpConfig import N_ary_Tree
from simpConfig import NodeNotFoundException


def chkKB(sA_Obj, kbTree):

    print('---- chkKB ----')

    print(sA_Obj.inSent)
    NNs = []
    for n in sA_Obj.inSent:                 # KB only has NNs and NNPs (no NNS)
        if n[1] in ['NNP', 'NN', 'NNS']:    # No NNS at this time but thinking ahead ;-)
            NNs.append(n)

    nnNodes = []
    for n in NNs:
        node = kbTree.find_node(kbTree.root, n[0])
        if node != None:
            nnNodes.append(node)
        else:
            print('{} is not in the current KB!'.format(n))
    """
    for node in nnNodes:
        print(node.key)
        print(node.parentNode)
        print(node.similar)
        print(node.tag)
        print(node.canDo)
        print(node.children)
    """

    print('---- chkKB complete ----')

    return nnNodes

    

if __name__ == "__main__":

    print(' --- checkKB __main__ ---')

    # setup test input
    taggedInput = [('the', 'DT'), ('cat', 'NN'), ('in', 'IN'), ('the', 'DT'), ('hat', 'NN')]
    sType = 'declarative'
    sSubj = 'cat'
    sVerb = ''
    sObj = 'hat'
    sInObj = ''
    sAdj = ''
    sDet = [('the', 'DT'), ('the', 'DT')]
    sIN = ('in', 'IN')
    sPP = ''
    sMD = ''
    sWDT = ''
    sCC = ''

    sent = Sentence(taggedInput, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)
    kbTree = loadPickle('kbTree')
    
    kbNodes = chkKB(sent, kbTree)

    for node in kbNodes:
        print('---')
        print(node.key)
        print(node.parentNode)
        print(node.similar)
        print(node.tag)
        print(node.canDo)
        print(node.children)
        for c in node.children:
            print(c)
   
    print('\n --- checkKB Complete __main__ ---')
    
    
