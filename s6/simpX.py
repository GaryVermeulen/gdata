#
# simpX.py -- Read text data to build classes & KB
#

import inspect
import simpConfig as sc
from simpStuff import getData

# Root class
#
class Thing:

    _classInfo = 'Thing Class Root--Topmost Class'

    def __init__(self, name):
        self.name = name

# Current sub classes
#
class Vehicle(Thing):

    _classInfo = 'Vehicle Sub Class -- Of Thing'
    _canDo = 'TBD'

    def __init__(self, name):
        self.name = name

class Device(Thing):

    _classInfo = 'Device Class Sub -- Of Thing'
    _canDo = 'TBD'

    def __init__(self, name):
        self.name = name

class Recreation_ground(Thing):

    _classInfo = 'Recreation-ground Sub Class -- Of Thing'
    _canDo = 'TBD'

    def __init__(self, name):
        self.name = name

class Animal(Thing):

    _classInfo = 'Animal Sub-Class -- Of Thing'
    _canDo = 'see,eat,walk,run'

    def __init__(self, name):
        self.name = name


# globals
#
classes2Build = []
myVars = globals()
buildStack = []
nnList = []
nnpList = []
nnpObjLst = []
nnObjLst = []


def makeObjects(sA):

    global nnpObjLst
    global nnObjLst
    
    global nnList
    global nnpList

    subNames = []
    objNames = []

    nnxList = []
    
    nnObjLst.clear()
    nnpObjLst.clear()

    subjectLst = sA.sSubj.split(';')

    for s in subjectLst:
        sLst = s.split(',')
        subNames.append(sLst[0])

    objObjLst = sA.sObj.split(';')

    for o in objObjLst:
        oLst = o.split(',')
        objNames.append(oLst[0])

    # Make one big noun since nouns can be subjects and objects
    for i in nnList:
        nnxList.append(i)
        
    for i in nnpList:
        nnxList.append(i)

    for nnx in nnxList:        
        if nnx[0] in subNames:
            name = nnx[0].capitalize()
            parentClass = nnx[2].capitalize()
            nnpObjLst.append(eval(parentClass)(name))

            # Update canDo if needed
            if nnpObjLst[-1]._canDo != nnx[3]:
                nnpObjLst[-1]._canDo = nnx[3]
                
        elif nnx[0] in objNames:
            name = nnx[0].capitalize()
            parentClass = nnx[2].capitalize()            
            nnObjLst.append(eval(parentClass)(name))

    return nnpObjLst, nnObjLst


def makeClass(c):

    global buildStack
    global classes2Build

    try:
        result = inspect.isclass(eval(c[1]))    # result can be used for debugging
        myVars.__setitem__(c[0], type(c[0], (eval(c[1]), ), {}))       
    except NameError:
        buildStack.append(c)

        for i in classes2Build:
            if i[0] == c[1]:
                makeClass(i)
    return


def buildClasses():

    global buildStack
    global classes2Build
    global nnList
    global nnpList

    if __name__ != "__main__":
        inData = getData()
        nnList, nnpList = extractNN(inData)


    for nn in nnList:
        n0 = nn[0].capitalize()
        n2 = nn[2].capitalize()
        try:
            result = inspect.isclass(eval(n0))  # result can be used for debugging
        except NameError:
            classes2Build.append(list((n0, n2)))
           
    for c in classes2Build:
            makeClass(c)

            for item in buildStack: # Backtracks/catches in between classes 
                makeClass(item)

            buildStack.clear()

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

    ''' Sample test data when running as standalone

    Input sentence w/corrected case:
    ['Mary', 'walked', 'Pookie', 'in', 'the', 'park']
    ----------------------
    sPOS =   
    sType =  declarative
    sSubj =  Mary,NNP;Pookie,NNP
    sVerb =  walked
    sObj =   park,NN
    sDet =   the
    sIN =    in
    sPP =    in,the,park,NN
    sMD =
    '''
    class Sentence:

        def __init__(self, inSent, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD):
            self.inSent = inSent
            self.sPOS = sPOS
            self.sType = sType
            self.sSubj = sSubj
            self.sVerb = sVerb
            self.sObj = sObj
            self.sDet = sDet
            self.sIN = sIN
            self.sPP = sPP
            self.sMD = sMD

    s = ['Mary', 'walked', 'Pookie', 'in', 'the', 'park']
    sPOS = ''
    sType = 'declarative'
    sSubj = 'Mary,NNP;Pookie,NNP'
    sVerb = 'walked'
    sObj = 'park,NN'
    sDet = 'the'
    sIN = 'in'
    sPP = 'in,the,park,NN'
    sMD = ''

    print('=== simpX (main) ===')

    inData = getData()
    nnList, nnpList = extractNN(inData)

    sA = Sentence(s, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD)
    
    print('inData len: ', len(inData))
    print('inData type: ', type(inData))
    print('nnList len: ', len(nnList))
    print('nnList type: ', type(nnList))
    print('nnpList len: ', len(nnpList))
    print('nnpList type: ', type(nnpList))
    
    buildClasses()  # Define classes from nn file

    nnpObjects, nnObjects = makeObjects(sA)   # Make objects (instances)

    print('    nnObjects len: ', len(nnObjects))    
    for x in nnObjects:
        print('    x.name: ', x.name)
        print('    x._canDo: ', x._canDo)
        print('    x._classInfo: ', x._classInfo)

    print('    nnObjects: ', nnObjects)
    print('    ----')
    print('    nnpObjects len: ', len(nnpObjects))
    for x in nnpObjects:
        print('    x.name: ', x.name)
        print('    x._canDo: ', x._canDo)
        print('    x._classInfo: ', x._classInfo)
            
    print('    nnpObjects: ', nnpObjects)

    print('[0].name: ', nnpObjects[0].name)
    print('[0] Cat?: ', isinstance(nnpObjects[0], Cat))
    print('[0] Woamn?: ', isinstance(nnpObjects[0], Woman))
    print('[0] Human?: ', isinstance(nnpObjects[0], Human))
    print('[0] Mammal?: ', isinstance(nnpObjects[0], Mammal))
    print('[1].name: ', nnpObjects[1].name)
    print('[1] Cat?: ', isinstance(nnpObjects[1], Cat))
    print('[1] Woman: ', isinstance(nnpObjects[1], Woman))
    print('[1] Human?: ', isinstance(nnpObjects[1], Human))
    print('[1] Mammal?: ', isinstance(nnpObjects[1], Mammal))
    
