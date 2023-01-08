#
# simpX.py -- Read text data and build classes to determine knowledge
#

import simpConfig as sc
from simpStuff import getData

# Root classes
#

class Thing:

    _classInfo = 'Thing Class Root'

    def __init__(self, name):
        self.name = name

class Place(Thing):

    _classInfo = 'Thing Class Root'
    _isFood    = False

    def __init__(self, name):
        self.name = name













def buildClasses(class2Build):


    print('--- buildClasses ---')

    exp = 'some expression'

    myVars = globals()
    myVars.__setitem__(class2Build, exp)


    return


def extractNN(inData):

    nnLst = []
    nnpLst = []

    for i in inData:
        if len(i) == 5:
            if i[4] in ['NN']:
                nnLst.append(i)
            elif i[4] in ['NNP']:
                nnpLst.append(i)

    return nnLst, nnpLst

if __name__ == "__main__":

    print('=== simpX (main) ===')

    inData = getData()

    nnList, nnpList = extractNN(inData)
    
    print('inData len: ', len(inData))
    print('inData type: ', type(inData))

#    for i in inData:
#        print('i len: ', len(i))
#        print('i type: ', type(i))
#        print('i: ', i)
#        print('----')
#
#    print('nnList len: ', len(nnList))
#    print('nnpList len: ', len(nnpList))
#
#    for i in nnList:
#        print(i)
#
#    print('---')
#
#    for i in nnpList:
#        print(i)
        
    x = 'Bob'
    
    buildClasses(x)
