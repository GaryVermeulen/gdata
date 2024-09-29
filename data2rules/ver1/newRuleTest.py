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



def testRules(kb):

    # Test starter rule:
    tag = 'NN'
    print('Tag = ', tag)
    result = isTagNNx(tag)
    print('isTagNNx Result = ', result)

    print('---')

    retVal = isNonfiction(kb)

    print('retVal:')
    for r in retVal:
        print(r)

    print('---')

    #res = isX('isNonfiction', kb)
    res = isX('isAlive', kb)

    print('res:')
    for r in res:
        print(r)

    print('---')

    if retVal == res:
        print('They match!')
    else:
        print('They do not match...')
    
    
    return "\nEND testRules"


#
if __name__ == "__main__":

    kb = loadData()
    rules = loadRules()
    kbCount = 0
    
    print('len kb: ', len(kb))
    print('type kb: ', type(kb))
    for k in kb:
        kbCount += 1
        print('{}; k: {}'.format(kbCount, k))
        
    print('----------')
    print('len rules: ', len(rules))
    print('type rules: ', type(rules))
    print('---')
    print(rules)
    print('----------')
    print(">>> Start test; testRules")
    testRules(kb)
        
    print(">>> End test; testRules")
    
