#
# Simpleton -- simp.py
#   Simple-Ton: A ton of simple things to do.
#
#

import os

import simpStuff as ss
import simpSA as sa
import simpConfig as sc
import history as h
import simpTree


from datetime import datetime

fConvo = 'convoHist.txt'
hFile = 'history.txt'
convo = []



def showData(data):
    print('- showData -')
    for d in data: print(d)
    print('- End showData -')

def adjustCase(s, data): 
# Adjusts case to match lex data

    slist = s.split(' ')
    ccs = []

    for w in slist:           
        for d in data:                       
            if d[0].lower() == w:
                if d[-1] == 'NNP':
                    w = w.capitalize()                            
        ccs.append(w)
    return ccs


def chkWords(s, inData):
# Returns sentence words not in lex
    words = []

    for d in inData:
        words.append(d[0])
                
    s1 = set(s)
    s2 = set(words)
    ret = s1.difference(s2)
    
    return ret


# May not be needed...~?
def getPOS(s, data):

    sPOS = []
    
    for w in s:
        for d in data:
            if w == d[0]:
                sPOS.append((w,d[-1]))
    return(sPOS)


def simpChat():

    validCFG = False
    cfgOverride = True

    # Read all data (Nx, Vx, etc.)
    inData = ss.getData()
    inDataLen = len(inData)
    if sc.verbose:
        print("getData() returned {} lines of data.".format(inDataLen))
        showData(inData)

    
    # Load weighted sentence history
    print('-history-')
    history = h.History.load_history(hFile)

    for s in history.weightedSentences:
        print(s)
    print('---------')
    
    # Build CFG file from data and cfg_rules
    ss.buildCFG(inData)

    # Develop rudimentary concept of self (I am Simp)
    simpName = 'Simp'
    for i in inData:
        if i[0] == simpName:
            simpData = i
            break

    print("Hello I am: " + simpName)
    if sc.verbose: print("simpData  : {}: ".format(simpData))

    loop = True
    while loop:
        sPOS = ''
        s = input("Enter a short sentence: ")
        
        if len(s) > 0: # Now the fun begins
            if len(convo) > 0:
                print('---- Current conversation:') 
                for c in convo:
                    print(c)
                print('----')
                    
            adjustedS = adjustCase(s, inData) 

            # Are all the words in the sentence in our Lex?
            ret = chkWords(adjustedS, inData)

            if len(ret) > 0:
                # ss.addWord is under construction...
                print('chkWords returned: ' + str(ret))
                ans = input('Learn and add? <y/n>:')

                if ans in ['Y','y']:
                    if ss.addWord(ret):
                        inData = ss.getData() # Refresh input data with new word added
                        if sc.verbose: print('inData refreshed with: ', ret)
                    else:
                        print('!!{} was not added!!'.format(ret))
                else:
                    continue

            # Has this been said before?   Need to revamp...             
            hist = ss.chkHistory(adjustedS)

            if len(hist) > 0:
                if sc.verbose: print('Something old...')    
                saidBefore = True
            else:
                if sc.verbose: print('Something new...')                    
                saidBefore = False
            
            # Parse corrected case sentence (input) per grammar
            # Draw out the grammar tree?
            draw = False
            grammarTree = ss.chkGrammar(adjustedS, draw)

            if grammarTree == None:
                validCFG = False
                if sc.verbose: print('grammarTree == none')

                sPOS = getPOS(adjustedS, inData)
                if sc.verbose: print('ccs tagged, sPOS: ', sPOS)

                sA = sa.Sentence('', '', '', '', '', '', '', '', '', '', '')
                
                sA.inSent = adjustedS
                sA.sPOS = sPOS

                print('--- A valid CFG was not returned. ---')

            else:
                validCFG = True

                tStr = grammarTree.pformat_latex_qtree()
                print("\n------------")
                print('tStr:')
                print(tStr)
                print("\n------------")
                
                sA = sa.sentAnalysis(tStr, adjustedS)
                print("\n------------")
                print("sA.inSent: ")
                print(sA.inSent)
                print(type(sA.inSent))
                print("\n------------")

            # Check input sentence with previous sentences in weighted history file/class
            print('Checking weighted history...')
            if history.sentence_exist(adjustedS):
                print('adjustedS found in weighted history, weight: ', history.get_weight(adjustedS))
                history.incrementWeight(adjustedS)

                print('increamented weight to: ', history.get_weight(adjustedS))
            else:
                history.add(list((adjustedS, 1)))
                print('Added adjustedS to weighted history w/weight of : ', history.get_weight(adjustedS))

            print('-' * 5)
            if not validCFG and (history.get_weight(adjustedS) > 5):
                print('{} has been mentioned over 5 times, checking CFG...'.format(adjustedS))

                cfgOverride = True
                
                chkCFGResults = chkCFG(adjustedS)

                for r in chkCFGResults:
                    print(r)
            elif not validCFG and (history.get_weight(adjustedS) <= 5):
                cfgOverride = False
                
            print('-' * 5)
            
            # Add data/KB stuff here...~?
            if cfgOverride:
                print('--- cfgOverride = True, so let us attempt to find some knowledge')

                print('----------------------')
                print('sA.inSent: ', sA.inSent)
                print('sA.sPOS:   ', sA.sPOS)
                print('sA.sType:  ', sA.sType)
                print('sA.sSubj:  ', sA.sSubj)
                print('sA.sVerb:  ', sA.sVerb)
                print('sA.sObj:   ', sA.sObj)
                print('sA.sDet:   ', sA.sDet)
                print('sA.sIN:    ', sA.sIN)
                print('sA.sPP:    ', sA.sPP)
                print('sA.sMD:    ', sA.sMD)
                print('sA.sWDT:   ', sA.sWDT)

                if validCFG:
                    w = simpTree.peruseData(sA)
                else:
                    w = simpTree.peruseDataNoCFG(sA)

                print('peruseData returned:')
                print(w)
                print('---')
                

            # Save sentence to list and conversation history file
            # 
            if sc.verbose: print('Retaining convo and weighted history files...')

            if sA.inSent != '':
                convo.append(sA.inSent)
                
                f = open(fConvo, 'a')
                f.write('\n' + str(sA.inSent))
                f.close()

            history.save_history(hFile, history.weightedSentences)

        else:
            if sc.verbose: print('Exiting chat...')
            loop = False

    # Archiving convo history
    now = datetime.now()
    timeStamp = now.strftime("%m%d%y-%H%M%S")

    if os.path.isfile('convoHist.txt'):
        os.rename('convoHist.txt', 'convoHist.txt' + '.' + timeStamp)
        
    return

def chkCFG(sent):

    draw = False
    idx = 0
    chkSent = []
    chkSentResults = []
    
    for w in sent:
        print('Checking: ', sent[idx])
        chkSent.append(sent[idx])
        grammarTree = ss.chkGrammar(chkSent, draw)
        chkSentResults.append(grammarTree)
        idx += 1

    return chkSentResults


if __name__ == "__main__":

    print("Simple-Ton, A ton of simple things to do.")

    simpChat()
        
    print('End Simple-Ton.')
    
