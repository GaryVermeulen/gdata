#
# simpReason.py
#
import simpConfig as sc
from simpStuff import getInflections as gI
from nltk.stem import PorterStemmer

ps = PorterStemmer()

nnpFile = "/home/gary/src/s6/data/nnp"
nnFile  = "/home/gary/src/s6/data/nn"
#nns?

# Root for Thing
#
class Thing:

    _classInfo = 'Thing Class Root'
    _isFood    = False

    def __init__(self, name):
        self.name = name


# Root for Animal
#
class Animal:

    _classInfo = 'Animal Class Root'
    _eat       = True
    _move      = True
    _isFood    = True

    def __init__(self, name):
        self.name = name
                

class Bird(Animal):
    _fly = True
#    def __init__(self, actions, *args, **kwargs):
#        self.actions = actions
#        super().__init__(*args, **kwargs)
    pass

class Duck(Bird):
    _swim = True
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Mammal(Animal):
    pass

class Canine(Mammal):
    pass

class Feline(Mammal):
    pass

class Dog(Canine):
    _tail = True
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)


class Cat(Feline):
    _tail = True
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Human(Mammal):
    pass

class Man(Human):
    _giveBirth = False
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Woman(Human):
    _giveBirth = True
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Self(Human):
    _think = True
    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)


# Other Things
#
class Device(Thing):
    pass    
    
class Computer(Device):

    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Instrument(Thing):
    pass

class Telescope(Instrument):

    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Vehicle(Thing):
    pass

class Bus(Vehicle):

    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

# Areas, places, spaces
#
class Recreation_ground:

    _classInfo = 'Recreation_ground Class Root'
    _isFood = False

    def __init__(self, name):
        self.name = name

class Park(Recreation_ground):

    def __init__(self, actions, *args, **kwargs):
        self.actions = actions
        super().__init__(*args, **kwargs)

class Playground(Park):
    pass

# End of Classes

def str2Var(s, exp):
    
    myVars = globals()
    myVars.__setitem__(s, exp)
 
    return


def readNNP():
    
    with open(nnpFile, 'r') as f:
        while (line := f.readline().rstrip()):
            if '#' not in line:
                line = line.replace(' ', '')
                ll = line.split(";")

                objName   = ll[0]
                baseClass = ll[2].capitalize()
                objActions = ll[3]

#                print("ll: ", ll)
#                print("objName: ", objName)
#                print("baseClass: ", baseClass)
#                print("objActions: ", objActions)

                if baseClass == "Computer":
                    str2Var(objName, Computer(objActions, objName))
               
                elif baseClass == "Man":
                    str2Var(objName, Man(objActions, objName))

                elif baseClass == "Woman":
                    str2Var(objName, Woman(objActions, objName))

                elif baseClass == "Cat":
                    str2Var(objName, Cat(objActions, objName))

                elif baseClass == "Duck":
                    str2Var(objName, Duck(objActions, objName))

    f.close()

    return


def readNN():

    nnList = []
    nnBaseClassLst = []
    
    with open(nnFile, 'r') as f:
        while (line := f.readline().rstrip()):
            if '#' not in line:
                line = line.replace(' ', '')
                ll = line.split(";")

                objName    = ll[0]
                baseClass  = ll[2].capitalize()
                objActions = ll[3]

                nnList.append(objName + ';' + baseClass + ';' + objActions)
                nnBaseClassLst.append(baseClass)
    f.close()

    print(nnList)
    print('-----...')
    print(nnBaseClassLst)

    return nnList, nnBaseClassLst


def testCognizance(sA, sD):

    vInflects = []
    canDo = []
    cannotDo = []
    vCount = -1

    simpCanDoList = []
    simpCannotDoList = []

    primarySubject = None
    secondarySubject = None

    primaryObject = None
    secondaryObject = None

    intersectionNNPVerb = "CAN"
    differenceVerbNNP   = "CANNOT"

    print("---- testCognizance ----")

###    readNNP() 

    with open(nnpFile, 'r') as f:
        while (line := f.readline().rstrip()):
            if '#' not in line:
                line = line.replace(' ', '')
                ll = line.split(";")

                objName   = ll[0]
                baseClass = ll[2].capitalize()
                objActions = ll[3]

