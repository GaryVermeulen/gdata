#
# simpX.py -- Read text data to build classes & KB
#

import inspect
import simpConfig as sc
from simpStuff import getData


# Abstract classes
#
class Thing:

    def __init__(self):
        self.name = None
        self.classInfo = 'Thing Class Root--Topmost Class'
        self.fly_Behavior = None
        self.run_Behavior = None
        self.walk_Behavior = None
        self.eat_Behavior = None
        self.see_Behavior = None

    def get_name(self):
        return self.name

    def get_classInfo(self):
        return self.classInfo

    def set_fly_Behavior(self, fly_Behavior):
        self.fly_Behavior = fly_Behavior
        
    def set_run_Behavior(self, run_Behavior):
        self.run_Behavior = run_Behavior

    def set_walk_Behavior(self, walk_Behavior):
        self.walk_Behavior = walk_Behavior

    def set_eat_Behavior(self, eat_Behavior):
        self.eat_Behavior = eat_Behavior

    def set_see_Behavior(self, see_Behavior):
        self.see_Behavior = see_Behavior



class seeBehavior:

    def See(self):
        raise NotImplementedError

class canSee(seeBehavior):

    def See(self):
        print("I can see")

class cannotSee(seeBehavior):

    def See(self):
        print("I cannot see")

class eatBehavior:

    def Eat(self):
        raise NotImplementedError

class canEat(eatBehavior):

    def Eat(self):
        print("I can eat")

class cannotEat(eatBehavior):

    def Eat(self):
        print("I cannot eat")

class walkBehavior:

    def Walk(self):
        raise NotImplementedError

class canWalk(walkBehavior):

    def Walk(self):
        print("I can walk")

class cannotWalk(walkBehavior):

    def Walk(self):
        print("I cannot walk")

class runBehavior:

    def Run(self):
        raise NotImplementedError

class canRun(runBehavior):

    def Run(self):
        print("I can run")

class cannotRun(runBehavior):

    def Run(self):
        print("I cannot run")

class flyBehavior:

    def Fly(self):
        raise NotImplementedError

class canFly(flyBehavior):

    def Fly(self):
        print("I can fly")

class cannotFly(flyBehavior):

    def Fly(self):
        print("I cannot fly")


class Functions:

    def Magnify(self):
        raise NotImplementedError

    def Transport(self):
        raise NotImplementedError

    def Recreation(self):
        raise NotImplementedError

    def Play(self):
        raise NotImplementedError

    def Compute(self):
        raise NotImplementedError


# Concrete classes -- L1 (layer 1 of KB)
#
class Recreation_groundThing(Thing):

    def __init__(self):
        super().__init__()
        self.name = "Recreation_groundThing name"
        self.classInfo = "Recreation_groundThing class info"

    def printBase(self):
        for base in self.__class__.__bases__:
            print(base.__name__)

class AnimalThing(Thing):

    def __init__(self):
        super().__init__()
        self.name = "AnimalThing name"
        self.classInfo = "AnimalThing class info"

    def printBase(self):
        for base in self.__class__.__bases__:
            print(base.__name__)

class VehicleThing(Thing):

    def __init__(self):
        super().__init__()
        self.name = "VehicleThing name"
        self.classInfo = "VehicleThing class info"

class DeviceThing(Thing):

    def __init__(self):
        super().__init__()
        self.name = "DeviceThing name"
        self.classInfo = "DeviceThing class info"


# Inherited conrete classes  -- L2 (layer 2 of KB)
#
class busVehicleThing(VehicleThing):

    def __init__(self):
        super().__init__()
        self.name = "busVehicleThing name"
        self.classInfo = "busVehicleThing class info"

class computerDeviceThing(DeviceThing):

    def __init__(self):
        super().__init__()
        self.name = "computerDeviceThing name"
        self.classInfo = "computerDeviceThing class info"

class instrumentDeviceThing(DeviceThing):

    def __init__(self):
        super().__init__()
        self.name = "instrumentDeviceThing name"
        self.classInfo = "instrumentDeviceThing class info"

class parkRecreation_groundThing(Recreation_groundThing):

    def __init__(self):
        super().__init__()
        self.name = "parkRecreation_ground name"
        self.classInfo = "parkRecreation_ground class info"

    def printBase(self):
        for base in self.__class__.__bases__:
            print(base.__name__)


