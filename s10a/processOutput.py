#
# processOutput.py
#

import pickle

from commonUtils import *
from simpConfig import *


def prattle(sA_Obj):

    osType = 'output'
    osSubj = ''
    osVerb = ''
    osObj = ''
    osInObj = ''
    osAdj = ''
    osDet = ''
    osIN = ''
    osPP = ''
    osMD = ''
    osWDT = ''
    osCC = ''

    outSent = Sentence(sA_Obj.inSent, osType, osSubj, osVerb, osObj, osInObj, osAdj, osDet, osIN, osPP, osMD, osWDT, osCC)
    

    print(' --- start prattle ---')

    if sA_Obj.sType == 'interrogative':
        print(' sType should be interrogative:')
        print(sA_Obj.sType)
        processInterrogative(sA_Obj, outSent)
        
    elif sA_Obj.sType == 'declarative':
        print(' sType should be declarative:')
        print(sA_Obj.sType)
        
    elif sA_Obj.sType == 'imperative':
        print(' sType should be imperative:')
        print(sA_Obj.sType)
        
    elif sA_Obj.sType == 'exclamative':
        print(' sType should be exclamative:')
        print(sA_Obj.sType)
        
    else:
        print(' Unrecognized sType')
        print(sA_Obj.sType)
        

    print(' --- end prattle ---')

    return outSent


def processInterrogative(sA_Obj, outSent):

    print(' --- start processInterrogative ---')

    if sA_Obj.sWDT[0] == 'how':
        processHow(sA_Obj, outSent)
    else:
        print(' Inrecognized sWDT:')
        print(sA_Obj.sWDT[0])



    print(' --- end processInterrogative ---')



def processHow(sA_Obj, outSent):

    print(' --- start processHow ---')

    if sA_Obj.sSubj[0] == 'you':
        outSent.sSubj = 'I'
        if type(sA_Obj.sVerb[0]) is list:
            if len(sA_Obj.sVerb) == 2: # Only processing 2 for now
                if sA_Obj.sVerb[1][0] == 'feel':
                    outSent.sVerb = 'do not feel'
                if sA_Obj.sObj != '':
                    outSent.sObj = sA_Obj.sObj
                    
                    return
        if len(sA_Obj.inSent) == 3:
            if sA_Obj.sVerb[0] == 'are':
                outSent.sVerb = 'good'
                return

    print(' --- end processHow ---')
    
    

if __name__ == "__main__":

    print(' ------ Start processOutput ------')

    sA_Obj = loadPickle('sA_Obj')
    sA_Obj.printAll()
    
    outSent = prattle(sA_Obj)
    outSent.printAll()

    print(' ------ End processOutput ------')
    