#                print("ll: ", ll)
#                print("objName: ", objName)
#                print("baseClass: ", baseClass)
#                print("objActions: ", objActions)

                if baseClass == "Computer":
                    str2Var(objName, Computer(objActions, objName))
               
                elif baseClass == "Man":
                    str2Var(objName, Man(objActions, objName))

                elif baseClass == "Woman":
                    str2Var(objName, Woman(objActions, objName))

                elif baseClass == "Cat":
                    str2Var(objName, Cat(objActions, objName))

                elif baseClass == "Duck":
                    str2Var(objName, Duck(objActions, objName))

    f.close()

###

    nnList, bClassLst = readNN()

    sA_sSubjList = sA.sSubj.split(',')
    sA_sObjList =sA.sObj.split(',')

    # Do the sA attributes exist?
    print('sA_sSubjList: ', sA_sSubjList)

    # Repackage list into noun names and POS tag pairs
    # So we can process NNS different from NN or NNP
    NNxPair = []
    for sSubj in sA_sSubjList:
        if sSubj not in ['NN','NNP','NNS']:
            tmp = sSubj
        else:
            if sSubj == 'NNS':
                nonP = ps.stem(tmp)
                NNxPair.append(nonP + ',' + sSubj)
            else:
                NNxPair.append(tmp + ',' + sSubj)
            
    print('Final-NNxPair: ', NNxPair)

    for sSubj in NNxPair:
        print('sSubj: ', sSubj)
        sSubjLst = sSubj.split(',')
        print('sSubjLst: ', sSubjLst)
        
        if sSubjLst[0] not in ['NN','NNP','NNS']:
            print('if sSubjLst[0]: ', sSubjLst[0]) 
            if sSubjLst[0].capitalize() in globals():
                print("Found Subject: ", sSubjLst[0])
                print("cap: ", sSubjLst[0].capitalize())

                if primarySubject == None:
                    primarySubject = sSubjLst[0].capitalize()
                    print('primarySubject: ', primarySubject)
                    print(type(primarySubject))
                    
                else:
                    secondarySubject = sSubjLst[0].capitalize()
                    print('secondarySubject: ', secondarySubject)
                    print(type(secondarySubject))
                
                print("Continue...")
            else:
                print("Subject Not Found: ", sSubjLst[0])
                print("Exit...")

    print("....................")


    pSubObj = eval(primarySubject)
    print('After pSubObj = eval(primarySubject)   pSubObj._isFood: ', str(pSubObj._isFood))

    

    if secondarySubject is not None:
        sSubObj = eval(secondarySubject)
        print('After eval 2nd subj: ', str(sSubObj._isFood))
        print(type(pSubObj))

    print("....................")            
    print('sA_sObjList: ', sA_sObjList)
    print('len(sA_sObjList): ', len(sA_sObjList))

    if len(sA_sObjList) == 2:
        if sA_sObjList[1] == 'NNS':
            nonP = ps.stem(tmp)
        else:
            nonP = sA_sObjList[0]

        capNonP = nonP.capitalize()

        if capNonP in globals(): 
            primaryObject = eval(capNonP)

            if hasattr(primaryObject, 'name'):
                print('primaryObject.name: ', primaryObject.name)
                print('primaryObject.actions: ', primaryObject.actions)
            else:

                # test and create NN object
                print('test and create')
                print('primaryObject: ', primaryObject)

                if capNonP == 'Cat':
                    nnCat = capNonP
                    str2Var(nnCat, Cat({'eats food'}, nnCat))
                else:
                    return [], ['ERROR' , ' No object selection for: ', capNonP]

    else:
        print('Possible more than one sObj--len(sA_sObjList): ', len(sA_sObjList))



    print("....................")

    simpDoList = sD[3].split(',')
    simpDoSet = set(simpDoList)

    try:
        pSubVerbLst = nnCat.actions.split(',')
        print('try ok')
    except AttributeError:
        print('nnCat: ', nnCat)
        print(type(nnCat))
        print('exception...')
            
