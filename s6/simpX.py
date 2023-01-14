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

    _classInfo = 'Vehicle Class Root--Of Thing'

    def __init__(self, name):
        self.name = name

class Device(Thing):

    _classInfo = 'Device Class Root--Of Thing'

    def __init__(self, name):
        self.name = name

class Recreation_ground(Thing):

    _classInfo = 'Recreation-ground Class Root--Of Thing'

    def __init__(self, name):
        self.name = name

class Animal(Thing):

    _classInfo = 'Animal Class Root--Of Thing'

    def __init__(self, name):
        self.name = name




# we have NN list and NNP list -- check
# determine which classes we need to build? -- check
# build undefined classes -- check
# build objects

# globals
#
classes2Build = []
myVars = globals()
buildStack = []
nnList = []
nnpList = []


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

    print('=== simpX (main) ===')

    inData = getData()
    nnList, nnpList = extractNN(inData)
    
    print('inData len: ', len(inData))
    print('inData type: ', type(inData))
    print('nnList len: ', len(nnList))
    print('nnList type: ', type(nnList))
    print('nnpList len: ', len(nnpList))
    print('nnpList type: ', type(nnpList))
    
    buildClasses()  # Define classes from 