class birdAnimalThing(AnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "birdAnimalThing name"
        self.classInfo = "birdAnimalThing class info"

    def printBase(self):
        for base in self.__class__.__bases__:
            print(base.__name__)

class mammalAnimalThing(AnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "mammalAnimalThing name"
        self.classInfo = "mammalAnimalThing class info"


# Inherited conrete classes  -- L3 (layer 3 of KB)
#
class playgroundParkRecreation_groundThing(parkRecreation_groundThing):

    def __init__(self):
        super().__init__()
        self.name = "playgroundParkRecreation_groundThing name"
        self.classInfo = "playgroundParkRecreation_groundThing class info"

    def printBase(self):
        for base in self.__class__.__bases__:
            print(base.__name__)

class humanMammalAnimalThing(mammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "humanMammalAnimalThing name"
        self.classInfo = "humanMammalAnimalThing class info"

class felineMammalAnimalThing(mammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "felineMammalAnimalThing name"
        self.classInfo = "felineMammalAnimalThing class info"

class canineMammalAnimalThing(mammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "canineMammalAnimalThing name"
        self.classInfo = "canimeMammalAnimalThing class info"

class duckBirdAnimalThing(birdAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "duckBirdAnimalThing name"
        self.classInfo = "duckBirdlAnimalThing class info"

class telescopeInstrumentDeviceThing(instrumentDeviceThing):

    def __init__(self):
        super().__init__()
        self.name = "telescopeInstrumentDeviceThing name"
        self.classInfo = "telescopeInstrumentDeviceThing class info"


# Inherited conrete classes  -- L4 (layer 4 of KB)
#
class selfHumanMammalAnimalThing(humanMammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "selfHumanMammalAnimalThing name"
        self.classInfo = "selfHumanMammalAnimalThing class info"

class womanHumanMammalAnimalThing(humanMammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "womanHumanMammalAnimalThing name"
        self.classInfo = "womanHumanMammalAnimalThing class info"

class manHumanMammalAnimalThing(humanMammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "manHumanMammalAnimalThing name"
        self.classInfo = "manHumanMammalAnimalThing class info"

class catFelineMammalAnimalThing(felineMammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "catFelineMammalAnimalThing name"
        self.classInfo = "catFelineMammalAnimalThing class info"
        self.see_Behavior = canSee()
        self.eat_Behavior = canEat()
        self.walk_Behavior = canWalk()
        self.run_Behavior = canRun()
        self.fly_Behavior = cannotFly()

class dogCanineMammalAnimalThing(canineMammalAnimalThing):

    def __init__(self):
        super().__init__()
        self.name = "dogCanineMammalAnimalThing name"
        self.classInfo = "dogCanimeMammalAnimalThing class info"

        
# Creator class
class ThingMaker:

    def createThing(self, whichThing):
        raise NotImplementedError

    def prepThing(self, whichThing):
        print('ThingMaker; prepThing: ', whichThing)
        thing = self.createThing(whichThing)
        return thing


# Concrete classes
class Vehicle(ThingMaker):

    def createThing(self, whichThing):
        chooser = {
            "bus": busVehicleThing()
        }
        return chooser.get(whichThing)

class Device(ThingMaker):

    def createThing(self, whichThing):
        chooser = {
            "computer": computerDeviceThing(),
            "instrument": instrumentDeviceThing()
        }
        return chooser.get(whichThing)

class Animal(ThingMaker):

    def createThing(self, whichThing):
        chooser = {
            "bird": birdAnimalThing(),
            "mammal": mammalAnimalThing()
        }
        return chooser.get(whichThing)

class Recreation_ground(ThingMaker):

    def createThing(self, whichThing):
        chooser = {
            "park": parkRecreation_groundThing()
        }
        return chooser.get(whichThing)

class Feline(ThingMaker):

    def createThing(self, whichThing):
        chooser = {
            "cat": felineMammalAnimalThing()
        }
        return chooser.get(whichThing)

class Cat(ThingMaker):

    def createThing(self, whichThing):
        chooser = {
            "pookie": catFelineMammalAnimalThing()
        }
        return chooser.get(whichThing)
        
#
#

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


    print('=== simpX1 (main) ===')

    inData = getData()
    nnList, nnpList = extractNN(inData)

    sA = sc.analyzedSentence(s, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD)
    
    print('inData len: ', len(inData))
    print('inData type: ', type(inData))
    print('nnList len: ', len(nnList))
    print('nnList type: ', type(nnList))
    print('nnpList len: ', len(nnpList))
    print('nnpList type: ', type(nnpList))


    myAnimal = Animal()    
    myBird = myAnimal.prepThing("bird")
    print(f"We made a {myBird.get_name()}\n")


    myRecGround = Recreation_ground()
    myPark = myRecGround.prepThing("park")
    print(f"We made a {myPark.get_name()}\n")


    myFeline = Feline()
    myCat = myFeline.prepThing("cat")
    print(f"We made a {myCat.get_name()}\n")


    myP_Cat = Cat()
    pookie = myP_Cat.prepThing("pookie")
    pookie.name = "Pookie"
    print(f"And POOF there is  {pookie.get_name()}\n")