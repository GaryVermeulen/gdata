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

