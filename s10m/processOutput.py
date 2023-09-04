#
# processOutput.py
#

import pickle

from datetime import datetime

from commonUtils import Sentence
from commonUtils import list2String
from commonConfig import simp



def buildOutputObj(sA_Obj, outObj, ppResults, simpDB):

    sType = 'output'
    sSubj = ''
    sVerb = ''
    sObj = ''
    sInObj = ''
    sAdj = ''
    sDet = ''
    sIN = ''
    sPP = ''
    sMD = ''
    sWDT = ''
    sCC = ''
    sRB = ''
    sUH = ''

    outObj = Sentence(sA_Obj.inSent, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC, sRB, sUH)
    

    print(' --- start buildOutputObj ---')

    if sA_Obj.sType == 'interrogative':
        print(' sType should be interrogative:')
        print(sA_Obj.sType)
        outObj.sType = 'output to interrogative'
        print(outObj.sType)
        outObj = processInterrogative(sA_Obj, outObj, ppResults, simpDB)
        
    elif sA_Obj.sType == 'declarative':
        print(' sType should be declarative:')
        print(sA_Obj.sType)
        outObj = processDeclarative(sA_Obj, outObj, ppResults, simpDB)
        
    elif sA_Obj.sType == 'imperative':
        print(' sType should be imperative:')
        print(sA_Obj.sType)
        
    elif sA_Obj.sType == 'exclamative':
        print(' sType should be exclamative:')
        print(sA_Obj.sType)
        
    else:
        print(' Unrecognized sType')
        print(sA_Obj.sType)
        

    print(' --- end buildOutputObj ---')

    return outObj


def processInterrogative(sA_Obj, outObj, ppResults, simpDB):

    print(' --- start processInterrogative ---')

    if sA_Obj.sWDT[0] in ['how', 'How']:
        outObj = processHow(sA_Obj, outObj)
    else:
        print(' Unrecognized sWDT:')
        print(sA_Obj.sWDT[0])



    print(' --- end processInterrogative ---')
    
    return outObj


def processDeclarative(sA_Obj, outObj, ppResults, simpDB):

    print(' --- start processDeclarative ---')

    if sA_Obj.sSubj[0] == simp:
        if sA_Obj.sUH[0] in ['hello', 'Hello']:
            outObj.sUH = 'Hello'
            return outObj
        
    if len(sA_Obj.sSubj) > 0:
        outObj.sSubj = sA_Obj.sSubj
    

    print(' --- end processDeclarative ---')

    return outObj


def processHow(sA_Obj, outObj):

    print(' --- start processHow ---')

    if sA_Obj.sSubj[0] == 'you':
        outObj.sSubj = 'I'
        if type(sA_Obj.sVerb[0]) is list:
            if len(sA_Obj.sVerb) == 2: # Only processing 2 for now
                if sA_Obj.sVerb[1][0] == 'feel':
                    outObj.sVerb = 'do not feel'
                if sA_Obj.sObj != '':
                    outObj.sObj = sA_Obj.sObj
                    
                    #return
                
        if sA_Obj.sVerb[0] == 'are':
            outObj.sVerb = 'good'

        if sA_Obj.sObj != '':
            outObj.sObj = sA_Obj.sObj[0]
            
            #return

    print(' --- end processHow ---')
    return outObj


def prattle(sA_Obj, outObj, ppResults, simpDB):

    print('---- start prattle ----')
    print('--- outObj ---')
    outObj = buildOutputObj(sA_Obj, None, ppResults, simpDB)
    outObj.printAll()

    print('sType: ', outObj.sType)

    if len(outObj.sUH) > 0:
        outSent = outObj.sUH
    else:
        if outObj.sSubj == '':
            sentSubject = '>Unknown subject<'
        else:
            print(type(outObj.sSubj))
            sentSubject = outObj.getSubjects()
            sentSubject = list2String(sentSubject)
            print(sentSubject)
            

        if outObj.sVerb == '':
            sentVerb = '>Unknown verb<'
        else:
            sentVerb = outObj.sVerb

        if outObj.sObj == '':
            sentObject = '>Unknown or no object<'
        else:
            sentObject = outObj.sObj

        outSent = str(sentSubject) + ' ' + str(sentVerb) + ' ' + str(sentObject)

    now = datetime.now()
    nowStr = now.strftime("%d/%m/%Y %H:%M")
    conversation = simpDB["conversation"]
    conversation.insert_one({"Input": sA_Obj.inSent, "Output": outSent, "DateTime": nowStr})
    

    print('---- end prattle ----')
    return outSent
    
    

if __name__ == "__main__":

    print(' ------ Start processOutput ------')

    sA_Obj = loadPickle('sA_Obj')
    sA_Obj.printAll()

    print('--- outObj ---')
    outObj = buildOutputObj(sA_Obj)
    outobj.printAll()

    outSent = prattle(sA_Obj, outObj, ppResults)

    print('----')
    print('outSent:')
    print(outSent)
    
    print(' ------ End processOutput ------')
    
