#
# simpSA.py
#
#   Sentence analysis--determine SVO
#   This version takes a tagged input sentence instead of
#   a CFG tree
"""
    declarative sentence (statement)
    interrogative sentence (question)
    imperative sentence (command)
    exclamative sentence (exclamation)
"""

from simpConfig import *

        
def processNPP(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpInObj = []
    tmpSubj = []
    
    if verbose: 
        print('taggedInput to processNNP:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

        
    if wordPosition == 1:
        sType = 'declarative'

        if sSubj == '':
            sSubj = taggedInput[0]                        
    else:
        if sType == '':
            sType = 'declarative'

        if sVerb != '':
            if sSubj == '':
                sSubj = taggedInput[wordPosition - 1]
            else:
                if sObj == '':
                    sObj = taggedInput[wordPosition - 1]
                else:
                    if sInObj == '':
                        sInObj = taggedInput[wordPosition - 1]
                    else:
                        tmpInObj.append(sObj)
                        sInObj = tmInpObj
                        sInObj.append(taggedInput[wordPosition - 1])
        else:
            if sCC != '':
                tmpSubj.append(sSubj)
                sSubj = tmpSubj
                sSubj.append(taggedInput[wordPosition - 1])
                    
    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processNN(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpInObj = []
    
    if verbose: 
        print('taggedInput to processNN:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'declarative'

        if sSubj == '':
            sSubj = taggedInput[0]                        
    else:
        if sType == '':
            sType = 'declarative'

        if sVerb != '':
            if sSubj == '':
                sSubj = taggedInput[wordPosition - 1]
            else:
                if sObj == '':
                    sObj = taggedInput[wordPosition - 1]
                else:
                    if sInObj == '':
                        sInObj = taggedInput[wordPosition - 1]
                    else:
                        tmpInObj.append(sObj)
                        sInObj = tmpInObj
                        sInObj.append(taggedInput[wordPosition - 1])
        else:
            if sDet != '':
                if sSubj == '':
                    sSubj = taggedInput[wordPosition - 1]
            
                    
    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processVerbs(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpVerbs = []

    if verbose: 
        print('taggedInput to processVerbs:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'imperative'
        sVerb = taggedInput[0]
    else:
        if sVerb == '':
            sVerb = taggedInput[wordPosition - 1]
        else:
            tmpVerbs.append(sVerb)
            tmpVerbs.append(taggedInput[wordPosition - 1])
            sVerb = tmpVerbs

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processAdj(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    if verbose: 
        print('taggedInput to processAdj:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'declarative'
        sAdj = taggedInput[0]
    else:
        if sAdj == '':
            sAdj = taggedInput[wordPosition - 1]
        else:
            sAdj = sAdj + ';' + taggedInput[wordPosition - 1]

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processDT(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpDet = []

    if verbose: 
        print('taggedInput to processDT:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'declarative'
        sDet = taggedInput[0]
    else:
        if sDet == '':
            sDet = taggedInput[wordPosition - 1]
        else:
            tmpDet.append(sDet)
            tmpDet.append(taggedInput[wordPosition - 1])
            sDet = tmpDet

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processIN(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpIN = []

    if verbose: 
        print('taggedInput to processIN:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'declarative'
        sIN = taggedInput[0]
    else:
        if sIN == '':
            sIN = taggedInput[wordPosition - 1]
        else:
            tmpIN.append(sIN)
            tmpIN.append(taggedInput[wordPosition - 1])
            sIN = tmpIN

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processMD(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpMD = []

    if verbose: 
        print('taggedInput to processMD:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'declarative'
        sMD = taggedInput[0]
    else:
        if sMD == '':
            sMD = taggedInput[wordPosition - 1]
        else:
            tmpMD.append(sMD)
            tmpMD.append(taggedInput[wordPosition - 1])
            sMD = tmpMD

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processWDT(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpWDT = []

    if verbose: 
        print('taggedInput to processWDT:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'interrogative'
        sWDT = taggedInput[0]
    else:
        if sWDT == '':
            sWDT = taggedInput[wordPosition - 1]
        else:
            tmpWDT.append(sMD)
            tmpWDT.append(taggedInput[wordPosition - 1])
            sWDT = tmpWDT

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC


def processCC(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC):

    tmpCC = []

    if verbose: 
        print('taggedInput to processCC:')
        print(taggedInput)
        print('wordPosition: ', wordPosition)

    if wordPosition == 1:
        sType = 'declarative?'
        sCC = taggedInput[0]
    else:
        if sCC == '':
            sCC = taggedInput[wordPosition - 1]
        else:
            tmpCC.append(sMD)
            tmpCC.append(taggedInput[wordPosition - 1])
            sCC = tmpCC

    return sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC







# Attempt to analyze the input sentence
#   from just POS tags (find SVO)
####################################################
def sentAnalysis(taggedInput):
   
    print('--- sentAnalysis ---')

    sPOS = ''
    sType = ''
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
    sSubjTemp = ''
    wordPosition = 0

    sent = Sentence(taggedInput, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)
    
    print('taggedInput to sentAnalysis:')
    print(taggedInput)
    
    for item in taggedInput:

        wordPosition += 1

        print('item: ', item)
        print(len(item))
        print(type(item))
        print('item[0]: ', item[0])
        print('item[1]: ', item[1])

        if item[1] == 'NNP':

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processNPP(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['NN', 'NNS']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processNN(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processVerbs(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['JJ', 'JJR', 'JJS']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processAdj(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['DT']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processDT(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['IN']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processIN(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['MD']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processMD(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)

        elif item[1] in ['CC']:

            sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC = processCC(taggedInput, wordPosition, sType, sSubj, sVerb, sObj, sInObj, sAdj, sDet, sIN, sPP, sMD, sWDT, sCC)


        else:
            print('sentAnalysis else -- something wrong or not defined?')
            print(item)
                            
    if verbose: 
        print('--_-_-_-_-_-_-_-_-_-_--')
        print('Tagged Input Sentence:')
        print(taggedInput)
        print('----------------------')
        print('sType = ', sType)
        print('sSubj = ', sSubj)
        print('sVerb = ', sVerb)
        print('sObj =  ', sObj)
        print('sInObj - ', sInObj)
        print('sAdj =  ', sAdj) 
        print('sDet =  ', sDet)
        print('sIN =   ', sIN)
        print('sPP =   ', sPP)
        print('sMD =   ', sMD)
        print('sWDT =  ', sWDT)
        print('sCC =  ', sCC)

#        sent.inSent = inSent   # Set at init
        sent.sType  = sType
        sent.sSubj  = sSubj
        sent.sVerb  = sVerb
        sent.sObj   = sObj
        sent.sInObj = sInObj
        sent.sAdj   = sAdj
        sent.sDet   = sDet
        sent.sIN    = sIN
        sent.sPP    = sPP
        sent.sMD    = sMD
        sent.sWDT   = sWDT
        sent.sCC    = sCC

        print('----------------------')
        print('sent.inSent: ', sent.inSent)
        print('sent.sType  = ', sent.sType)
        print('sent.sSubj  = ', sent.sSubj)
        print('sent.sVerb  = ', sent.sVerb)
        print('sent.sObj   = ', sent.sObj)
        print('sent.sInObj = ', sent.sInObj)
        print('sent.sAdj   = ', sent.sAdj)
        print('sent.sDet   = ', sent.sDet)
        print('sent.sIN    = ', sent.sIN)
        print('sent.sPP    = ', sent.sPP)
        print('sent.sMD    = ', sent.sMD)
        print('sent.sWDT   = ', sent.sWDT)
        print('sent.sCC    = ', sent.sCC)

    print('--- end sentAnalysis ---')

    return sent
# End sentAnalysis


if __name__ == "__main__":

#    tagged_uI = [['see', 'VBP'], ['hammy', 'NNP'], ['run', 'VB']]
#    tagged_uI = [['see', 'VBP'], ['hammy', 'NNP'], ['run', 'VB'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN']]
#    tagged_uI = [['bob', 'NNP'], ['was', 'VBD'], ['happy', 'JJ']]
#    tagged_uI = [['bob', 'NNP'], ['saw', 'VBD'], ['pookie', 'NNP']]
#    tagged_uI = [['bob', 'NNP'], ['walked', 'VBD'], ['pookie', 'NNP'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN'], ['with', 'IN'], ['hammy', 'NNP']]
    tagged_uI = [['bob', 'NNP'], ['and', 'CC'], ['mary', 'NNP'], ['walked', 'VBD'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN'], ['with', 'IN'], ['pookie', 'NNP']]
#    tagged_uI = [['bob', 'NNP'], ['is', 'VBZ'], ['in', 'IN'], ['the', 'DT'], ['park', 'NN'], ['with', 'IN'], ['pookie', 'NNP'], ['and', 'CC'], ['hammy', 'NNP']]

    sA_Obj = sentAnalysis(tagged_uI)
