#
# simpConfig.py
#
## Global var's

verbose = True

# Abstract class for a sentence
class Sentence:

    def __init__(self):
        self.inSent = None
        self.sPOS = None
        self.sType = None
        self.sSubj = None
        self.sVerb = None
        self.sObj = None
        self.sDet = None
        self.sIN = None
        self.sPP = None
        self.sMD = None

# Conrete class for an analyzed sentence
class analyzedSentence(Sentence):

    def __init__(self, inSent, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD):
        super().__init__()
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

# Abstract class or Thing is our root of the KB
#
class Thing:

    def __init__(self):
        self.name = None
        self.classInfo = 'Thing Class Root--Topmost Class'


# Concrete classes
#
class Vehicle(Thing):

    _classInfo = 'Vehicle Sub Class -- Of Thing'

    def __init__(self, name):
        super().__init__()
        self.name = name

class Device(Thing):

    _classInfo = 'Device Class Sub -- Of Thing'

    def __init__(self, name):
        super().__init__()
        self.name = name

class Recreation_ground(Thing):

    _classInfo = 'Recreation-ground Sub Class -- Of Thing'

    def __init__(self, name):
        super().__init__()
        self.name = name

class Animal(Thing):

    _classInfo = 'Animal Sub-Class -- Of Thing'

    def __init__(self, name):
        super().__init__()
        self.name = name
        
