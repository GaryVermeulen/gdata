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
#

import sys
import simpConfig as sc


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
    sSubjTemp = ''

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
            
#        print('---')
        if len(iLst) > 0:
#            print(type(iLst))
#            print(len(iLst))
#            print(iLst)
#            print('----')

            if iLst[0][0] == 'NP':
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
                            if sTypLst[0] == 'interrogative':
                                sSubj = iLst[1] + ',' + iLst[0][1]
                                if sc.verbose: print('who dat1 ', iLst[1])
                            else:
                                sObj = iLst[1] + ',' + iLst[0][1]
                                if sc.verbose: print('who dat2 ', iLst[1])
                        else:
                            if sSubj == '':
                                sSubj = iLst[1] + ',' + iLst[0][1]
                            else:
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

            elif iLst[0][0] == 'VP':
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
                
            elif iLst[0][0] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
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
            elif iLst[0][0] == 'PP':
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
                                        sPP = sIN + ',' + sDet + ',' + sObj
                firstLine = False
            elif iLst[0][0] == 'WDT':
                if sc.verbose: 
                    print('iLst[0][0] == WDT')
                    print(iLst[0])
                    print('iLst: ', str(iLst))
                    
                sType = 'interrogative,' + str(iLst[1])
                sTypLst = sType.split(',')
                if sc.verbose:
                    print('sType: {}'.format(sType))
                    print('sTypLst: {}'.format(sTypLst))
                    print('len(iLst): ', len(iLst))

                if len(iLst) > 2:
                    if iLst[2][1] == 'VBZ':
                        sVerb = iLst[3]
                        if len(iLst) > 4:
                            if iLst[4][1] in ['NNP','NN']:
                                sSubj = iLst[5] + ',' + iLst[4][1]
                            elif iLst[4][1] == 'DT':
                                sDet = iLst[5]
                                if len(iLst) > 6:
                                    if iLst[6][0] == 'NN':
                                        sSubj = iLst[7] + ',' + iLst[6][0]
                
                firstLine = False

            elif iLst[0][0] == 'MD':
                if sc.verbose: 
                    print('iLst[0][0] == MD')
                    print(iLst[0])
                    print('iLst: ', str(iLst))
                
                if firstLine:
                    sType = 'interrogative'
                    print('MD firstline: ')
                else:
                    print('MD else: ')
                    
                if sMD == '':
                    sMD = iLst[1]
                else:
                    sMD = sMD + ',' + iLst[1]

                

                firstLine = False
            else:
                print('else--something wrong or not defined?')
                print(iLst)
                print(str(firstLine))
                
                firstLine = False

    # Korny where to deal with additional sSubj's
    if len(sSubjTemp) > 0:
        if len(sObj) > 0:
            sSubj = sSubj + ';' + sSubjTemp
            
    if sc.verbose: 
        print('======================')
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
        print('sPP =   ',  sPP)
        print('sMD =   ', sMD)

    sent = Sentence(s, sPOS, sType, sSubj, sVerb, sObj, sDet, sIN, sPP, sMD)
                

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

