#
# simpSA.py
#
#    Sentence analysis--determine SVO
"""
    declarative sentence (statement)
    interrogative sentence (question)
    imperative sentence (command)
    exclamative sentence (exclamation)
"""

import simpConfig as sc


class Sentence:

    def __init__(self, inSent, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):
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
        self.sWDT = sWDT

        
def processNP(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):
    
    if sc.verbose: 
        print('iLst[0][0] == NP')
        print(iLst[0])
        print('.', iLst[0][1])
        
    if iLst[0][1] in ['NP','NNP','NN','NNS']: # Included NP for NP NP NNx
        if firstLine:
            sType = 'declarative'
            if sSubj == '':
                sSubj = iLst[1] + ',' + iLst[0][1]
                if sc.verbose: print('..', sSubj)
            else:
                if sc.verbose: print('Who this: ', iLst[1])

            if len(iLst) > 2:
                if iLst[2][0] == 'VP':
                    if iLst[2][1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
                        sVerb = iLst[3]
                        if len(iLst) > 3:
                            print('*** ', iLst)
                            print('len(iLst: ', len(iLst))
                            if sObj == '':
                                if iLst[2][0] == 'NP':
                                    if iLst[2][1] in ['NP','NNP','NN','NNS']:
                                        sObj = iLst[3] + ',' + iLst[2][1]
                            else:
                                if iLst[2][0] == 'NP':
                                    if iLst[2][1] in ['NP','NNP','NN','NNS']:
                                        sObj = sObj + ';' + iLst[3] + ',' + iLst[2][1]
        else:
            if sVerb == '':
                if sTypLst == 'interrogative':
                    sSubj = iLst[1] + ',' + iLst[0][1]
                    if sc.verbose: print('who dat1 ', iLst[1])
                else:
                    sObj = iLst[1] + ',' + iLst[0][1]
                    if sc.verbose: print('who dat2 ', iLst[1])
            else:
                if sSubj == '':
                    if len(iLst[0]) == 2:
                        sSubj = iLst[1] + ',' + iLst[0][1]
                    elif len(iLst[0]) == 3:
                        sSubj = iLst[1] + ',' + iLst[0][2]
                    else:
                        print('NP iLst[0][x] len error')
                else:
                    print('sSubj: ', sSubj)
                    print(type(sSubj))
                    sSubj = sSubj + ';' + iLst[1] + ',' + iLst[0][1]
                    if sc.verbose: print('who dat ', iLst[1])
                                
                if len(iLst) > 2:
                    if iLst[2][0] == 'VP':
                        if iLst[2][1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
                            if sVerb == '':
                                sVerb = iLst[3]
                            else:
                                sVerb = sVerb + ',' + iLst[3]
    elif iLst[0][1] == 'DT':
        if firstLine:
            sType = 'declarative'
            sDet = iLst[1]
            if len(iLst) > 2:
                if iLst[2][0] in ['NP','NNP','NN','NNS']:
                    sSubj = iLst[3] + ',' + iLst[2][0]
                    if len(iLst) > 4:
                        if iLst[4][0] in ['VP','VB','VBD','VBG','VBN','VBP','VBZ']:
                            sVerb = iLst[5]
        else:
            sDet = iLst[1]
            if len(iLst) > 2:    
                if iLst[2][0] in ['NN','NNS']:
                    if sSubj == '':
                        sSubj = iLst[3] + ',' + iLst[2][0]
                    else:
                        sSubjTemp = iLst[3] + ',' + iLst[2][0] # Hold value and wait to see if we find an sObj
                                    
    elif iLst[0][1] == 'PRP':
        if firstLine:
            sType = 'declarative'
            sSubj = iLst[1], ',' + iLst[0][1]
        else:
            if sSubj == '':
                sSubj = iLst[1] + ',' + iLst[0][1]
            else:
                sSubj = sSubj + ';' + iLst[1] + ',' + iLst[0][1] 
                        
    firstLine = False

    return firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT


def processVP(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):

    if sc.verbose: 
        print('iLst[0][0] == VP')
        print(iLst[0])
    if iLst[0][1] in ['VB','VBD','VBG','VBN','VBZ']:
        if firstLine:
            sType = 'imperative'
            sVerb = iLst[1]

            if len(iLst) > 2:
                if iLst[2][0] in ['NP','NNP','NN','NNS']: # Included NP for NP NP NNx
                    if iLst[2][1] == 'DT':
                        sDet = iLst[3]
                        if len(iLst) > 4:
                            if iLst[4][0] in ['NP','NNP','NN','NNS']:
                                sObj = iLst[5] + ',' + iLst[4][0]
                    else:
                        sSubj = iLst[3] + ',' + iLst[2][0]
                        if len(iLst) > 4:
                            if iLst[4][0] == 'VP':
                                if iLst[4][1] in ['VB','VBD','VBG','VBN','VBZ']:
                                    if sVerb == '':
                                        sVerb = iLst[5]
                                    else:
                                        sVerb = sVerb + ',' + iLst[5]
        else:
            if sVerb == '':
                sVerb = iLst[1]
            else:
                sVerb = sVerb + ',' + iLst[1]
            if len(iLst) > 2:
                if iLst[2][0] == 'NP':
                    if iLst[2][1] in ['NP','NNP','NN','NNS']:
                        if sObj == '':
                            sObj = iLst[3] + ',' + iLst[2][1]
                        else:
                            sObj = sObj + ';' + iLst[3] + ',' + iLst[2][1]
                    elif iLst[2][1] == 'DT':
                        if sDet == '':
                            sDet = iLst[3]
                        else:
                            sDet = sDet + ',' + iLst[3]
                        if len(iLst) > 4:
                            if iLst[4][0] in ['NP','NNP','NN','NNS']:
                                if sObj == '':
                                    sObj = iLst[5] + ',' + iLst[4][0]
                                else:
                                    sObj = sObj + ';' + iLst[5] + ',' + iLst[4][0]
    firstLine = False

    return firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT


def processVerbs(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):

    if sc.verbose: 
        print('iLst[0][0] in [VB,VBD,VBG,VBN,VBP,VPZ]')
        print(iLst[0])
    if not firstLine:
        if sVerb == '':
            sVerb = iLst[1]
        else:
            sVerb = sVerb + ',' + iLst[1]
    else:
        sType = 'imperative'
        sVerb = iLst[1]
                
    firstLine = False

    return firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT


def processPP(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):
         
    if sc.verbose: 
        print('iLst[0][0] == PP')
        print(iLst[0])
    if iLst[0][1] == 'IN':
        sIN = iLst[1]
        if len(iLst) > 2:
            if iLst[2][0] == 'NP':
                if iLst[2][1] == 'DT':
                    sDet = iLst[3]
                    if len(iLst) > 4:
                        if iLst[4][0] in ['NN', 'NNP', 'NNS']:
                            sObj = iLst[5] + ',' + iLst[4][0]
                            sPP = sIN + ',' + sDet + ',' + iLst[5]
    firstLine = False

    return firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT 


def processWDT(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):

    if sc.verbose: 
        print('iLst[0][0] == WDT')
        print(iLst[0])
        print('iLst: ', str(iLst))
                    
    if firstLine:
        sType = 'interrogative'
        sWDT = iLst[1]
        
        if len(iLst) > 2:
            if iLst[2][1] in ['VP','VB','VBD','VBG','VBN','VBP','VBZ']:
                sVerb = iLst[3]
                if len(iLst) > 4:
                    if iLst[4][1] in ['NNP','NN']:
                        if sSubj == '':
                            sSubj = iLst[5] + ',' + iLst[4][1]
                        else:
                            sSubj = sSubj + ';' + iLst[5] + ',' + iLst[4][1]
                    elif iLst[4][1] == 'DT':
                        sDet = iLst[5]
                        if len(iLst) > 6:
                            if iLst[6][0] == 'NN':
                                if sSubj == '':
                                    sSubj = iLst[7] + ',' + iLst[6][0]
                                else:
                                    sSubj = sSubj + ',' + iLst[7] + ',' + iLst[6][0]
    firstLine = False

    return firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT


def processMD(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT):

    if sc.verbose: 
        print('iLst[0][0] == MD')
        print(iLst[0])
        print('iLst: ', str(iLst))
                
    if firstLine:
        sType = 'interrogative'
        print('MD firstLine: ')

        if sMD == '':
            sMD = iLst[1]
        else:
            sMD = sMD + ';' + iLst[1]

        if len(iLst) > 4:
            if iLst[2][0] in ['NP','NNP','NN','NNS']:
                if sSubj == '':
                    sSubj = iLst[3] + ',' + iLst[2][1]
                else:
                    sSubj = sSubj + ';' + iLst[3] + ',' + iLst[2][1]

                if len(iLst) > 5:
                    if iLst[4][0] in ['VP','VB','VBD','VBG','VBN','VBP','VPZ']:
                        if sVerb == '':
                            sVerb = iLst[5]
                        else:
                            sVerb = sVerb + ',' + iLst[5]
    else:
        print('MD not firstLine: ')
        if sMD == '':
            sMD = iLst[1]
        else:
            sMD = sMD + ';' + iLst[1]

    firstLine = False

    return firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT



# Attempt to analyze the sentence per CFG (find SVO)
####################################################
def sentAnalysis(t, s):
   
    print('--- sentAnalysis ---')

    sPOS = ''
    sType = ''
    sSubj = ''
    sVerb = ''
    sObj = ''
    sDet = ''
    sIN = ''
    sPP = ''
    sMD = ''
    sWDT = ''
    sSubjTemp = ''

    sent = Sentence(s, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)

    firstLine = True

    t = t.replace('\Tree ', '')
    t = t.replace('[.S', '')
    t = t[:-1]

    tLst = t.split('\n')
    sTypLst = []
    tmpLst = []
    
    for item in tLst:
        item = item.strip()
        if len(item) > 0:
            tmpLst.append(item)

    if sc.verbose: print('tmpLst: ', str(tmpLst))

    for item in tmpLst:

        iLst = buildItemList(item)

        if sc.verbose: 
            print('item:  >>' + item + '<<')
            print('iLst --->', iLst)
            
        if len(iLst) > 0:

            if iLst[0][0] == 'NP':

                firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT = processNP(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)
                
            elif iLst[0][0] == 'VP':

                firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT = processVP(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)

            elif iLst[0][0] in ['VB','VBD','VBG','VBN','VBP','VBZ']:

                firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT = processVerbs(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)
                                                                                         
            elif iLst[0][0] == 'PP':

                firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT = processPP(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)

            elif iLst[0][0] == 'WDT':

                firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT = processWDT(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)

            elif iLst[0][0] == 'MD':

                firstLine, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT = processMD(firstLine, iLst, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD, sWDT)
                
            else:
                print('sentAnalysis else -- something wrong or not defined?')
                print(iLst)
                print(str(firstLine))
                
                firstLine = False

    # Korny where to deal with additional sSubj's
    if len(sSubjTemp) > 0:
        if len(sObj) > 0:
            sSubj = sSubj + ';' + sSubjTemp
            
    if sc.verbose: 
        print('--_-_-_-_-_-_-_-_-_-_--')
        print('Input sentence w/corrected case:')
        print(s)
        print('----------------------')
        print('sPOS =  ', sPOS)
        print('sType = ', sType)
        print('sSubj = ', sSubj)
        print('sVerb = ', sVerb)
        print('sObj =  ', sObj)
        print('sDet =  ', sDet)
        print('sIN =   ', sIN)
        print('sPP =   ', sPP)
        print('sMD =   ', sMD)
        print('sWDT =  ', sWDT)

#        sent.inSent = inSent   # Set at init
        sent.sPOS   = sPOS
        sent.sType  = sType
        sent.sSubj  = sSubj
        sent.sVerb  = sVerb
        sent.sObj   = sObj
        sent.sDet   = sDet
        sent.sIN    = sIN
        sent.sPP    = sPP
        sent.sMD    = sMD
        sent.sWDT   = sWDT

        print('----------------------')
        print('sent.inSent: ', sent.inSent)
        print('sent.sPOS =  ', sent.sPOS)
        print('sent.sType = ', sent.sType)
        print('sent.sSubj = ', sent.sSubj)
        print('sent.sVerb = ', sent.sVerb)
        print('sent.sObj =  ', sent.sObj)
        print('sent.sDet =  ', sent.sDet)
        print('sent.sIN =   ', sent.sIN)
        print('sent.sPP =   ', sent.sPP)
        print('sent.sMD =   ', sent.sMD)
        print('sent.sWDT =  ', sent.sWDT)

    print('--- end sentAnalysis ---')

    return sent
# End sentAnalysis


# Build a list of the item/string
####################################################
def buildItemList(s):

    tags = []
    word = ""
    wordTags = []

    row = []
    col = []

    for sIdx in range(len(s)):
        if s[sIdx] == ' ':
            col.append(row)
            row = []
        else:
            row.append(s[sIdx])
    
    for c in col:
        tag = ''
        if len(c) > 2 and c[1] == '.':
            if len(c) == 4: # NP, DT, VB,...
                tag = c[-2] + c[-1]
            elif len(c) == 5: # NNP, NNS, VBD,...
                tag = c[-3] + c[-2] + c[-1]
            elif c[-1] == 'S': # Don't forget the S--S has been stripped, so not needed?
                tag = c[-1]

            tags.append(tag)
                
        elif c[0] not in ['[',']']:
            word = ''.join(c)
            wordTags.append(tags)
            wordTags.append(word)
            tags = []
            
    return wordTags


