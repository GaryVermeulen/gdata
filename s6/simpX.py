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

    def __init__(self, name):
        self.name = name

class Device(Thing):

    _classInfo = 'Device Class Sub -- Of Thing'

    def __init__(self, name):
        self.name = name

class Recreation_ground(Thing):

    _classInfo = 'Recreation-ground Sub Class -- Of Thing'

    def __init__(self, name):
        self.name = name

class Animal(Thing):

    _classInfo = 'Animal Sub-Class -- Of Thing'

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

def constructor(self, arg):
    self.constructor_arg = arg


def makeObjects(sA):

    names = []
    objects = {}

    print('--- makeObjects ---')

    # Make all objects or just sentence objects?
    # Hmmm, let's just make sentence objects for now...
    #

    print('    sA.inSent: ', sA.inSent)
    print('    building sentence subject object(s)...')

    subjectLst = sA.sSubj.split(';')

    print('    subjectLst: ', subjectLst)

    for s in subjectLst:
        sLst = s.split(',')
        names.append(sLst[0])

    print('    names: ', names)
#    print('    nnpList: ', nnpList)

    for n in nnpList:

        print('    n: ', n)
        
        if n[0] in names:
            print('    n[0]: ', n[0])
            print('    n[2]: ', n[2])
            parentClass = n[2].capitalize()

            print('    parentClass: ', parentClass)
            
            #myVars.__setitem__(n[0], type(n[0], (eval(parentClass), ), dict(name=n[0])))
        
            globals()[n[0]] = type(n[0], (eval(parentClass), ), dict(name=n[0]))

            #objects[n[0]] = type(n[0], (eval(parentClass), ), {})
            #print(objects)


#    Daffy = Duck('Daffy')                               
    

    print('--- return makeObjects ---')
    return


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

    makeObjects(sA)   # Construct objects (instances)

    Daffy = Duck('Daffy')