#        pSubInstance   str2Var(objName, Duck(objActions, objName))

    print('primaryObject test: ', primaryObject.name)
    print('actions:      ', primaryObject.actions)
    print(type(primaryObject))

        
    pSubVerbSet = set(pSubVerbLst)

    verbList = sA.sVerb.split(',')

    for v in verbList:
        vInflects.append(gI(v, "VB"))
    
    for i in vInflects:
        vCount += 1
        infList = i.split(',')

        verbSet  = set(infList)

        pSubVerbSet_intersect_verbSet = pSubVerbSet.intersection(verbSet)
        verbSet_diff_pSubVerbSet = verbSet.difference(pSubVerbSet)

        simpDoSet_intersect_verbSet = simpDoSet.intersection(verbSet)
        verbSet_diff_simpDoSet = verbSet.difference(simpDoSet)

        canDo.append(pSubVerbSet_intersect_verbSet)

        if len(pSubVerbSet_intersect_verbSet) == 0:
                cannotDo.append(verbList[vCount])
        else:
            if len(pSubVerbSet_intersect_verbSet) > 0:
                cannotDo.append('')
                
        simpCanDoList.append(simpDoSet_intersect_verbSet)

        if len(simpDoSet_intersect_verbSet) == 0:
            simpCannotDoList.append(verbList[vCount])
        else:
            if len(simpDoSet_intersect_verbSet) > 0:
                simpCannotDoList.append('')

    print("....................")
        

    print('simpCanDoList: ', simpCanDoList)
    print("-------")    
    
    # Clean up return values
    print('simpCanDoList:: ', simpCanDoList)
    tmp = simpCanDoList.copy()
    simpCanDoList.clear()
    print('tmp: ', tmp)
    for i in tmp:
        print('i: ', i)
        if len(i) > 0:
            if type(i) is set:
                simpCanDoList.append(i.pop())
            else:
                simpCanDoList.append(i)

    print('simpCannotDoList:: ', simpCannotDoList)        
    tmp = simpCannotDoList.copy()
    simpCannotDoList.clear()
    print('tmp: ', tmp)
    for i in tmp:
        print('i: ', i)
        if len(i) > 0:
            if type(i) is set:
                simpCannotDoList.append(i.pop())
            else:
                simpCannotDoList.append(i)
                
    print('canDo:: ', canDo)
    tmp = canDo.copy()
    canDo.clear()
    print('tmp: ', tmp)
    for i in tmp:
        print('i: ', i)
        print(type(i))
        if len(i) > 0:
            if type(i) is set:
                canDo.append(i.pop())
            else:
                canDo.append(i)

    print('cannotDo:: ', cannotDo)        
    tmp = cannotDo.copy()
    cannotDo.clear()
    print('tmp: ', tmp)
    for i in tmp:
        print('i: ', i)
        print(type(i))
        if len(i) > 0:
            if type(i) is set:
                cannotDo.append(i.pop())
            else:
                cannotDo.append(i)
    
            

    print("----cleaned----")

    print('simpCanDoList: ', simpCanDoList)
    print('simpCannotDoList: ', simpCannotDoList)

    print('canDo: ', canDo)
    print('cannotDo: ', cannotDo)


    print('---obj.isFood---')
    for i in canDo:
        print('Last i: ', i)
        print(vInflects)

        # Fix vInflects for just one verb set--baby steps
        tmp = vInflects[0]
        vInflects.clear()
        vInflects = tmp.split(',')
        if i in vInflects:

            if secondarySubject is not None:
            
                if sSubObj._isFood:
                    print('{} can eat {}'.format(pSubObj.name, sSubObj))
                else:
                    if primaryObject:
                        if primaryObject._isFood:
                            print('{} is edible'.format(primaryObject.name))
                        else:
                            print('{} is not edible'.format(primaryObject))


    return canDo, cannotDo
#    return "CAN", "CANNOT"


#
# Main
#
if __name__ == "__main__":


    startNew = True;

    if startNew:

        readNNP()

        # Does the obj exist for testVerbs?
        x = Bob.name
        
        if not x in dir():
            print("{} not defined".format(Bob))
            print(dir())
        else:
            print("Bob found")

            print("_" * 8)
        
            can, canNot = testVerbs(Bob, "eat,fly")

            print("can: ", can)
            print(type(can))
            print("canNot: ", canNot)
            print(type(can))
                
#        print("_" * 8)
#        print(globals()) 

    else:

        print("PICKLES SUCK")

        print("_" * 8)
        print(globals())

