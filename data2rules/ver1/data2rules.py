#
# data2rules.py
#

import sys
import pickle
import importlib
from rules import isTagNNx


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

# Create a function from the KB data and add it to rules
#
def createFunction(functionName, functionInput, functionReturnType):

    newRule = ''

    if functionReturnType == bool:
        print("create a {} function called {}".format(functionReturnType, functionName))

    if functionName not in rules:
        print('{} rule does not exist...'.format(functionName))

        # We'll start off crude (static) with only "is" something rule
        # (how can we make this dynamic?)
        #
        newRule += '\n'
        newRule += '# New Rule: ' + functionName + '\n'
        newRule += 'def ' + functionName + '(functionInput):\n'
        newRule += '\n'
        newRule += '    retVal = []\n'
        #newRule += '    for k in ' + str(functionInput) + ':\n'
        newRule += '    for k in functionInput:\n'
        newRule += '        if k["' + functionName + '"] == True:\n'
        newRule += '            retVal.append(k)\n'
        newRule += '\n'
        newRule += '    return retVal\n'
    else:
        print('{} rule exists...'.format(functionName))
        

    return newRule


def writeRules(rules):

    # Is it better to completely re-write rules?
    # Or append? For now, we re-write...

    rulesFile = 'rules.py'

    with open(rulesFile, 'w') as fr:
        fr.write(rules)
    fr.close()

    return "END writeRules"


def testRules():

    # Test starter rule:
    tag = 'NN'
    print('Tag = ', tag)
    result = isTagNNx(tag)
    print('isTagNNx Result = ', result)
    
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
    print('---rules to start')
    print(rules)
    print('----------')
    print(">>> Start test; testRules")
    testRules()
    print('----------')

    wantedList = []

    for k in kb:
        print('k:')
        print(k)
        myKeys = k.keys()

        wanted = 'is'

        #result = list(filter(lambda x: x.startswith(wanted), myKeys))
        # List-comprehension is a wee bit faster...
        result = [v for v in myKeys if v.startswith(wanted)]
        print('result:')
        print(result)

        for r in result:
            if r not in wantedList:
                wantedList.append(r)
              
        print('----')
    print('wantedList:')
    print(wantedList)
    print('----------')

    # Attempt to creat a "is" function
    functionName = wantedList[0]
    functionReturnType = bool
    functionInput = kb
    
#
    newRule = createFunction(functionName, kb, functionReturnType)

    print('----newRule:')
    print(newRule)

    rules += newRule
    print('----rules:')
    print(rules)

    print('---------- saving rules')
    
    writeRules(rules)

    print('----------')
    print('reloading: rules')
    importlib.reload(sys.modules['rules'])
    from rules import *
        
    print(">>> End test; testRules")
    testRules()

    res = 'UNK'
    try:
        print('trying new function...')
        res = isNonfiction(kb)
    except:
        print('it is too dumb not to know it has been re-loaded with the new function :-(')
        res = isNonfiction(kb)
        
        
    print(res)
