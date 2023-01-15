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




# we have NN list and NNP list -- check
# determine which classes we need to build? -- check
# build undefined classes -- check
# add knowledge (properties) to classes
# build objects



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

#    print('--- makeObjects ---')

    # Make all objects or just sentence objects?
    # Hmmm, let's just make sentence objects for now...
    #

#    print('    sA.inSent: ', sA.inSent)
#    print('    building sentence object(s)...')

    subjectLst = sA.sSubj.split(';')

#    print('    subjectLst: ', subjectLst)

    for s in subjectLst:
        sLst = s.split(',')
        subNames.append(sLst[0])

#    print('    subNames: ', subNames)


    objObjLst = sA.sObj.split(';')

#    print('    objObjLst: ', objObjLst)

    for o in objObjLst:
        oLst = o.split(',')
        objNames.append(oLst[0])

    # Make one big noun since nouns can be subjects and objects
    for i in nnList:
        nnxList.append(i)
        
    for i in nnpList:
        nnxList.append(i)

    for nnx in nnxList:

#        print('    nnx: ', nnx)
        
        if nnx[0] in subNames:
#            print('    nnx[0]: ', nnx[0])
#            print('    nnx[2]: ', nnx[2])
            name = nnx[0].capitalize()
            parentClass = nnx[2].capitalize()

#            print('    name: ', name)
#            print('    parentClass: ', parentClass)
            
            nnpObjLst.append(eval(parentClass)(name))

            # Update canDo if needed
            if nnpObjLst[-1]._canDo != nnx[3]:
#                print('no match')
#                print('nnpObjLst[-1]._canDo: ', nnpObjLst[-1]._canDo)
#                print('nnx[3]: ', nnx[3])
                nnpObjLst[-1]._canDo = nnx[3]
#                print('updated...')
#                print('nnpObjLst[-1]._canDo: ', nnpObjLst[-1]._canDo)
                
        elif nnx[0] in objNames:
#            print('    nnx[0]: ', nnx[0])
#            print('    nnx[2]: ', nnx[2])
            name = nnx[0].capitalize()
            parentClass = nnx[2].capitalize()

#            print('    name: ', name)
#            print('    parentClass: ', parentClass)
            
            nnObjLst.append(eval(parentClass)(name))

#    print('    nnpObjLst len: ', len(nnpObjLst))    
#    for o in nnpObjLst:
#        print('    o.name: ', o.name) 

#    print('    nnObjLst len: ', len(nnObjLst))    
#    for o in nnObjLst:
#        print('    o.name: ', o.name) 

#    print('--- return makeObjects ---')
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
    
    buildClasses()  # Define classes from 

    nnpObjects, nnObjects = makeObjects(sA)   # Construct objects (instances)


    print('    nnObjects len: ', len(nnObjects))
    
    for x in nnObjects:
        print('    x.name: ', x.name)

    print('    nnObjects: ', nnObjects)


    print('    ----')
    print('    nnpObjects len: ', len(nnpObjects))
    
    for x in nnpObjects:
        print('    x.name: ', x.name)

    print('    nnpObjects: ', nnpObjects)


    Daffy = Duck('Daffy')
