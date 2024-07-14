#
# data2rules.py
#

import pickle
from rules import *


def loadData():

    pickleFile = 'processedKB.p'

    with open(pickleFile, 'rb') as fp:
        myData = pickle.load(fp)
        print('Aunt Bee loaded: ', pickleFile)
    fp.close()
    
    return myData


def loadRules():

    rulesFile = 'rules.py'

    with open(rulesFile, 'r') as fr:
        myRules = fr.read()
    fr.close()

    return myRules



def testRules():

    # Test starter rule:
    tag = 'NN'
    print('Tag = ', tag)
    result = isTagNNx(tag)
    print('isTagNNx Result = ', result)

    print('---')

    retVal = isNonfiction()

    print('retVal:')
    for r in retVal:
        print(r)
    
    
    return "END testRules"


#
if __name__ == "__main__":

    kb = loadData()
    rules = loadRules()
    
    print('len kb: ', len(kb))
    print('type kb: ', type(kb))
    print('----------')
    print('len rules: ', len(rules))
    print('type rules: ', type(rules))
    print('---')
    print(rules)
    print('----------')
    print(">>> Start test; testRules")
    testRules()
        
    print(">>> End test; testRules")
    
